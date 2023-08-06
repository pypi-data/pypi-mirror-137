# Copyright (C) 2018-2021  The Plenpy Authors
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


"""
Module defining the :class:`LytroIllum` camera class.

This camera class, derived from the :class:`AbstractLightFieldCamera` base
class, implements the Lytro Illum camera.

"""
from itertools import product
from pathlib import Path
from typing import Optional, Any

import gc
import imageio
import numpy as np
from numpy.core import ndarray

import plenpy.logg
from plenpy.cameras.abstract_lightfield_camera import AbstractLightFieldCamera
from plenpy.lightfields import LightField
from plenpy.utilities import demosaic
from plenpy.utilities.misc import get_avail_extensions

logger = plenpy.logg.get_logger()

__all__ = ['LytroIllum']

# Use Lytro Illum lfr amd raw format from imageio plugins
imageio.formats.sort('lytro-illum-lfr')
imageio.formats.sort('lytro-illum-raw')


class LytroIllum(AbstractLightFieldCamera):
    """Lytro Illum light field camera.

    The class does not add any attributes to the
    :class:`AbstractLightFieldCamera` base class.

    """

    def __init__(self, path: Any, format='LYTRO-ILLUM-RAW'):
        """
        Args:
            path: Folder path of camera.
            format: The ``imageio`` format of the white images.
                    Default: LYTRO-ILLUM-RAW.
        """
        # Call init from AbstractLightfieldCamera base class
        super().__init__(path,
                         microlens_size=14,
                         grid_type='hex',
                         ml_focal_length=40e-6)
        self._format = format

        # Add image resolution
        # Use full sensor image for calibration and decoding
        shape = (5368, 7728)
        self._shape_original = shape
        self._crop_slice_x = slice(0, shape[0])
        self._crop_slice_y = slice(0, shape[1])
        self._validate_crop()

    def _validate_crop(self):
        """Check whether set crop slice are valid."""
        if self._crop_slice_x.start % 2 != 0 or \
           self._crop_slice_y.start % 2 != 0:
            raise ValueError("Odd crop offset not currently supported as it "
                             "results in a different Bayer pattern than what is implemented.")
        self._shape_crop = (self._crop_slice_x.stop - self._crop_slice_x.start, self._crop_slice_y.stop - self._crop_slice_y.start)

    def _crop_raw(self, im):
        """Crop original raw sensor image to specified slices"""
        # If empty, return directly (migh tbe the case when only reading metadata)
        if im.size == 0:
            return im

        # If slice covers full image, return original
        if im.shape[0] == self._crop_slice_x.stop - self._crop_slice_x.start and \
           im.shape[1] == self._crop_slice_y.stop - self._crop_slice_y.start:
            return im

        return im[self._crop_slice_x, self._crop_slice_y]

    def calibrate(self,
                  filename: Optional[str] = None,
                  method: str = 'own',
                  force: bool = False):
        """Calibrate the Lytro Illum camera.

        The calibration estimates the microlens centers from the provided
        white images. Based on the chosen method, this will yield ml centers
        with (``det_method='own'``) or without (``det_method='dans'``)
        subpixel precision. Using the estimated ML centers, an ideal grid is
        estimated that best approximates the ML centers.
        This grid is used in the decoding of every light field
        (depending on the zoom and focus settings).

        Args:
            filename: System path to calibration filename withoout extension.
                      If ``None``, the standard path is used.

            method: Method used for grid estimation.
                        - 'own': Own method, proposed in [ref]
                        - 'dans': Method by Dansereau et al.

            force: If ``True`` forces the recalibration, even if a calibration
                   file is found. This can be useful when recalibrating with
                   different parameters.
        """

        logger.info("Calibrating Lytro Illum camera...")

        if filename is not None:
            self._calDataFilename = (self.calibrationFolderPath / filename).with_suffix(".npz")

        # If a calibration file is found, load it
        if (self.path / self._calDataFilename).is_file() and not force:
            logger.info(
                f"Found calibration file '{self._calDataFilename}'. "
                "Reading from calibration file.")
            self._load_cal_data()
        else:
            logger.info(
                f"No calibration file '{self._calDataFilename}' found. "
                "Creating new.")

        # Read white images (or update)
        self._create_wi_db()

        # Calculate grid parameters and align transformation
        self._process_wi_db(method=method)

        # Save calibration data for next use
        self._save_cal_data()

        self._isCalibrated = True
        logger.info("... done.")
        return

    def decode_sensor_image(self,
                            num: int,
                            demosaic_method: str = 'malvar2004',
                            resample_method: str = 'guided'):
        """Decode the specified sensor image.

        The decoding yields a
        :class:`.plenpy.lightfields.lightfield.LightField` object that is
        added the objects dictionary of decoded images.

        Args:
            num: Number of the sensor image that is to be decoded.

            demosaic_method : Method used to calculate the demosaiced image.
                If ``None`` is specified, no demosaicing is performed. For
                available methods and default value,
                see :func:`plenpy.utilities.demosaic.get_demosaiced()`.

            resample_method: Method used to resample the light field from a
                hex to rect grid. Available:
                - 'guided': Perform gradient guided interpolation (recommended)
                - 'bilinear' : Perform bilinear interpolation.
                - 'horizontal': Only use horizontal 1D-interpolation
                - 'vertical': Only use vertical 1D-interpolation



        """
        # Check if camera is calibrated. If not, calibrate it.
        if not self._isCalibrated:
            self.calibrate()

        # Get raw sensor image and metadata corresponding to number num
        raw_img = np.squeeze(self.get_sensor_image(num))
        raw_img = self._crop_raw(raw_img)
        metadata = self.get_image_metadata(num)

        # Get the white image corresponding to current zoom and focus setting
        zoomstep = metadata['metadata']['devices']['lens']['zoomStep']
        focusstep = metadata['metadata']['devices']['lens']['focusStep']
        serial_number = metadata['privateMetadata']['camera']['serialNumber']
        if serial_number != self._serial_number:
            raise ValueError(f"Image's serial number {serial_number} not identical "
                             f"to camera's serial number {self._serial_number}.")

        # First, get all WI with same/similar zoomstep
        diff_ = np.abs(self._whiteImageDb['zoomStep'] - (zoomstep))
        idx_ = np.argwhere(diff_ == diff_.min())

        # Now, find those with similar focus step
        if len(idx_) > 1:
            wi_select = self._whiteImageDb[idx_]
            diff_ = np.abs(wi_select['focusStep'] - (focusstep))
            idx_select_ = np.argmin(diff_)
            idx_ = np.argwhere(self._whiteImageDb == wi_select[idx_select_])

        wi_select_idx = np.squeeze(idx_)

        # Load corresponding white image
        wi_select = self._get_wi(self._whiteImageDb[wi_select_idx]['path'],
                                 process=False)

        # Get white and black level from metadata
        white_dict = metadata['metadata']['image']['pixelFormat']['white']
        black_dict = metadata['metadata']['image']['pixelFormat']['black']

        # Convert levels to float from 10 bit uint
        white = np.mean([white_dict[key] for key in white_dict]) / (2**10 - 1)
        black = np.mean([black_dict[key] for key in black_dict]) / (2**10 - 1)

        # Remove black and white levels
        raw_img = (raw_img - black) / (white - black)
        wi_select = (wi_select - black) / (white - black)

        # Devignetting, divide by selected white image
        raw_img = np.clip(raw_img / wi_select, 0, 1)

        # Might encounter division by zero...
        raw_img[np.isnan(raw_img)] = 0

        del wi_select, black, white, white_dict, black_dict
        gc.collect()

        # Demosaic raw image
        logger.info("Demosaicing sensor image...")
        img = demosaic.get_demosaiced(raw_img,
                                      pattern='GRBG',
                                      method=demosaic_method)
        logger.info("...done.")

        del raw_img
        gc.collect()

        # Aligning the sensor image
        img = self._align_image(img, wi_idx=wi_select_idx)

        # Slice image to light field
        lf = self._slice_image(img, wi_idx=wi_select_idx)

        del img
        gc.collect()

        # Only use central subapertures
        u, v, s, t, ch = lf.shape
        step = self._microlensRadius - 1
        u_mid = int(u / 2)
        v_mid = int(v / 2)
        data = lf[u_mid - step:u_mid + step + 1, v_mid - step:v_mid + step + 1]
        lf = LightField(data)

        # Resampling the light field:
        lf = self._resample_lf(lf, method=resample_method)

        self._add_decoded_image(img=lf, num=num)

        return

    def _process_wi_db(self, method):
        # Calculate grid parameters and align transformation
        self._est_grid(method=method)

        return

    def _create_raw_wi_db(self):

        # Read all available images in White Image folder
        white_image_paths = [f.relative_to(self.path) for f in (self.path/self.whiteImageFolderPath).glob("**/*")
                             if f.suffix in get_avail_extensions()
                             and not f.suffix == '.npz']

        white_image_paths.sort()

        if self._rawWhiteImageDb is None:
            # Create initial database with raw data
            self._rawWhiteImageDb = np.squeeze(
                np.stack([self._get_wi_db_entry(path) for path in white_image_paths]))
        else:
            white_image_paths = set([str(i) for i in white_image_paths]) - set(self._rawWhiteImageDb['path'].tolist())
            white_image_paths = [Path(i) for i in list(white_image_paths)]
            if len(white_image_paths) > 0:
                logger.info(f"Found {len(white_image_paths)} new raw white image(s). Updating database...")
                new_db_entries = np.stack([self._get_wi_db_entry(path) for path in white_image_paths])
                new_db_entries = np.squeeze(new_db_entries, axis=-1)
                self._rawWhiteImageDb = np.concatenate((self._rawWhiteImageDb, new_db_entries))

        # If only one item is contained, extend dimension
        if self._rawWhiteImageDb.ndim == 0:
            self._rawWhiteImageDb = np.array([self._rawWhiteImageDb])

        if self._serial_number is None:
            serial_number = set(self._rawWhiteImageDb['serial_number'].tolist())
            if len(serial_number) != 1:
                raise ValueError(f"Found raw white images with more than one "
                                 f"serial number.\n {self._rawWhiteImageDb}")
            self._serial_number = serial_number.pop()
        else:
            if np.any(self._rawWhiteImageDb['serial_number'] != self._serial_number):
                raise ValueError(f"Found raw white images with incorrect serial "
                                 f"number. The camera serial number is {self._serial_number}. "
                                 f"Found:\n {self._rawWhiteImageDb[np.where(self._rawWhiteImageDb['serial_number'] != self._serial_number)]}")

    def _create_wi_db(self):
        logger.info(f"Creating white image database...")

        # Create raw white image database
        self._create_raw_wi_db()

        # Look up raw white images with (almost) identical zoom and focus
        # Average them
        if self._whiteImageDb is None:
            # For first time creation, initialize
            self._whiteImageDb = np.array([], dtype=self._whiteImageDbDtype)
            paths_processed = []
        else:
            paths_processed = [i for sublist in self._whiteImageDb['processed_paths_raw'].tolist() for i in sublist]
            paths_processed = list(set(paths_processed))

        db = self._rawWhiteImageDb
        for paths_curr, exposure, iso, focus_step, zoom_step \
                in self.unique_geometry_exposure_gen(db, paths_processed):


            name = f"white_image_zoomStep_{zoom_step}_focusStep_{focus_step}.npy"
            save_path = self.path / self.calibrationFolderPath / name

            if not save_path.exists():
                wi = np.mean([self._get_wi(self.path / f, process=False) for f in paths_curr],
                             axis=0,
                             dtype=np.float32)

                paths_processed += paths_curr

                # Normalize
                wi = wi.astype(np.float64)
                wi -= wi.min()
                wi /= wi.max()

                # Save white image
                np.save(save_path, wi)
                del wi
                gc.collect()
            else:
                logger.info(f"White Image {name} already exists. Skipping.")

            db_entry = np.array(
                [(self.calibrationFolderPath / name,
                  self._serial_number,
                  self._get_focal_length(zoom_step),
                  zoom_step,
                  focus_step,
                  exposure,
                  iso,
                  paths_curr)],
                dtype=self._whiteImageDbDtype)
            self._whiteImageDb = np.append(self._whiteImageDb, db_entry)

        assert set(self._rawWhiteImageDb['path']) == \
               set([i for sublist in self._whiteImageDb['processed_paths_raw'] for i in sublist])
        logger.info("...done")

    def _get_wi_db_entry(self, path: Path) -> ndarray:
        """Get the database entry for a white image.
        Entries include the zoomStep and focusStep setting of
        the white image to be used for decoding.

        Args:
            path: Path to the white image, relative to Camera main folder.
                  Used as database identfication

            metadata: The metadata to the whiteimage

        Returns:
            A structured array containing the path, focal_length, zoomStep and
            focusStep setting of the white image.

        """
        img = self._get_wi(self.path / path, process=False, meta_only=True)
        metadata = img.meta

        # Metadata extraction for RAW files
        if 'master' in metadata.keys():
            metadata = metadata['master']['picture']['frameArray'][0]['frame']

        # Metadata extraction for LFR files
        zoom_step = metadata['metadata']['devices']['lens']['zoomStep']
        focus_step = metadata['metadata']['devices']['lens']['focusStep']
        serial_number = metadata['privateMetadata']['camera']['serialNumber']
        exposure_time = metadata['metadata']['devices']['shutter']['frameExposureDuration']
        try:
            iso = metadata['metadata']['image']['iso']
        # Lytro Illum calibration .RAW files do not contain iso...
        except KeyError:
            iso = 0

        focal_length = self._get_focal_length(zoom_step)

        # Create structured array for white image table
        db_entry = np.array(
            [(str(path), serial_number, focal_length, zoom_step, focus_step, exposure_time, iso)],
            dtype=self._rawWhiteImageDbDtype)

        return db_entry

    def _get_wi(self, path: Path, process: bool = False, meta_only: bool = False):
        """Read the white image from path and perform preprocessing such as
        contrast stretching, normalization, etc.

        Args:
            path: Path to the white image, relative to camera folder.

            process: Whether to perform preprocessing such as contras stretching.

        Returns:
            White image as float in range [0, 1].

        """
        path = self.path / path

        # Explicitly copy as returned value is read-only
        if path.suffix.lower() == ".npy":
            wi = np.load(self.path / path)
        else:
            if path.suffix.lower() == ".raw":
                frmt = self._format
            else:
                frmt = None
            try:
                wi = imageio.imread(self.path / path, format=frmt, meta_only=meta_only).copy()
            except TypeError:
                wi = imageio.imread(self.path / path, format=frmt).copy()

        if not meta_only:
            # Crop as specified
            wi = self._crop_raw(wi)

            if process:
                # Contrast stretch
                wi -= wi.min()
                wi /= wi.max()
                wi = np.clip(wi, 0, 1)

        return wi

    @staticmethod
    def _get_focal_length(zoom_step):
        """Calculate focal length in meter from zoom_step setting.

        Uses a cubic function obtained via least squares fit of data
        measured with a Lytro Illum Camera.
        """

        fit_func = lambda p, x: p[0] + p[1]*x + p[2]*x**2 + p[3]*x**3
        params = [5.12921535e+01, -6.27792215e-02,  6.85768795e-05, -5.18338520e-08]

        # fit_func was fitted in mm units, divide by 1000 to obtain meters
        return fit_func(params, zoom_step) / 1000

    @staticmethod
    def unique_geometry_exposure_gen(db, paths_processed):
        """Generator to yield unique zoom, focus, exposure and iso values from
        a raw database together with the correpsoning current database and paths.

        Args:
            db: Raw image database to process.
            paths_processed: Paths of raw images that have already been processed

        Yields:
            tmp_db, paths_curr, exposure, iso, focus_step, zoom_step

        """
        uniqe_focus_steps = list(set([i['focusStep'] for i in db]))
        unique_zoom_steps = list(set([i['zoomStep'] for i in db]))
        unique_isos = list(set([i['iso'] for i in db]))
        unique_exposures = list(set([i['exposure_time'] for i in db]))

        # Mapper for focus step values
        mapper = lambda x: max(set(x), key=x.count) if len(x) > 2 else np.min(x)

        # Get entries with (almost) identical zoom, (almost) identical focus and identical iso
        for zoom_step, focus_step, iso in product(unique_zoom_steps, uniqe_focus_steps, unique_isos):
            db_zoom_id = db[(db['zoomStep'] >= zoom_step - 3) & (db['zoomStep'] <= zoom_step + 3)]
            db_focus_id = db_zoom_id[
                (db_zoom_id['focusStep'] > focus_step - 50) & (db_zoom_id['focusStep'] < focus_step + 50)]
            db_iso_id = db_focus_id[db_focus_id['iso'] == iso]

            if len(db_iso_id) > 0 and mapper(db_iso_id['focusStep'].tolist()) == focus_step:
                for exposure in unique_exposures:
                    # Get images with same exposure times
                    tmp_db = db_iso_id[db_iso_id['exposure_time'] == exposure]

                    # Load images and average (if only one is found, mean does not do anything
                    paths_curr = [f['path'] for f in tmp_db if f['path'] not in paths_processed]
                    if len(paths_curr) > 0:
                        yield paths_curr, exposure, iso, focus_step, zoom_step

    @staticmethod
    def unique_exposure_gen(db, paths_processed):
        """Generator to yield unique exposure and iso values from a raw database
        together with the correpsoning current database and paths.

        Args:
            db: Raw image database to process.
            paths_processed: Paths of raw images that have already been processed

        Yields:
            tmp_db, paths_curr, exposure, iso
        """

        unique_isos = list(set([i['iso'] for i in db]))
        unique_exposures = list(set([i['exposure_time'] for i in db]))

        for iso, exposure in product(unique_isos, unique_exposures):
            tmp_db = db[db['iso'] == iso]
            tmp_db = tmp_db[tmp_db['exposure_time'] == exposure]

            if len(tmp_db) > 0:
                # Load images and average (if only one is found, mean does not do anything
                paths_curr = [f['path'] for f in tmp_db if f['path'] not in paths_processed]
                if len(paths_curr) > 0:
                    yield paths_curr, exposure, iso
