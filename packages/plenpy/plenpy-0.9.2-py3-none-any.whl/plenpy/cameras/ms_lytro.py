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
Module defining the :class:`MsLytro` camera class.

This camera class, derived from the :class:`AbstractLightFieldCamera` base
class, implements a prototype multispectral Lytro Illum camera.

"""
import gc
from itertools import product
import json
from pathlib import Path
from typing import Any
from typing import List
from typing import Optional
from typing import Tuple

import imageio
import numpy as np
from numpy.core import ndarray
from tqdm import tqdm

import torch
from torchvision.transforms import GaussianBlur

import plenpy.logg
from plenpy.cameras.lytro_illum import LytroIllum
from plenpy.lightfields import LightField
from plenpy.utilities.misc import get_avail_extensions

logger = plenpy.logg.get_logger()

__all__ = ['MsLytro']

# Use Lytro Illum lfr amd raw format from imageio plugins
imageio.formats.sort('lytro-illum-lfr')
imageio.formats.sort('lytro-illum-raw')


class MsLytro(LytroIllum):
    """Multispectral Lytro Illum light field camera.
    """

    def __init__(self, path: Any, num_channels: int = 13, format='LYTRO-ILLUM-RAW'):
        """
        Args:
            path: Folder path of camera.

            num_channels: Number of spectral channels.

            format: The ``imageio`` format of the white images.
                    Default: LYTRO-ILLUM-RAW.
        """
        # Call init from AbstractLightfieldCamera base class
        super().__init__(path, format)

        # Add image resolution
        shape = self._shape_original  # Inherited from original Lytro Illum class
        offset = (shape[1] - shape[0]) // 2
        self._crop_slice_x = slice(0, shape[0])
        self._crop_slice_y = slice(offset, offset+shape[0])
        self._validate_crop()

        # Add camera specific attributes
        self.blackImageFolderPath = self.calibrationFolderPath / "BlackImages"
        self.msWhiteImageFolderPath = self.calibrationFolderPath / "SpectralWhiteImages"
        self._num_channels = num_channels
        self._blackImageDb = None
        self._rawBlackImageDb = None
        self._msWhiteImageDb = None
        self._rawMsWhiteImageDb = None

        self._darkCurrentDb = None
        self._darkCurrentDbDtype = [('serial_number', 'U9999'),
                                    ('iso', 'i4'),
                                    ('dark_current', 'f8'),
                                    ('dark_offset', 'f8'),
                                    ('processed_paths_raw', object)]

        self._responsivityDb = None
        self._responsivityDbDtype = [('path_responsivity', 'U9999'),
                                     ('path_vignetting', 'U9999'),
                                     ('serial_number', 'U9999'),
                                     ('focal_length', 'f8'),
                                     ('zoomStep', 'i4'),
                                     ('focusStep', 'i4'),
                                     ('iso', 'i4'),
                                     ('processed_paths_raw', object)]

    def _save_cal_data(self, filename: Optional[str] = None):
        """Save the calibration data.

        The calibration data is saved as a compressed numpy array file
        in the camera's ``Calibration`` folder.

        """
        if filename is not None:
            filename = self.calibrationFolderPath / filename
            if not filename.suffix == ".npz":
                filename = filename.with_suffix('.npz')
            self._calDataFilename = filename

        logger.info(f"Saving calibration data to {self._calDataFilename}...")
        np.savez_compressed(self.path/self._calDataFilename,
                            calDB=self._calibrationDb,
                            darkCurrentDB=self._darkCurrentDb,
                            responsivityDB=self._responsivityDb,
                            wiDB=self._whiteImageDb,
                            rawWiDB=self._rawWhiteImageDb,
                            biDB=self._blackImageDb,
                            rawBiDB=self._rawBlackImageDb,
                            msWiDB=self._msWhiteImageDb,
                            rawMsWiDB=self._rawMsWhiteImageDb,
                            serialNumber=self._serial_number)
        logger.info("...done.")

        return

    def _load_cal_data(self, filename: Optional[Any] = None):
        """Load the calibration data from the calibration data file.

        Args:
            filename: Calibration data filename.
                Specify only if it deviates from the default value.

        """
        if filename is not None:
            filename = self.calibrationFolderPath / filename
            if not filename.suffix  == ".npz":
                filename = filename.with_suffix('.npz')
            self._calDataFilename = filename

        logger.info("Loading calibration data....")
        loaded = np.load(self.path / self._calDataFilename, allow_pickle=True)
        self._calibrationDb = loaded['calDB'] if not str(loaded['calDB']) == "None" else None
        self._darkCurrentDb = loaded['darkCurrentDB'] if not str(loaded['darkCurrentDB']) == "None" else None
        self._responsivityDb = loaded['responsivityDB'] if not str(loaded['responsivityDB']) == "None" else None
        self._whiteImageDb = loaded['wiDB'] if not str(loaded['wiDB']) == "None" else None
        self._rawWhiteImageDb = loaded['rawWiDB'] if not str(loaded['rawWiDB']) == "None" else None
        self._blackImageDb = loaded['biDB'] if not str(loaded['biDB']) == "None" else None
        self._rawBlackImageDb = loaded['rawBiDB'] if not str(loaded['rawBiDB']) == "None" else None
        self._msWhiteImageDb = loaded['msWiDB'] if not str(loaded['msWiDB']) == "None" else None
        self._rawMsWhiteImageDb = loaded['rawMsWiDB'] if not str(loaded['rawMsWiDB']) == "None" else None
        self._serial_number = str(loaded['serialNumber']) if not str(loaded['serialNumber']) == "None" else None
        logger.info("...done")

        return

    def _read_ms_raw(self, folder: Path,
                     dtype=np.float64,
                     multi_exposure=False,
                     meta_only=False) -> Tuple[ndarray, dict]:
        """Reads a single multispectral raw light field.
        All raw data must be contained in a single folder with
        alphanumerically sorted filenames according to the corresponding
        spectral channel index order.

        Checks data for consistency regarding the camera serial number,
        the ISO setting and the exposure time.

        Args:
            folder: Folder containing the raw measurements per channel.
                    The folder is searched recursively.

            dtype: Dtype used for loading.

            multi_exposure: Whether to allow multi-exposure series.

            meta_only: Whether to only read the metadata.

        Returns:
            Spectral raw data of shape (num_channels, x, y)
        """
        files = sorted(list(folder.glob("**/*.LFR")))

        # Check correct number of files
        if len(files) != self._num_channels:
            raise ValueError(f"Found {len(files)} images in {folder} but "
                             f"expected {self._num_channels}.")

        # Check that file list is not corrupt
        ids = [int(i.with_suffix("").name[4:]) for i in files]
        ids_ref = list(range(min(ids), max(ids) + 1))
        if len(set(ids_ref) - set(ids)) != 0:
            raise ValueError(f"Files invalid. Naming not in continuous numerical order. "
                             f"Found {[f.name for f in files]}.")

        # Read files and extract metadata
        raw_images = [self._crop_raw(imageio.imread(f, meta_only=meta_only, include_thumbnail=False)).astype(dtype) for f in files]
        raw_metadata = [im.meta for im in raw_images]

        serial_nums = set([m['privateMetadata']['camera']['serialNumber'] for m in raw_metadata])
        iso_nums = set([m['metadata']['image']['iso'] for m in raw_metadata])
        exposures = [m['metadata']['devices']['shutter']['frameExposureDuration'] for m in raw_metadata]
        zoom_steps = set([m['metadata']['devices']['lens']['zoomStep'] for m in raw_metadata])
        focus_steps = [m['metadata']['devices']['lens']['focusStep'] for m in raw_metadata]

        if len(serial_nums) != 1:
            raise ValueError("Found images from multiple cameras with serial  numbers {serial_nums}.")
        if len(iso_nums) != 1:
            raise ValueError(f"Found images multiple ISO settings {iso_nums}.")
        if not multi_exposure:
            exposures = set(exposures)
            if len(exposures) != 1:
                raise ValueError(f"Found images with multiple exposures {exposures}.")
        if len(zoom_steps) != 1:
            raise ValueError(f"Found images with multiple zoom settings {zoom_steps}.")

        focus_steps_median = np.median(focus_steps)
        min_dev = focus_steps_median - np.min(focus_steps)
        max_dev = np.max(focus_steps) - focus_steps_median
        if max(min_dev, max_dev) > 25.0:
            raise ValueError(f"Found too large focus deviations {focus_steps}.")

        # Find config file
        config_file = list(folder.glob("**/config.json"))
        if len(config_file) == 0:
            raise ValueError(f"Found no config file {config_file} for {folder}.")
        if len(config_file) != 1:
            raise ValueError(f"Found more than one config file {config_file} for {folder}.")

        with open(config_file[0]) as file:
            config = json.load(file)

        config['zoom_step'] = zoom_steps.pop()
        config['focus_step'] = int(focus_steps_median)
        config['serial_number'] = serial_nums.pop()
        if multi_exposure:
            config['exposures'] = exposures
        else:
            config['exposure_time'] = exposures.pop()
        config['iso'] = iso_nums.pop()

        metadata = dict(config=config, raw_metadata=raw_metadata)
        # Return numpy array of shape (num_ch, x, y) and metadata
        return np.asarray(raw_images, dtype=dtype), metadata

    def decode_image(self,
                     folder: str,
                     resample_method: str = 'guided'):
        """Decode a multispectral light field

        The decoding returns a
        :class:`.plenpy.lightfields.lightfield.LightField` object.

        Args:
            folder: Path to multispectral raw data folder.

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
        raw_img, metadata = self._get_ms_wi(self.path / self.imageFolderPath / folder,
                                            multi_exposure=True,
                                            return_meta=True)

        # Get the responsivity corresponding to current zoom, focus and iso setting
        zoomstep = metadata['config']['zoom_step']
        focusstep = metadata['config']['focus_step']
        exposures = np.asarray(metadata['config']['exposures'])
        iso = metadata['config']['iso']
        serial_number = metadata['config']['serial_number']
        if serial_number != self._serial_number:
            raise ValueError(f"Image's serial number {serial_number} not identical "
                             f"to camera's serial number {self._serial_number}.")

        # Dark current and offset
        tmp_db = self._darkCurrentDb[self._darkCurrentDb['iso'] == iso][0]
        dark_current = tmp_db['dark_current']
        dark_offset = tmp_db['dark_offset']

        # Get responsivities with same ISO
        tmp_db = self._responsivityDb[self._responsivityDb['iso'] == iso]

        # Find all responsivities with same/similar zoomStep
        diff_ = np.abs(tmp_db['zoomStep'] - (zoomstep))
        idx_ = np.argwhere(diff_ == diff_.min())

        # Now, find those with similar focus step
        if len(idx_) > 1:
            responsivity = self._responsivityDb[idx_]
            diff_ = np.abs(responsivity['focusStep'] - (focusstep))
            idx_select_ = np.argmin(diff_)
            idx_ = np.argwhere(tmp_db == responsivity[idx_select_])

        responsivity_select_idx = np.squeeze(idx_)

        # Load corresponding responsivity and vignetting
        responsivity = np.load(self.path / tmp_db[responsivity_select_idx]['path_responsivity'])
        vignetting = np.load(self.path / tmp_db[responsivity_select_idx]['path_vignetting'])

        # Calculate (y - y_0) / (r + alpha) / t_exp
        raw_img -= dark_offset

        for color_idx, color_mask in enumerate(get_bayer_mask(raw_img.shape[1:])):
            raw_img[:, color_mask] /= (responsivity[color_idx]*exposures)[:, np.newaxis] \
                                      * vignetting[np.newaxis, color_mask] \
                                      + dark_current*exposures[:, np.newaxis]

        del responsivity, vignetting, exposures
        gc.collect()

        # raw_img /= responsivity + dark_current
        # raw_img /= np.expand_dims(exposures, (1, 2))
        # del responsivity, exposures
        # gc.collect()

        # Bring to shape (x, y, lambda)
        raw_img = raw_img.transpose((1, 2, 0))

        raw_img[raw_img == np.inf] = 0
        raw_img[raw_img == -np.inf] = 0

        # Get all WI with same/similar zoomstep
        tmp_db = self._whiteImageDb
        diff_ = np.abs(tmp_db['zoomStep'] - (zoomstep))
        idx_ = np.argwhere(diff_ == diff_.min())

        # Now, find those with similar focus step
        if len(idx_) > 1:
            wi_select = tmp_db[idx_]
            diff_ = np.abs(wi_select['focusStep'] - (focusstep))
            idx_select_ = np.argmin(diff_)
            idx_ = np.argwhere(tmp_db == wi_select[idx_select_])

        wi_select_idx = np.squeeze(idx_)

        # Aligning the sensor image
        img = self._align_image(raw_img, wi_idx=wi_select_idx)
        del raw_img
        gc.collect()

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

        return lf

    def _process_wi_db(self, method):

        # Estimate dark current and offset from black images
        self._estimate_dark_current()

        # Estimate pixel-wise responsivity from spectral white images
        self._estimate_responsivity()

        # Calculate grid parameters and align transformation from regular white images
        self._est_grid(method=method)

        return

    def _create_wi_db(self):
        # Create regular white image database for microlens calibration
        super(MsLytro, self)._create_wi_db()

        # Create black image database
        self._create_bi_db()

        # Create multispectral white image database
        self._create_ms_wi_db()

    def _create_raw_bi_db(self):

        # Read all available images in Black Image folder
        black_image_paths = [f.relative_to(self.path) for f in (self.path/self.blackImageFolderPath).glob("**/*")
                             if f.suffix in get_avail_extensions()
                             and not f.suffix == '.npz']

        black_image_paths.sort()

        if self._rawBlackImageDb is None:
            # Create initial database with raw data
            self._rawBlackImageDb = np.squeeze(
                np.stack([self._get_wi_db_entry(path) for path in black_image_paths]))
        else:
            black_image_paths = set([str(i) for i in black_image_paths]) - set(self._rawBlackImageDb['path'].tolist())
            black_image_paths = [Path(i) for i in list(black_image_paths)]
            if len(black_image_paths) > 0:
                logger.info(f"Found {len(black_image_paths)} new raw black image(s). Updating database...")
                new_db_entries = np.squeeze(np.stack([self._get_wi_db_entry(path) for path in black_image_paths]),
                                            axis=-1)
                self._rawBlackImageDb = np.concatenate((self._rawBlackImageDb, new_db_entries))

        # If only one item is contained, extend dimension
        if self._rawBlackImageDb.ndim == 0:
            self._rawBlackImageDb = np.array([self._rawBlackImageDb])

        if self._serial_number is None:
            serial_number = set(self._rawBlackImageDb['serial_number'].tolist())
            if len(serial_number) != 1:
                raise ValueError(f"Found raw white images with more than one "
                                 f"serial number.\n {self._rawBlackImageDb}")
            self._serial_number = serial_number.pop()
        else:
            if np.any(self._rawBlackImageDb['serial_number'] != self._serial_number):
                raise ValueError(f"Found raw black images with incorrect serial "
                                 f"number. The camera serial number is {self._serial_number}. "
                                 f"Found:\n {self._rawBlackImageDb[np.where(self._rawBlackImageDb['serial_number'] != self._serial_number)]}")

    def _create_bi_db(self):
        logger.info(f"Creating black image database...")

        # Create raw white image database
        self._create_raw_bi_db()

        # Look up raw white images with (almost) identical zoom and focus
        # Average them
        if self._blackImageDb is None:
            # For first time creation, initialize
            self._blackImageDb = np.array([], dtype=self._whiteImageDbDtype)
            paths_processed = []
        else:
            paths_processed = [i for sublist in self._blackImageDb['processed_paths_raw'].tolist() for i in sublist]
            paths_processed = list(set(paths_processed))

        db = self._rawBlackImageDb

        for paths_curr, exposure, iso in self.unique_exposure_gen(db, paths_processed):

            name = f"black_image_iso_{iso}_exposure_{exposure}.npy"
            save_path = self.path / self.calibrationFolderPath / name
            if not save_path.exists():
                bi = np.mean([self._get_wi(self.path / f, process=False) for f in paths_curr],
                             axis=0,
                             dtype=np.float64)

                paths_processed += paths_curr #db_tmp['path'].tolist()

                # Save white image
                np.save(save_path, bi)
            else:
                logger.info(f"Black Image {name} already exists. Skipping.")

            db_entry = np.array(
                [(self.calibrationFolderPath / name,
                  self._serial_number,
                  -1,
                  -1,
                  -1,
                  exposure,
                  iso,
                  paths_curr)],
                dtype=self._whiteImageDbDtype)
            self._blackImageDb = np.append(self._blackImageDb, db_entry)

        assert set(self._rawBlackImageDb['path']) == \
               set([i for sublist in self._blackImageDb['processed_paths_raw'] for i in sublist])
        logger.info("...done")

    def _create_raw_ms_wi_db(self):

        # Add spectral white images
        # Read all available images in Spectral White Image folder
        # Get folder paths that contain at least one LFR file
        ms_white_image_paths = [f.relative_to(self.path) for f in (self.path/self.msWhiteImageFolderPath).glob("*/**")
                                if f.is_dir() and list(f.glob("*.LFR"))]

        ms_white_image_paths.sort()

        if self._rawMsWhiteImageDb is None:
            # Create initial database with raw data
            self._rawMsWhiteImageDb = np.squeeze(
                np.stack([self._get_ms_wi_db_entry(path) for path in ms_white_image_paths]))
        else:
            ms_white_image_paths = set([str(i) for i in ms_white_image_paths]) - set(self._rawMsWhiteImageDb['path'].tolist())
            ms_white_image_paths = [Path(i) for i in list(ms_white_image_paths)]
            if len(ms_white_image_paths) > 0:
                logger.info(f"Found {len(ms_white_image_paths)} new raw multispectral white image(s). Updating database...")
                new_db_entries = np.squeeze(np.stack([self._get_ms_wi_db_entry(path) for path in ms_white_image_paths]),
                                            axis=-1)
                self._rawMsWhiteImageDb = np.concatenate((self._rawMsWhiteImageDb, new_db_entries))

        # If only one item is contained, extend dimension
        if self._rawMsWhiteImageDb.ndim == 0:
            self._rawMsWhiteImageDb = np.array([self._rawMsWhiteImageDb])

        if self._serial_number is None:
            serial_number = set(self._rawMsWhiteImageDb['serial_number'].tolist())
            if len(serial_number) != 1:
                raise ValueError(f"Found raw white images with more than one "
                                 f"serial number.\n {self._rawMsWhiteImageDb}")
            self._serial_number = serial_number.pop()
        else:
            if np.any(self._rawMsWhiteImageDb['serial_number'] != self._serial_number):
                raise ValueError(f"Found raw multispectral white images with incorrect serial "
                                 f"number. The camera serial number is {self._serial_number}. "
                                 f"Found:\n {self._rawMsWhiteImageDb[np.where(self._rawMsWhiteImageDb['serial_number'] != self._serial_number)]}")

    def _create_ms_wi_db(self):
        """

        Returns:

        """
        logger.info("Creating multispectral white image database...")

        # Create raw multispectral white image database
        self._create_raw_ms_wi_db()

        # Look up raw multispectral white images with (almost) identical zoom and focus
        # identical iso and identical exposure time
        # Average them
        if self._msWhiteImageDb is None:
            # For first time creation, initialize
            self._msWhiteImageDb = np.array([], dtype=self._whiteImageDbDtype)
            paths_processed = []
        else:
            paths_processed = [i for sublist in self._msWhiteImageDb['processed_paths_raw'].tolist() for i in sublist]
            paths_processed = list(set(paths_processed))

        db = self._rawMsWhiteImageDb

        # Get entries with (almost) identical zoom, (almost) identical focus and identical iso
        n_wi_total = len(list(self.unique_geometry_exposure_gen(db, paths_processed)))
        for idx, (paths_curr, exposure, iso, focus_step, zoom_step) in \
                enumerate(self.unique_geometry_exposure_gen(db, paths_processed)):
            logger.info(f"Processing MS White Image {idx+1} of {n_wi_total}")

            name = f"spectral_white_image_zoomStep_{zoom_step}_focusStep_{focus_step}_iso_{iso}_exposure_{exposure}.npy"
            save_path = self.path/self.calibrationFolderPath/name
            if not save_path.exists():

                # Get identical ISO and exposure times
                N = len(paths_curr)
                f_init = paths_curr[0]
                _, meta = self._get_ms_wi(self.path / f_init, dtype=np.float32, return_meta=True, meta_only=True)
                ms_wi = np.zeros((N, self._num_channels, ) + self._shape_crop, dtype=np.float32)

                for i, f in enumerate(paths_curr):
                    logger.debug(f"Reading MS WI {i+1} of {len(paths_curr)}")
                    ms_wi[i] = self._get_ms_wi(self.path / f, dtype=np.float32)

                logger.debug("Calculation MS WI mean")
                ms_wi = np.mean(ms_wi, axis=0, dtype=np.float32)

                paths_processed += paths_curr

                # Save white image
                np.save(save_path, ms_wi)

                # Free memory
                del ms_wi
                gc.collect()

            else:
                logger.info(f"MS White Image {name} already exists. Skipping.")

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
            self._msWhiteImageDb = np.append(self._msWhiteImageDb, db_entry)

        # Double check that all raw white images have been processed
        assert set(self._rawMsWhiteImageDb['path']) == \
               set([i for sublist in self._msWhiteImageDb['processed_paths_raw'] for i in sublist])
        logger.info("...done")

    def _estimate_dark_current(self):

        logger.info("Estimating dark current from black images...")
        if self._darkCurrentDb is None:
            self._darkCurrentDb = np.array([], dtype=self._darkCurrentDbDtype)
            iso_processed = []
        else:
            iso_processed = list(set([i['iso'] for i in self._darkCurrentDb]))

        db = self._blackImageDb
        unique_isos = list(set([i['iso'] for i in db]))
        missing_isos = list(set(unique_isos) - set(iso_processed))
        unique_exposures = list(set([i['exposure_time'] for i in db]))
        logger.info(f"Found ISOs: {unique_isos}")
        if len(iso_processed) > 0:
            logger.info(f"Processed ISOs in Database: {iso_processed}")
        for iso in missing_isos:
            logger.info(f"Processing ISO {iso}")
            tmp_db = db[db['iso'] == iso]
            exposures = tmp_db['exposure_time']

            # Load image, use median filter to filter out salt&pepper-like noise
            ims = np.array([np.load(self.path/f) for f in tmp_db['path']])

            # Filter out 3sigma around median
            median = np.median(ims, axis=(1, 2))
            median_std = np.mean(ims - np.expand_dims(median, axis=(1, 2)), axis=(1, 2))
            interval = np.clip(3*median_std, a_min=1e-3, a_max=None)
            mask = np.logical_or(ims > np.expand_dims(median + interval, axis=(1, 2)),
                                 ims < np.expand_dims(median - interval, axis=(1, 2)))
            ims[mask] = np.nan

            # Calculate image-wise mean
            im_mean = np.nanmean(ims, axis=(1, 2))
            del ims

            # Linear fit of data
            N = len(exposures)
            t = exposures
            y = im_mean
            sum_y = np.sum(y)
            sum_t = np.sum(t)

            a = (N * np.sum(t * y) - sum_t * sum_y) / (N * np.sum(t*t) - sum_t**2)
            b = sum_y / N - a * sum_t / N

            db_entry = np.array(
                [(self._serial_number,
                  iso,
                  a,
                  b,
                  list(tmp_db['path']))],
                dtype=self._darkCurrentDbDtype)
            self._darkCurrentDb = np.append(self._darkCurrentDb, db_entry)
        logger.info("...done")

        return

    def _estimate_responsivity(self):

        logger.info("Estimating responsivity from spectral white images...")
        if self._responsivityDb is None:
            self._responsivityDb = np.array([], dtype=self._responsivityDbDtype)
            paths_processed = []
        else:
            paths_processed = [i for sublist in self._responsivityDb['processed_paths_raw'].tolist() for i in sublist]
            paths_processed = list(set(paths_processed))

        db = self._msWhiteImageDb
        n_wi_total = len(list(self.unique_ms_wi_gen(db, paths_processed)))
        for idx, (paths_curr, exposures, iso, focus_step, zoom_step) in enumerate(self.unique_ms_wi_gen(db, paths_processed)):
            logger.info(f"Processing spectral white image {idx+1} of {n_wi_total}")
            dark_offset = self._darkCurrentDb[self._darkCurrentDb['iso'] == iso]['dark_offset'][0]
            dark_current = self._darkCurrentDb[self._darkCurrentDb['iso'] == iso]['dark_current'][0]

            name_responsivity = f"responsivity_zoomStep_{zoom_step}_focusStep_{focus_step}_iso_{iso}.npy"
            save_path_responsivity = self.path / self.calibrationFolderPath / name_responsivity

            name_vignetting = f"vignetting_zoomStep_{zoom_step}_focusStep_{focus_step}_iso_{iso}.npy"
            save_path_vignetting = self.path / self.calibrationFolderPath / name_vignetting

            if (not save_path_responsivity.exists()) and (not save_path_vignetting.exists()):
                # Load images with read mmap, to not overload RAM
                ims = [np.load(self.path / f, mmap_mode='r') for f in paths_curr]
                # responsivity, offset = self.fit_linear_pixel_wise(ims,
                #                                                   exposures,
                #                                                   dark_current,
                #                                                   dark_offset)
                # vignetting = offset  # debug

                responsivity, vignetting = self.fit_linear_full(ims,
                                                                exposures,
                                                                dark_current,
                                                                dark_offset)

                np.save(save_path_responsivity, responsivity)
                np.save(save_path_vignetting, vignetting)

            else:
                logger.info(f"Responsivity {name_responsivity} and vignetting {name_vignetting} already exists. Skipping.")

            paths_processed += paths_curr
            db_entry = np.array(
                [(self.calibrationFolderPath / name_responsivity,
                  self.calibrationFolderPath/name_vignetting,
                  self._serial_number,
                  self._get_focal_length(zoom_step),
                  zoom_step,
                  focus_step,
                  iso,
                  paths_curr)],
                dtype=self._responsivityDbDtype)
            self._responsivityDb = np.append(self._responsivityDb, db_entry)

        return

    def _get_ms_wi_db_entry(self, folder: Path) -> ndarray:
        """Get the database entry for a white image.
        Entries include the zoomStep and focusStep setting of
        the white image to be used for decoding.

        Args:
            folder: Folder path containing the multispectral white image.


        Returns:
            A structured array containing the folder, focal_length, zoomStep and
            focusStep setting of the white image.

        """
        img, metadata = self._get_ms_wi(self.path / folder, process=False, return_meta=True, meta_only=True)
        focal_length = metadata['config']['zoom']
        zoom_step = metadata['config']['zoom_step']
        focus_step = metadata['config']['focus_step']
        serial_number = metadata['config']['serial_number']
        exposure_time = metadata['config']['exposure_time']
        iso = metadata['config']['iso']

        # Create structured array for white image table
        db_entry = np.array(
            [(str(folder), serial_number, focal_length, zoom_step, focus_step, exposure_time, iso)],
            dtype=self._rawWhiteImageDbDtype)

        return db_entry

    def _get_ms_wi(self,
                   folder: Path,
                   dtype=np.float64,
                   process: bool = False,
                   multi_exposure=False,
                   return_meta=False,
                   meta_only=False):
        """Read a multispectral white image from a folder and perform
        preprocessing such as contrast stretching, normalization, etc.

        Args:
            folder: Folder path to the multispectral white image,
                    relative to camera folder.

            dtype: Which dtype to convert to after loading. Defaults to float64.

            process: Whether to perform preprocessing such as contrast stretching.

            return_meta: Whether to return the metadata dict.

        Returns:
            Multispectral white image as ndarray and metadata.
        """
        path = self.path / folder

        ms_wi, metadata = self._read_ms_raw(path, dtype=dtype, multi_exposure=multi_exposure,meta_only=meta_only)

        if process:
            # Contrast stretch
            ms_wi -= ms_wi.min()
            try:
                ms_wi /= ms_wi[:, 2500:-2500, 3500:-3500].max()
            except ValueError or KeyError:
                ms_wi /= ms_wi.max()
            ms_wi = np.clip(ms_wi, 0, 1)

        if return_meta:
            return ms_wi, metadata
        else:
            return ms_wi

    @staticmethod
    def unique_ms_wi_gen(db, paths_processed):
        """Generator to yield unique zoom, focus, and iso values from
        the multispectral white image database together with the corresponding current database and paths.

        Args:
            db: Raw image database to process.
            paths_processed: Paths of raw images that have already been processed

        Yields:
            tmp_db, paths_curr, exposure, iso, focus_step, zoom_step

        """
        uniqe_focus_steps = list(set([i['focusStep'] for i in db]))
        unique_zoom_steps = list(set([i['zoomStep'] for i in db]))
        unique_isos = list(set([i['iso'] for i in db]))

        # Mapper for focus step values
        mapper = lambda x: max(set(x), key=x.count) if len(x) > 2 else np.min(x)

        # Get entries with (almost) identical zoom, (almost) identical focus and identical iso
        for zoom_step, focus_step, iso in product(unique_zoom_steps, uniqe_focus_steps, unique_isos):
            db_zoom_id = db[(db['zoomStep'] >= zoom_step - 3) & (db['zoomStep'] <= zoom_step + 3)]
            db_focus_id = db_zoom_id[
                (db_zoom_id['focusStep'] > focus_step - 50) & (db_zoom_id['focusStep'] < focus_step + 50)]
            tmp_db = db_focus_id[db_focus_id['iso'] == iso]

            if len(tmp_db) > 0 and mapper(tmp_db['focusStep'].tolist()) == focus_step:

                # Load images and average (if only one is found, mean does not do anything
                paths_curr = [f['path'] for f in tmp_db if f['path'] not in paths_processed]
                exposures = [f['exposure_time'] for f in tmp_db if f['path'] not in paths_processed].copy()
                if len(paths_curr) > 0:
                    yield paths_curr, exposures, iso, focus_step, zoom_step

    @staticmethod
    def fit_linear_pixel_wise(data: List[ndarray],
                              exposures: ndarray,
                              dark_current,
                              dark_offset,
                              **kwargs) -> Tuple[ndarray, ndarray]:
        """

        Args:
            data: List of Numpy arrays (possibly with 'r' memmap) of shape (x, y)
                  or (ch, x, y) with list length T.

            exposures: Numpy array with reference exposures of shape (T, ).

            method: Either "numpy" using CPU or "torch" using GPU acceleration.

            **kwargs:

        Returns:
            responsivity, offset

        """
        cpu = torch.device("cpu")
        gpu = torch.device("cuda:0")
        device = kwargs.get("device", cpu)
        dtype = kwargs.get("dtype", torch.float32)

        # Sort exposures
        sort_keys = np.argsort(exposures)
        exposures = np.sort(exposures)
        exposures = torch.tensor(exposures, dtype=dtype, device=device)

        shape = set([i.shape for i in data]).pop()
        responsivity = np.zeros(shape, dtype=np.float64)
        offset = np.zeros(shape, dtype=np.float64)

        # Patch into i*j patches without overlap
        # Need to be even
        i_max = 6
        j_max = 6
        if not np.array_equal([0, 0], np.mod([i_max, j_max], 2)):
            raise ValueError(f"Need an even number of patches per dimension, found {(i_max, j_max)}.")

        shape_patch = (shape[0],) + tuple(np.array(shape[1:], dtype=np.int) // np.array([i_max, j_max]))
        if not np.array_equal([0, 0], np.mod(shape_patch[1:], 2)):
            raise ValueError(f"Need an even shape patch, found {shape_patch[1:]}.")

        logger.info(f"Using {i_max*j_max} patches of shape {shape_patch}.")

        # Extract bayer mask
        x = torch.arange(shape_patch[1], device=cpu)
        y = torch.arange(shape_patch[2], device=cpu)
        x, y = torch.meshgrid(x, y)

        # FOR GRBG pattern
        R = torch.logical_and((torch.remainder(x, 2) == 0), (torch.remainder(y, 2) == 1))
        Gb = torch.logical_and((torch.remainder(x, 2) == 0), (torch.remainder(y, 2) == 0))
        Gr = torch.logical_and((torch.remainder(x, 2) == 1), (torch.remainder(y, 2) == 1))
        # G = Gb + Gr
        B = torch.logical_and((torch.remainder(x, 2) == 1), (torch.remainder(y, 2) == 0))

        # Iterate over patches
        EPS = 1e-11
        for i, j in product(range(i_max), range(j_max)):

            logger.info(f"Index {i*j_max + j + 1} of {i_max*j_max}")

            # Extract current patch slice
            x_slice = slice(i*shape_patch[1], (i + 1)*shape_patch[1])
            y_slice = slice(j*shape_patch[2], (j + 1)*shape_patch[2])

            # Extract measurement patch, stack in shape (ch, x, y, T)
            logger.info("Loading data...")
            img_patch = np.stack([data[i][..., x_slice, y_slice].copy() for i in sort_keys],
                                 axis=-1)

            img_patch = torch.tensor(img_patch, dtype=dtype, device=device)
            logger.info("done.")
            logger.info(f"Fitting...")

            # Mask out saturated pixels (over-exposure)
            mask_thres = 0.975
            mask = img_patch < mask_thres

            # Mask out neighboring pixels from saturation that lie in the same line
            # to eliminate electron overflow to neighboring pixels
            m_gr = torch.logical_and(mask[:, R, :], mask[:, Gr, :])
            m_gb = torch.logical_and(mask[:, B, :], mask[:, Gb, :])

            for amount in [1, 2]:
                ones_shape = torch.tensor(mask.shape)
                ones_shape[1] = amount
                ones_shape = ones_shape.tolist()
                tmp_mask_l = torch.cat((mask[:, amount:], torch.ones(ones_shape, device=device, dtype=torch.bool)), dim=1)
                tmp_mask_r = torch.cat((torch.ones(ones_shape, device=device, dtype=torch.bool), mask[:, :-amount]),  dim=1)
                for tmp_mask in [tmp_mask_l, tmp_mask_r]:
                    m_gr_tmp = torch.logical_and(tmp_mask[:, R, :], tmp_mask[:, Gr, :])
                    m_gr = torch.logical_and(m_gr, m_gr_tmp)

                    m_gb_tmp = torch.logical_and(tmp_mask[:, B, :], tmp_mask[:, Gb, :])
                    m_gb = torch.logical_and(m_gb, m_gb_tmp)

            mask[:, R, :] = m_gr
            mask[:, Gr, :] = m_gr
            mask[:, Gb, :] = m_gb
            mask[:, B, :] = m_gb

            oversaturation = torch.sum(~mask, dim=(1,2))
            oversaturation = oversaturation > 0.33*shape_patch[1] * shape_patch[2]
            mask.permute(0, -1, 1, 2)[oversaturation, :, :] = False

            # Weight low exposure less since they are logarithmically more densely sampled
            weights = 0.1*10.**(0.1*torch.arange(0, 10, dtype=torch.float32, device=device))
            weights = torch.cat((weights, torch.ones(len(exposures) - 10, device=device)))
            mask = mask * weights.view((1, 1, 1, -1))  # converts int->float
            # Fit model y = a*t+b with weights w
            t = exposures
            y = img_patch
            w = mask

            w_sum = torch.sum(w, dim=-1)
            w_y = w*y

            w_y_sum = torch.sum(w_y, dim=-1)
            w_t_sum = torch.sum(w*t, dim=-1)

            a = torch.div(w_sum * torch.sum(w_y * t, dim=-1) - w_y_sum * w_t_sum,
                          w_sum * torch.sum(w * torch.square(t), dim=-1) - torch.square(w_t_sum) + EPS)

            b = torch.div((w_y_sum - a * w_t_sum), w_sum + EPS)

            responsivity[:, x_slice, y_slice] = a.detach().cpu().numpy()
            offset[:, x_slice, y_slice] = b.detach().cpu().numpy()

        # Smooth responsivity for RGB pixels separately
        # Extract bayer mask
        # x = torch.arange(shape[1])
        # y = torch.arange(shape[2])
        # x, y = torch.meshgrid(x, y)

        # # FOR GRBG pattern
        # R = torch.logical_and((torch.remainder(x, 2) == 0), (torch.remainder(y, 2) == 1))
        # Gb = torch.logical_and((torch.remainder(x, 2) == 0), (torch.remainder(y, 2) == 0))
        # Gr = torch.logical_and((torch.remainder(x, 2) == 1), (torch.remainder(y, 2) == 1))
        # # G = Gb + Gr
        # B = torch.logical_and((torch.remainder(x, 2) == 1), (torch.remainder(y, 2) == 0))

        # # Perform RGB pixel-wise smoothing
        # rgb_shape = (shape_patch[0], shape_patch[1]//2, shape_patch[2]//2)
        # for m in [R, Gr, Gb, B]:
        #     for tmp in [responsivity, offset]:
        #         tmp_smooth = tmp[:, m].reshape(rgb_shape)
        #         blur = GaussianBlur(3, 1.0)
        #         tmp_smooth = blur(tmp_smooth)
        #         tmp[:, m] = tmp_smooth.reshape(tmp[:, m].shape)

        logger.info(f"Done.")
        return responsivity, offset

    @staticmethod
    def fit_linear_full(data: List[ndarray],
                        exposures: ndarray,
                        dark_current,
                        dark_offset,
                        epochs=2000,
                        learning_rate=1e-2,
                        **kwargs) -> Tuple[ndarray, ndarray]:
        """

        Args:
            data: List of Numpy arrays (possibly with 'r' memmap) of shape (x, y)
                  or (ch, x, y) with list length T.

            exposures: Numpy array with reference exposures of shape (T, ).

            method: Either "numpy" using CPU or "torch" using GPU acceleration.

            **kwargs:

        Returns:
            responsivity, offset

        """
        cpu = torch.device("cpu")
        gpu = torch.device("cuda:0")
        device = kwargs.get("device", gpu)
        dtype = kwargs.get("dtype", torch.float32)

        def get_mask(img_patch, shape_patch):
            # Mask out saturated pixels (over-exposure)
            mask_thres = 0.985
            mask = img_patch < mask_thres

            # Mask out neighboring pixels from saturation that lie in the same line
            # to eliminate electron overflow to neighboring pixels
            R, Gr, Gb, B = color_masks
            m_gr = torch.logical_and(mask[:, R, :], mask[:, Gr, :])
            m_gb = torch.logical_and(mask[:, B, :], mask[:, Gb, :])

            # Neighbors along line in wich CCD is read out
            for amount in [2, 3]:
                ones_shape = torch.tensor(mask.shape)
                ones_shape[1] = amount
                ones_shape = ones_shape.tolist()
                tmp_mask_l = torch.cat((mask[:, amount:], torch.ones(ones_shape, device=cpu, dtype=torch.bool)),
                                       dim=1)
                tmp_mask_r = torch.cat((torch.ones(ones_shape, device=cpu, dtype=torch.bool), mask[:, :-amount]),
                                       dim=1)

                for tmp_mask in [tmp_mask_l, tmp_mask_r]:
                    m_gr_tmp = torch.logical_and(tmp_mask[:, R, :], tmp_mask[:, Gr, :])
                    m_gr = torch.logical_and(m_gr, m_gr_tmp)

                    m_gb_tmp = torch.logical_and(tmp_mask[:, B, :], tmp_mask[:, Gb, :])
                    m_gb = torch.logical_and(m_gb, m_gb_tmp)

            mask_cp = mask.clone()
            mask[:, R, :] = m_gr
            mask[:, Gr, :] = m_gr
            mask[:, Gb, :] = m_gb
            mask[:, B, :] = m_gb

            # Direct neighbors (non-diagonally and diagonally)
            mask_l = torch.logical_and(mask[:, :, 1:, :], mask[:, :, :-1, :])
            mask_r = torch.logical_and(mask[:, 1:, :, :], mask[:, :-1, :, :])
            mask[:, :-1, :-1, :] = torch.logical_and(mask_l[:, :-1, :, :], mask_r[:, :, :-1, :])

            oversaturation = torch.sum(~mask, dim=(1, 2))
            oversaturation = oversaturation > 0.33*shape_patch[1]*shape_patch[2]
            mask.permute(0, -1, 1, 2)[oversaturation, :, :] = False

            # Weight low exposure less since they are logarithmically more densely sampled
            weights = 0.1*10.**(0.1*torch.arange(0, 10, dtype=dtype, device=cpu))
            weights = torch.cat((weights, torch.ones(len(exposures) - 10, device=cpu)))
            return mask*weights.view((1, 1, 1, -1))  # converts int->float

        def get_slices(i, j, shape_patch, patch_offset):
            # Extract current patch slice
            x_slice = slice(i*patch_offset[0], i*patch_offset[0]+shape_patch[1])
            y_slice = slice(j*patch_offset[1], j*patch_offset[1]+shape_patch[2])
            return x_slice, y_slice

        def estimate_patch(x_slice,
                           y_slice,
                           responsivity_init=None,
                           min_loss_init=None):

            # Extract measurement patch, stack in shape (ch, x, y, T)
            logger.info("Loading data...")
            img_patch = np.stack([data[i][..., x_slice, y_slice].copy() for i in sort_keys],
                                 axis=-1)

            img_patch = torch.tensor(img_patch, dtype=dtype, device=cpu)
            logger.info("done.")

            logger.info("Masking out saturated pixels...")
            mask = get_mask(img_patch, shape_patch)

            logger.info("done.")
            logger.info(f"Fitting...")

            # Normalize data
            # y_kijl - dark_offset - dark_current * t_l = vignetting_ij * responsivity_k * t_l
            # Where (i,j) -> spatial, (k) -> spectral, (l) -> temporal dimension
            img_patch = img_patch - dark_offset - dark_current * exposures.view(1, 1, 1, -1)

            # Init result
            vignetting_patch = torch.zeros(shape_patch[1:], device=cpu, dtype=dtype)
            responsivity_patch = torch.zeros((len(color_masks), ) + (shape_patch[0], ), device=cpu, dtype=dtype)

            logger.info("Fitting vignetting and responsivity...")
            train_loss = torch.zeros(len(color_masks), epochs, device=cpu, dtype=dtype)
            if min_loss_init is None:
                min_loss = 1e-5
            else:
                min_loss = min_loss_init

            for color_idx, color_mask in enumerate(color_masks):
                logger.info(f"Fitting color channel {color_idx + 1} of {len(color_masks)}.")

                t = exposures.to(device)
                y_gt = img_patch[:, color_mask, :].to(device)
                w = mask[:, color_mask, :].to(device)

                # Init weights
                weight_kwargs = dict(requires_grad=True, device=device, dtype=dtype)
                # Transform: responsivity = exp2(r_weights),   0 <responsivitiy
                # Transform: vignetting = sigmoid(v_weights), 0 < vignetting < 1
                if responsivity_init is None:
                    r_weights = torch.zeros(y_gt.shape[0], **weight_kwargs)
                else:
                    with torch.no_grad():
                        r_weights = torch.log2(responsivity_init[color_idx]).clone().to(device)
                        r_weights.requires_grad_()

                v_weights = torch.zeros(y_gt.shape[1], **weight_kwargs)

                # Init optimizer and train
                # For optimization with initialization, use smaller LR for responsivity
                # as it should already be very close to the optimum, only the vignetting should change significantly
                if responsivity_init is not None:
                    optimizer = torch.optim.Adam([
                        {'params': [r_weights], 'lr': 0.05*learning_rate},
                        {'params': [v_weights], 'lr': 1.25*learning_rate}
                    ])
                else:
                    optimizer = torch.optim.Adam([r_weights, v_weights], lr=learning_rate)

                loss = 100.00
                epoch = 0

                with tqdm(total=epochs, postfix=f" Loss: {loss}") as t_bar:
                    while loss > min_loss and epoch < epochs:

                        # Reset gradients
                        optimizer.zero_grad()

                        # Forward pass
                        y_pred = torch.einsum('k,i,l->kil', torch.exp2(r_weights), torch.sigmoid(v_weights), t)

                        # Weighted Least Squares loss function
                        # L = sum_ijkl w_ijkl * (y_pred_ijkl - y_gt_ijkl)^2
                        loss = torch.div(
                            torch.sum(
                                torch.multiply(
                                    torch.square(torch.subtract(y_gt, y_pred)),
                                    w)),
                            w.numel())

                        # Backwards pass
                        loss.backward()

                        # Parameter update
                        optimizer.step()

                        # Append loss
                        train_loss[color_idx, epoch] = loss.detach().cpu()

                        # Update TQDM bar
                        t_bar.postfix = f" Loss: {train_loss[color_idx, epoch]}"
                        t_bar.update()

                        # Update epoch
                        epoch += 1

                vignetting_patch[color_mask] = torch.sigmoid(v_weights).detach().cpu()
                responsivity_patch[color_idx] = torch.exp2(r_weights).detach().cpu()

            return responsivity_patch, vignetting_patch, torch.min(train_loss)

        # Sort exposures
        sort_keys = np.argsort(exposures)
        exposures = np.sort(exposures)
        exposures = torch.tensor(exposures, dtype=dtype, device=cpu)

        shape = set([i.shape for i in data]).pop()

        # Patch into i*j patches
        # i_max, j_max = 7, 7
        i_max, j_max = 21, 21

        i_central, j_central = i_max//2, j_max//2

        shape_patch = (shape[0],) + tuple(np.array(shape[1:])//(1 + np.array([i_max, j_max])//2))
        if not np.array_equal([0, 0], np.mod(np.array(shape[1:]), (1 + np.array([i_max, j_max])//2))):
            raise ValueError(f"Specified number of patches is not a true divider of input shape. "
                             f"Resulting shape would be {(shape[0],) + tuple(np.array(shape[1:])/(1 + np.array([i_max, j_max])//2))}")
        if not np.array_equal([0, 0], np.mod(shape_patch[1:], 2)):
            raise ValueError(f"Need an even shape patch, found {shape_patch[1:]}.")

        patch_offset = tuple(np.asarray(shape_patch[1:])//2)
        logger.info(f"Using {i_max*j_max} patches of shape {shape_patch}.")

        # Use Gr and Gb channel separately, can be changed however
        color_masks = [torch.tensor(m) for m in get_bayer_mask(shape_patch[1:3])]

        # Init result and counter mask for overlap
        # Responsivity of shape (lambda) for RGrGbB pixels separately
        responsivity = torch.zeros((i_max*j_max, len(color_masks)) + (shape[0],), dtype=torch.float64, device=cpu)
        # Vignetting of shape (x, y)
        vignetting = torch.zeros(shape[1:], dtype=torch.float64, device=cpu)
        overlap_mask = torch.zeros(shape[1:], dtype=torch.uint8, device=cpu)

        # Get initial estimate from central patch
        logger.info("Estimating initial responsivity and vignetting from central patch...")
        x_slice_central, y_slice_central = get_slices(i_central, j_central, shape_patch, patch_offset)
        responsivity_init, vignetting_init, min_loss_init = estimate_patch(x_slice_central, y_slice_central)
        logger.info("done.")

        # Iterate over patches
        for patch_idx, (i, j) in enumerate(product(range(i_max), range(j_max))):

            logger.info(f"Index {i*j_max + j + 1} of {i_max*j_max}")
            x_slice, y_slice = get_slices(i, j, shape_patch, patch_offset)
            responsivity_patch, vignetting_patch, _ = estimate_patch(x_slice, y_slice,
                                                                     responsivity_init=responsivity_init,
                                                                     min_loss_init=1.1*min_loss_init)

            vignetting[x_slice, y_slice] += vignetting_patch
            overlap_mask[x_slice, y_slice] += 1
            responsivity[patch_idx] = responsivity_patch

        # Average estimates
        responsivity = torch.mean(responsivity, dim=0).numpy()
        vignetting = vignetting / overlap_mask

        # Smooth vignetting slightly
        blur = GaussianBlur((3, 3), sigma=0.75)
        vignetting = blur(vignetting.unsqueeze(0)).squeeze().numpy()

        logger.info(f"Done.")
        return responsivity, vignetting


def get_bayer_mask(shape: tuple, num_channels: int = 4):
    """Creates the Bayer mask of the Lytro Illum camera (layout GRBG)

    Args:
        shape: Spatial shape of the mask.
        num_channels: Number of channels to return.
                      When 3, return RGB masks.
                      When 4, returns RGrGbB masks.

    Returns:
        [R, G, B] mask if num_channels == 3,
        [R, Gr, Gb, B] masks if num_channels == 4.

    """
    if not len(shape) == 2:
        raise ValueError(f"Need to specify a 2D shape. Found {shape}.")
    if not (num_channels == 3 or num_channels == 4):
        raise ValueError(f"Need to specify 3 or 4 channels. Found {num_channels}.")

    # Extract bayer mask
    x = np.arange(shape[0])
    y = np.arange(shape[1])
    x, y = np.meshgrid(x, y)
    x = x.T
    y = y.T

    # FOR GRBG pattern
    R = np.logical_and((np.mod(x, 2) == 0), (np.mod(y, 2) == 1))
    Gb = np.logical_and((np.mod(x, 2) == 0), (np.mod(y, 2) == 0))
    Gr = np.logical_and((np.mod(x, 2) == 1), (np.mod(y, 2) == 1))
    B = np.logical_and((np.mod(x, 2) == 1), (np.mod(y, 2) == 0))

    if num_channels == 3:
        G = Gb + Gr
        return [R, G, B]
    else:
        return [R, Gr, Gb, B]
