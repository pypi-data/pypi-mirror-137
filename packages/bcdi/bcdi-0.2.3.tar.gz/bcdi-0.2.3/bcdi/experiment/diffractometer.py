# -*- coding: utf-8 -*-

# BCDI: tools for pre(post)-processing Bragg coherent X-ray diffraction imaging data
#   (c) 07/2017-06/2019 : CNRS UMR 7344 IM2NP
#   (c) 07/2019-05/2021 : DESY PHOTON SCIENCE
#       authors:
#         Jerome Carnis, carnis_jerome@yahoo.fr

"""
Beamline-dependent diffractometer classes.

These classes follow the same structure as beamline classes. It would have been
possible to put all the beamline-dependent code in a single child class per beamline,
but the class would have been huge and more difficult to maintain. The class methods
manage the extraction of motors/counters position, data loading (which can be thought
just as another counter), data preprocessing (normalization by monitor, flatfield,
hotpixels removal, background subtraction), and the rotation of the sample so that all
sample circles are at 0 degrees. Generic method are implemented in the abstract base
class Diffractometer, and beamline-dependent methods need to be implemented in each
child class (they are decoracted by @abstractmethod in the base class, they are
indicated using @ in the following diagram). These classes are not meant to be
instantiated directly but via a Setup instance.

.. mermaid::
  :align: center

  classDiagram
    class Diffractometer{
      +tuple sample_offsets
      +tuple sample_circles
      +tuple detector_circles
      goniometer_values(@)
      load_data(@)
      motor_positions(@)
      read_device(@)
      read_monitor(@)
      add_circle()
      flatten_sample()
      get_circles()
      get_rocking_circle()
      init_data_mask()
      init_monitor()
      load_check_dataset()
      load_frame()
      remove_circle()
      rotation_matrix()
      select_frames()
      valid_name()
  }
    ABC <|-- Diffractometer

API Reference
-------------

"""

try:
    import hdf5plugin  # for P10, should be imported before h5py or PyTables
except ModuleNotFoundError:
    pass

from abc import ABC, abstractmethod
import fabio
from functools import reduce
import h5py
from matplotlib import pyplot as plt
from numbers import Integral, Number, Real
import numpy as np
import os
import re
import sys
import tkinter as tk
from tkinter import filedialog
from typing import List, Optional

from ..graph import graph_utils as gu
from .rotation_matrix import RotationMatrix
from ..utils import utilities as util
from ..utils import validation as valid


def check_empty_frames(data, mask=None, monitor=None, frames_logical=None):
    """
    Check if there is intensity for all frames.

    In case of beam dump, some frames may be empty. The data and optional mask will be
    cropped to remove those empty frames.

    :param data: a numpy 3D array
    :param mask: a numpy 3D array of 0 (pixel not masked) and 1 (masked pixel),
     same shape as data
    :param monitor: a numpy 1D array of shape equal to data.shape[0]
    :param frames_logical: 1D array of length equal to the number of measured frames.
     In case of cropping the length of the stack of frames changes. A frame whose
     index is set to 1 means that it is used, 0 means not used.
    :return:
     - cropped data as a numpy 3D array
     - cropped mask as a numpy 3D array
     - cropped monitor as a numpy 1D array
     - updated frames_logical

    """
    valid.valid_ndarray(arrays=data, ndim=3)
    if mask is not None:
        valid.valid_ndarray(arrays=mask, shape=data.shape)
    if monitor is not None:
        if not isinstance(monitor, np.ndarray):
            raise TypeError("monitor should be a numpy array")
        if monitor.ndim != 1 or len(monitor) != data.shape[0]:
            raise ValueError("monitor be a 1D array of length data.shae[0]")

    if frames_logical is None:
        frames_logical = np.ones(data.shape[0])
    valid.valid_1d_array(
        frames_logical,
        allowed_types=Integral,
        allow_none=False,
        allowed_values=(0, 1),
        name="frames_logical",
    )

    # check if there are empty frames
    is_intensity = np.zeros(data.shape[0])
    is_intensity[np.argwhere(data.sum(axis=(1, 2)))] = 1
    if is_intensity.sum() != data.shape[0]:
        print("\nEmpty frame detected, cropping the data\n")

    # update frames_logical
    frames_logical = np.multiply(frames_logical, is_intensity)

    # remove empty frames from the data and update the mask and the monitor
    data = data[np.nonzero(frames_logical)]
    mask = mask[np.nonzero(frames_logical)]
    monitor = monitor[np.nonzero(frames_logical)]
    return data, mask, monitor, frames_logical


def check_pixels(data, mask, debugging=False):
    """
    Check for hot pixels in the data using the mean value and the variance.

    :param data: 3D diffraction data
    :param mask: 2D or 3D mask. Mask will summed along the first axis if a 3D array.
    :param debugging: set to True to see plots
    :type debugging: bool
    :return: the filtered 3D data and the updated 2D mask.
    """
    valid.valid_ndarray(arrays=data, ndim=3)
    valid.valid_ndarray(arrays=mask, ndim=(2, 3))
    nbz, nby, nbx = data.shape

    if mask.ndim == 3:  # 3D array
        print("Mask is a 3D array, summing it along axis 0")
        mask = mask.sum(axis=0)
        mask[np.nonzero(mask)] = 1
    valid.valid_ndarray(arrays=mask, shape=(nby, nbx))

    print(
        "\ncheck_pixels(): number of masked pixels due to detector gaps ="
        f" {int(mask.sum())} on a total of {nbx*nby}"
    )
    meandata = data.mean(axis=0)  # 2D
    vardata = 1 / data.var(axis=0)  # 2D
    var_mean = vardata[vardata != np.inf].mean()
    vardata[meandata == 0] = var_mean
    # pixels were data=0 (i.e. 1/variance=inf) are set to the mean of  1/var:
    # we do not want to mask pixels where there was no intensity during the scan

    if debugging:
        gu.combined_plots(
            tuple_array=(mask, meandata, vardata),
            tuple_sum_frames=False,
            tuple_sum_axis=0,
            tuple_width_v=None,
            tuple_width_h=None,
            tuple_colorbar=True,
            tuple_vmin=0,
            tuple_vmax=(1, 1, np.nan),
            tuple_scale=("linear", "linear", "linear"),
            tuple_title=(
                "Input mask",
                "check_pixels()\nmean(data) before masking",
                "check_pixels()\n1/var(data) before masking",
            ),
            reciprocal_space=True,
            position=(131, 132, 133),
        )

    # calculate the mean and variance of a single photon event along the rocking curve
    min_count = 0.99  # pixels with only 1 photon count along the rocking curve,
    # use the value 0.99 to be inclusive
    mean_singlephoton = min_count / nbz
    var_singlephoton = (
        ((nbz - 1) * mean_singlephoton ** 2 + (min_count - mean_singlephoton) ** 2)
        * 1
        / nbz
    )
    print(
        "check_pixels(): var_mean={:.2f}, 1/var_threshold={:.2f}".format(
            var_mean, 1 / var_singlephoton
        )
    )

    # mask hotpixels with zero variance
    temp_mask = np.zeros((nby, nbx))
    temp_mask[vardata == np.inf] = 1
    # this includes only hotpixels since zero intensity pixels were set to var_mean
    mask[np.nonzero(temp_mask)] = 1  # update the mask with zero variance hotpixels
    vardata[vardata == np.inf] = 0  # update the array
    print(
        "check_pixels(): number of zero variance hotpixels = {:d}".format(
            int(temp_mask.sum())
        )
    )

    # filter out pixels which have a variance smaller that the threshold
    # (note that  vardata = 1/data.var())
    indices_badpixels = np.nonzero(vardata > 1 / var_singlephoton)
    mask[indices_badpixels] = 1  # mask is 2D
    print(
        "check_pixels(): number of pixels with too low variance = {:d}\n".format(
            indices_badpixels[0].shape[0]
        )
    )

    # update the data array
    indices_badpixels = np.nonzero(mask)  # update indices
    for index in range(nbz):
        tempdata = data[index, :, :]
        tempdata[
            indices_badpixels
        ] = 0  # numpy array is mutable hence data will be modified

    if debugging:
        meandata = data.mean(axis=0)
        vardata = 1 / data.var(axis=0)
        vardata[meandata == 0] = var_mean  # 0 intensity pixels, not masked
        gu.combined_plots(
            tuple_array=(mask, meandata, vardata),
            tuple_sum_frames=False,
            tuple_sum_axis=0,
            tuple_width_v=None,
            tuple_width_h=None,
            tuple_colorbar=True,
            tuple_vmin=0,
            tuple_vmax=(1, 1, np.nan),
            tuple_scale="linear",
            tuple_title=(
                "Output mask",
                "check_pixels()\nmean(data) after masking",
                "check_pixels()\n1/var(data) after masking",
            ),
            reciprocal_space=True,
            position=(131, 132, 133),
        )
    return data, mask


def create_diffractometer(beamline, sample_offsets):
    """
    Create a Diffractometer instance depending on the beamline.

    :param beamline: str, name of the beamline
    :param sample_offsets: list or tuple of angles in degrees, corresponding to
     the offsets of each of the sample circles (the offset for the most outer circle
     should be at index 0). The number of circles is beamline dependent. Convention:
     the sample offsets will be subtracted to measurement the motor values.
    :return:  the corresponding diffractometer instance
    """
    if beamline == "ID01":
        return DiffractometerID01(sample_offsets)
    if beamline in {"SIXS_2018", "SIXS_2019"}:
        return DiffractometerSIXS(sample_offsets)
    if beamline == "34ID":
        return Diffractometer34ID(sample_offsets)
    if beamline == "P10":
        return DiffractometerP10(sample_offsets)
    if beamline == "P10_SAXS":
        return DiffractometerP10SAXS()
    if beamline == "CRISTAL":
        return DiffractometerCRISTAL(sample_offsets)
    if beamline == "NANOMAX":
        return DiffractometerNANOMAX(sample_offsets)
    raise NotImplementedError(
        f"No diffractometer implemented for the beamline {beamline}"
    )


def load_filtered_data(detector):
    """
    Load a filtered dataset and the corresponding mask.

    :param detector: an instance of the class Detector
    :return: the data and the mask array
    """
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        initialdir=detector.datadir,
        title="Select data file",
        filetypes=[("NPZ", "*.npz")],
    )
    data = np.load(file_path)
    npz_key = data.files
    data = data[npz_key[0]]
    file_path = filedialog.askopenfilename(
        initialdir=detector.datadir,
        title="Select mask file",
        filetypes=[("NPZ", "*.npz")],
    )
    mask = np.load(file_path)
    npz_key = mask.files
    mask = mask[npz_key[0]]

    monitor = np.ones(data.shape[0])
    frames_logical = np.ones(data.shape[0])

    return data, mask, monitor, frames_logical


def normalize_dataset(array, monitor, savedir=None, norm_to_min=True, debugging=False):
    """
    Normalize array using the monitor values.

    :param array: the 3D array to be normalized
    :param monitor: the monitor values
    :param savedir: path where to save the debugging figure
    :param norm_to_min: bool, True to normalize to min(monitor) instead of max(monitor),
     avoid multiplying the noise
    :param debugging: bool, True to see plots
    :return:

     - normalized dataset
     - updated monitor
     - a title for plotting

    """
    valid.valid_ndarray(arrays=array, ndim=3)
    ndim = array.ndim
    nbz, nby, nbx = array.shape
    original_max = None
    original_data = None

    if ndim != 3:
        raise ValueError("Array should be 3D")

    if debugging:
        original_data = np.copy(array)
        original_max = original_data.max()
        original_data[original_data < 5] = 0  # remove the background
        original_data = original_data.sum(
            axis=1
        )  # the first axis is the normalization axis

    print(
        "Monitor min, max, mean: {:.1f}, {:.1f}, {:.1f}".format(
            monitor.min(), monitor.max(), monitor.mean()
        )
    )

    if norm_to_min:
        print("Data normalization by monitor.min()/monitor\n")
        monitor = monitor.min() / monitor  # will divide higher intensities
    else:  # norm to max
        print("Data normalization by monitor.max()/monitor\n")
        monitor = monitor.max() / monitor  # will multiply lower intensities

    nbz = array.shape[0]
    if len(monitor) != nbz:
        raise ValueError(
            "The frame number and the monitor data length are different:",
            f"got {nbz} frames but {len(monitor)} monitor values",
        )

    for idx in range(nbz):
        array[idx, :, :] = array[idx, :, :] * monitor[idx]

    if debugging:
        norm_data = np.copy(array)
        # rescale norm_data to original_data for easier comparison
        norm_data = norm_data * original_max / norm_data.max()
        norm_data[norm_data < 5] = 0  # remove the background
        norm_data = norm_data.sum(axis=1)  # the first axis is the normalization axis
        fig = gu.combined_plots(
            tuple_array=(monitor, original_data, norm_data),
            tuple_sum_frames=False,
            tuple_colorbar=False,
            tuple_vmin=(np.nan, 0, 0),
            tuple_vmax=np.nan,
            tuple_title=(
                "monitor.min() / monitor",
                "Before norm (thres. 5)",
                "After norm (thres. 5)",
            ),
            tuple_scale=("linear", "log", "log"),
            xlabel=("Frame number", "Detector X", "Detector X"),
            is_orthogonal=False,
            ylabel=("Counts (a.u.)", "Frame number", "Frame number"),
            position=(211, 223, 224),
            reciprocal_space=True,
        )
        if savedir is not None:
            fig.savefig(savedir + f"monitor_{nbz}_{nby}_{nbx}.png")
        plt.close(fig)

    return array, monitor


class Diffractometer(ABC):
    """
    Base class for defining diffractometers.

    The frame used is the laboratory frame with the CXI convention (z downstream,
    y vertical up, x outboard).

    :param sample_offsets: list or tuple of angles in degrees, corresponding to
     the offsets of each of the sample circles (the offset for the most outer circle
     should be at index 0). The number of circles is beamline dependent. Convention:
     the sample offsets will be subtracted to measurement the motor values.
    :param sample_circles: list of sample circles from outer to inner (e.g. mu eta
     chi phi), expressed using a valid pattern within {'x+', 'x-', 'y+', 'y-', 'z+',
     'z-'}. For example: ['y+' ,'x-', 'z-', 'y+']
    :param detector_circles: list of detector circles from outer to inner
     (e.g. gamma delta), expressed using a valid pattern within {'x+', 'x-', 'y+',
     'y-', 'z+', 'z-'}. For example: ['y+', 'x-']
    :param kwargs:
     - 'default_offsets': tuple, default sample offsets of the diffractometer. It needs
       to be implemented as a class attribute in the child class if necessary. See an
       example in DiffractometerP10

    """

    valid_circles = {
        "x+",
        "x-",
        "y+",
        "y-",
        "z+",
        "z-",
    }  # + counter-clockwise, - clockwise
    valid_names = {"sample": "_sample_circles", "detector": "_detector_circles"}

    def __init__(
        self,
        sample_offsets,
        sample_circles=(),
        detector_circles=(),
        **kwargs,
    ):
        self.sample_angles = None
        self.sample_circles = sample_circles
        self.detector_angles = None
        self.detector_circles = detector_circles
        if sample_offsets is None:
            sample_offsets = kwargs.get("default_offsets")
        self.sample_offsets = sample_offsets

    @property
    def detector_angles(self):
        """Tuple of goniometer angular values for the detector stages."""
        return self._detector_angles

    @detector_angles.setter
    def detector_angles(self, value):
        valid.valid_container(
            value,
            container_types=tuple,
            item_types=(Real, np.ndarray),
            allow_none=True,
            name="detector_angles",
        )
        self._detector_angles = value

    @property
    def detector_circles(self):
        """
        List of detector circles.

        The circles should be listed from outer to inner (e.g. gamma delta), expressed
        using a valid pattern within {'x+', 'x-', 'y+', 'y-', 'z+', 'z-'}. For
        example: ['y+' ,'x-', 'z-', 'y+']. Convention: CXI convention (z downstream,
        y vertical up, x outboard), + for a counter-clockwise rotation, - for a
        clockwise rotation.
        """
        return self._detector_circles

    @detector_circles.setter
    def detector_circles(self, value):
        valid.valid_container(
            value,
            container_types=(tuple, list),
            min_length=0,
            item_types=str,
            name="Diffractometer.detector_circles",
        )
        if any(val not in self.valid_circles for val in value):
            raise ValueError(
                "Invalid circle value encountered in detector_circles,"
                f" valid are {self.valid_circles}"
            )
        self._detector_circles = list(value)

    @property
    def sample_angles(self):
        """Tuple of goniometer angular values for the sample stages."""
        return self._sample_angles

    @sample_angles.setter
    def sample_angles(self, value):
        valid.valid_container(
            value,
            container_types=tuple,
            item_types=(Real, np.ndarray),
            allow_none=True,
            name="sample_angles",
        )
        self._sample_angles = value

    @property
    def sample_circles(self):
        """
        List of sample circles.

        The sample circles should be listed from outer to inner (e.g. mu eta chi phi),
        expressed using a valid pattern within {'x+', 'x-', 'y+', 'y-', 'z+', 'z-'}. For
        example: ['y+' ,'x-', 'z-', 'y+']. Convention: CXI convention (z downstream,
        y vertical up, x outboard), + for a counter-clockwise rotation, - for a
        clockwise rotation.
        """
        return self._sample_circles

    @sample_circles.setter
    def sample_circles(self, value):
        valid.valid_container(
            value,
            container_types=(tuple, list),
            min_length=0,
            item_types=str,
            name="Diffractometer.sample_circles",
        )
        if any(val not in self.valid_circles for val in value):
            raise ValueError(
                "Invalid circle value encountered in sample_circles,"
                f" valid are {self.valid_circles}"
            )
        self._sample_circles = list(value)

    @property
    def sample_offsets(self):
        """
        List or tuple of sample angular offsets in degrees.

        These angles correspond to the offsets of each f the sample circles (the
        offset for the most outer circle should be at index 0). Convention: the
        sample offsets will be subtracted to measurement the motor values.
        """
        return self._sample_offsets

    @sample_offsets.setter
    def sample_offsets(self, value):
        nb_circles = len(self.__getattribute__(self.valid_names["sample"]))
        if value is None:
            value = (0,) * nb_circles
        valid.valid_container(
            value,
            container_types=(tuple, list, np.ndarray),
            length=nb_circles,
            item_types=Real,
            name="Diffractometer.sample_offsets",
        )
        self._sample_offsets = value

    def add_circle(self, stage_name, index, circle):
        """
        Add a circle to the list of circles.

        The most outer circle should be at index 0.

        :param stage_name: supported stage name, 'sample' or 'detector'
        :param index: index where to put the circle in the list
        :param circle: valid circle in {'x+', 'x-', 'y+', 'y-', 'z+', 'z-'}.
         + for a counter-clockwise rotation, - for a clockwise rotation.
        """
        self.valid_name(stage_name)
        nb_circles = len(self.__getattribute__(self.valid_names[stage_name]))
        valid.valid_item(
            index,
            allowed_types=int,
            min_included=0,
            max_included=nb_circles,
            name="index",
        )
        if circle not in self.valid_circles:
            raise ValueError(
                f"{circle} is not in the list of valid circles:"
                f" {list(self.valid_circles)}"
            )
        self.__getattribute__(self.valid_names[stage_name]).insert(index, circle)

    def flatten_sample(
        self,
        arrays,
        voxel_size,
        q_com,
        rocking_angle,
        central_angle=None,
        fill_value=0,
        is_orthogonal=True,
        reciprocal_space=False,
        debugging=False,
        **kwargs,
    ):
        """
        Send all sample circles to zero degrees.

        Arrays are rotatedsuch that all circles of the sample stage are at their zero
        position.

        :param arrays: tuple of 3D real arrays of the same shape.
        :param voxel_size: tuple, voxel size of the 3D array in z, y, and x
         (CXI convention)
        :param q_com: diffusion vector of the center of mass of the Bragg peak,
         expressed in an orthonormal frame x y z
        :param rocking_angle: angle which is tilted during the rocking curve in
         {'outofplane', 'inplane'}
        :param central_angle: if provided, angle to be used in the calculation
         of the rotation matrix for the rocking angle. If None, it will be defined as
         the angle value at the middle of the rocking curve.
        :param fill_value: tuple of numeric values used in the RegularGridInterpolator
         for points outside of the interpolation domain. The length of the tuple
         should be equal to the number of input arrays.
        :param is_orthogonal: set to True is the frame is orthogonal, False otherwise.
         Used for plot labels.
        :param reciprocal_space: True if the data is in reciprocal space,
         False otherwise. Used for plot labels.
        :param debugging: tuple of booleans of the same length as the number
         of input arrays, True to see plots before and after rotation
        :param kwargs:

         - 'title': tuple of strings, titles for the debugging plots, same length as
           the number of arrays
         - 'scale': tuple of strings (either 'linear' or 'log'), scale for the
           debugging plots, same length as the number of arrays
         - width_z: size of the area to plot in z (axis 0), centered on the middle
           of the initial array
         - width_y: size of the area to plot in y (axis 1), centered on the middle
           of the initial array
         - width_x: size of the area to plot in x (axis 2), centered on the middle
           of the initial array

        :return: a rotated array (if a single array was provided) or a tuple of
         rotated arrays (same length as the number of input arrays)
        """
        valid.valid_ndarray(arrays, ndim=3)

        # check few parameters, the rest will be validated in rotate_crystal
        valid.valid_container(
            q_com,
            container_types=(tuple, list, np.ndarray),
            length=3,
            item_types=Real,
            name="q_com",
        )
        if np.linalg.norm(q_com) == 0:
            raise ValueError("the norm of q_com is zero")
        if self.sample_angles is None:
            raise ValueError(
                "call diffractometer.goniometer_values before calling this method"
            )
        valid.valid_item(
            central_angle, allowed_types=Real, allow_none=True, name="central_angle"
        )
        # find the index of the circle which corresponds to the rocking angle
        angles = self.sample_angles
        rocking_circle = self.get_rocking_circle(
            rocking_angle=rocking_angle, stage_name="sample", angles=angles
        )

        # get the relevant angle within the rocking circle.
        # The reference point when orthogonalizing if the center of the array,
        # but we do not know to which angle it corresponds if the data was cropped.
        if central_angle is None:
            print(
                "central_angle=None, using the angle at half of the rocking curve"
                " for the calculation of the rotation matrix"
            )
            nb_steps = len(angles[rocking_circle])
            central_angle = angles[rocking_circle][int(nb_steps // 2)]

        # use this angle in the calculation of the rotation matrix
        angles = list(angles)
        angles[rocking_circle] = central_angle
        print(
            f"sample stage circles: {self._sample_circles}\n"
            f"sample stage angles:  {angles}"
        )

        # check that all angles are Real, not encapsulated in a list or an array
        for idx, angle in enumerate(angles):
            if not isinstance(angle, Real):  # list/tuple or ndarray, cannot be None
                if len(angle) != 1:
                    raise ValueError(
                        "A list of angles was provided instead of a single value"
                    )
                angles[idx] = angle[0]

        # calculate the rotation matrix
        rotation_matrix = self.rotation_matrix(stage_name="sample", angles=angles)

        # rotate the arrays
        rotated_arrays = util.rotate_crystal(
            arrays=arrays,
            rotation_matrix=rotation_matrix,
            voxel_size=voxel_size,
            fill_value=fill_value,
            debugging=debugging,
            is_orthogonal=is_orthogonal,
            reciprocal_space=reciprocal_space,
            **kwargs,
        )
        rotated_q = util.rotate_vector(
            vectors=q_com, rotation_matrix=np.linalg.inv(rotation_matrix)
        )
        return rotated_arrays, rotated_q

    def get_circles(self, stage_name):
        """
        Return the list of circles for the stage.

        :param stage_name: supported stage name, 'sample' or 'detector'
        """
        self.valid_name(stage_name)
        return self.__getattribute__(self.valid_names[stage_name])

    def get_rocking_circle(self, rocking_angle, stage_name, angles):
        """
        Find the index of the circle which corresponds to the rocking angle.

        :param rocking_angle: angle which is tilted during the rocking curve in
         {'outofplane', 'inplane'}
        :param stage_name: supported stage name, 'sample' or 'detector'
        :param angles: tuple of angular values in degrees, one for each circle
         of the sample stage
        :return: the index of the rocking circles in the list of angles
        """
        # check parameters
        if rocking_angle not in {"outofplane", "inplane"}:
            raise ValueError(
                f"Invalid value {rocking_angle} for rocking_angle,"
                f' should be either "inplane" or "outofplane"'
            )
        self.valid_name(stage_name)
        valid.valid_container(angles, container_types=(tuple, list), name="angles")
        nb_circles = len(angles)

        # find which angles were scanned
        candidate_circles = set()
        for idx in range(nb_circles):
            if not isinstance(angles[idx], Real) and len(angles[idx]) > 1:
                # not a number, hence a tuple/list/ndarray (cannot be None)
                candidate_circles.add(idx)

        # exclude arrays with identical values
        wrong_motors = []
        for idx in candidate_circles:
            if (
                angles[idx][1:] - angles[idx][:-1]
            ).mean() < 0.0001:  # motor not scanned, noise in the position readings
                wrong_motors.append(idx)
        candidate_circles.difference_update(wrong_motors)

        # check that there is only one candidate remaining
        if len(candidate_circles) > 1:
            raise ValueError("Several circles were identified as scanned motors")
        if len(candidate_circles) == 0:
            raise ValueError("No circle was identified as scanned motor")
        index_circle = next(iter(candidate_circles))

        # check that the rotation axis corresponds to the one definec by rocking_angle
        circles = self.__getattribute__(self.valid_names[stage_name])
        if rocking_angle == "inplane":
            if circles[index_circle][0] != "y":
                raise ValueError(
                    f"The identified circle '{circles[index_circle]}' is incompatible "
                    f"with the parameter '{rocking_angle}'"
                )
        else:  # 'outofplane'
            if circles[index_circle][0] != "x":
                raise ValueError(
                    f"The identified circle '{circles[index_circle]}' is incompatible "
                    f"with the parameter '{rocking_angle}'"
                )
        return index_circle

    @abstractmethod
    def goniometer_values(self, setup, **kwargs):
        """
        Retrieve goniometer values.

        This method is beamline dependent. It must be implemented in the child classes.

        :param setup: the experimental setup: Class Setup
        :param kwargs: beamline_specific parameters
        :return: a tuple of angular values in degrees (rocking angular step, grazing
         incidence angles, inplane detector angle, outofplane detector angle). The
         grazing incidence angles are the positions of circles below the rocking circle.
        """

    def init_data_mask(
        self,
        detector,
        setup,
        normalize,
        nb_frames,
        bin_during_loading,
        **kwargs,
    ):
        """
        Initialize data, mask and region of interest for loading a dataset.

        :param detector: an instance of the class Detector
        :param setup: an instance of the class Setup
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param nb_frames: number of data points (not including series at each point)
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory space for large 2D detectors.
        :param kwargs:

         - 'scan_number': int, the scan number to load

        :return:

         - the empty 3D data array
         - the 2D mask array initialized with 0 values
         - the initialized monitor as a 1D array
         - the region of interest use for loading the data, as a list of 4 integers

        """
        # define the loading ROI, the user-defined ROI may be larger than the physical
        # detector size
        if (
            detector.roi[0] < 0
            or detector.roi[1] > detector.unbinned_pixel_number[0]
            or detector.roi[2] < 0
            or detector.roi[3] > detector.unbinned_pixel_number[1]
        ):
            print(
                "Data shape is limited by detector size,"
                " loaded data will be smaller than as defined by the ROI."
            )
        loading_roi = [
            max(0, detector.roi[0]),
            min(detector.unbinned_pixel_number[0], detector.roi[1]),
            max(0, detector.roi[2]),
            min(detector.unbinned_pixel_number[1], detector.roi[3]),
        ]

        # initialize the data array, the mask is binned afterwards in load_check_dataset
        if bin_during_loading:
            print(
                "Binning the data: detector vertical axis by",
                detector.binning[1],
                ", detector horizontal axis by",
                detector.binning[2],
            )
            data = np.empty(
                (
                    nb_frames,
                    (loading_roi[1] - loading_roi[0]) // detector.binning[1],
                    (loading_roi[3] - loading_roi[2]) // detector.binning[2],
                ),
                dtype=float,
            )
        else:
            data = np.empty(
                (
                    nb_frames,
                    loading_roi[1] - loading_roi[0],
                    loading_roi[3] - loading_roi[2],
                ),
                dtype=float,
            )

        # initialize the monitor
        monitor = self.init_monitor(
            normalize=normalize,
            nb_frames=nb_frames,
            setup=setup,
            **kwargs,
        )

        return (
            data,
            np.zeros(detector.unbinned_pixel_number),
            monitor,
            loading_roi,
        )

    def init_monitor(self, normalize, nb_frames, setup, **kwargs):
        """
        Initialize the monitor for normalization.

        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param nb_frames: number of data points (not including series at each point)
        :param setup: an instance of the class Setup
        :param kwargs:

         - 'scan_number': int, the scan number to load

        :return: the initialized monitor as a 1D array
        """
        monitor = None
        if normalize == "sum_roi":
            monitor = np.zeros(nb_frames)
        elif normalize == "monitor":
            if setup.custom_scan:
                monitor = setup.custom_monitor
            else:
                monitor = self.read_monitor(setup=setup, **kwargs)
        if monitor is None:
            monitor = np.ones(nb_frames)
            print("Skipping intensity normalization.")
        return monitor

    def load_check_dataset(
        self,
        scan_number,
        detector,
        setup,
        frames_pattern=None,
        flatfield=None,
        hotpixels=None,
        background=None,
        normalize="skip",
        bin_during_loading=False,
        debugging=False,
    ):
        """
        Load data, apply filters and concatenate it for phasing.

        :param scan_number: the scan number to load
        :param detector: an instance of the class Detector
        :param setup: an instance of the class Setup
        :param frames_pattern: 1D array of int, of length data.shape[0]. If
         frames_pattern is 0 at index, the frame at data[index] will be skipped,
         if 1 the frame will added to the stack.
        :param flatfield: the 2D flatfield array
        :param hotpixels: the 2D hotpixels array. 1 for a hotpixel, 0 for normal pixels.
        :param background: the 2D background array to subtract to the data
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory for large detectors.
        :param debugging: set to True to see plots
        :return:

         - the 3D data array in the detector frame and the 3D mask array
         - the monitor values for normalization
         - frames_logical: 1D array of length equal to the number of measured frames.
           In case of cropping the length of the stack of frames changes. A frame whose
           index is set to 1 means that it is used, 0 means not used.

        """
        print(
            "User-defined ROI size (VxH):",
            detector.roi[1] - detector.roi[0],
            detector.roi[3] - detector.roi[2],
        )
        print(
            "Detector physical size without binning (VxH):",
            detector.unbinned_pixel_number[0],
            detector.unbinned_pixel_number[1],
        )
        print(
            "Detector size with binning (VxH):",
            detector.unbinned_pixel_number[0] // detector.binning[1],
            detector.unbinned_pixel_number[1] // detector.binning[2],
        )

        if setup.filtered_data:
            data, mask3d, monitor, frames_logical = load_filtered_data(
                detector=detector
            )
        else:
            data, mask2d, monitor, loading_roi = self.load_data(
                setup=setup,
                scan_number=scan_number,
                detector=detector,
                flatfield=flatfield,
                hotpixels=hotpixels,
                background=background,
                normalize=normalize,
                bin_during_loading=bin_during_loading,
                debugging=debugging,
            )

            print("")

            ###################
            # update the mask #
            ###################
            mask2d = mask2d[
                loading_roi[0] : loading_roi[1], loading_roi[2] : loading_roi[3]
            ]
            if bin_during_loading:
                mask2d = util.bin_data(
                    mask2d,
                    (detector.binning[1], detector.binning[2]),
                    debugging=debugging,
                )
            mask2d[np.nonzero(mask2d)] = 1

            #################
            # select frames #
            #################
            data, frames_logical = self.select_frames(
                data=data, frames_pattern=frames_pattern
            )

            #################################
            # crop the monitor if necessary #
            #################################
            monitor = util.apply_logical_array(
                arrays=monitor, frames_logical=frames_logical
            )

            ########################################
            # check for abnormally behaving pixels #
            ########################################
            data, mask2d = check_pixels(data=data, mask=mask2d, debugging=debugging)
            mask3d = np.repeat(mask2d[np.newaxis, :, :], data.shape[0], axis=0)
            mask3d[np.isnan(data)] = 1
            data[np.isnan(data)] = 0

            ####################################
            # check for empty frames (no beam) #
            ####################################
            data, mask3d, monitor, frames_logical = check_empty_frames(
                data=data, mask=mask3d, monitor=monitor, frames_logical=frames_logical
            )

            ###########################
            # intensity normalization #
            ###########################
            if normalize == "skip":
                print("Skip intensity normalization")
            else:
                print("Intensity normalization using " + normalize)
                data, monitor = normalize_dataset(
                    array=data,
                    monitor=monitor,
                    norm_to_min=True,
                    savedir=detector.savedir,
                    debugging=debugging,
                )

            ##########################################################################
            # check for negative pixels, it can happen when subtracting a background #
            ##########################################################################
            print((data < 0).sum(), " negative data points masked")
            mask3d[data < 0] = 1
            data[data < 0] = 0

        return data, mask3d, monitor, frames_logical.astype(int)

    @abstractmethod
    def load_data(
        self,
        detector,
        setup,
        flatfield=None,
        hotpixels=None,
        background=None,
        normalize="skip",
        bin_during_loading=False,
        debugging=False,
        **kwargs,
    ):
        """
        Load data including detector/background corrections.

        :param detector: an instance of the class Detector
        :param setup: an instance of the class Setup
        :param flatfield: the 2D flatfield array
        :param hotpixels: the 2D hotpixels array
        :param background: the 2D background array to subtract to the data
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory space for large 2D detectors.
        :param debugging: set to True to see plots

        :param kwargs: beamline_specific parameters, which may include part of the
         totality of the following keys:

          - 'scan_number': the scan number to load (e.g. for ID01)

        :return: in this order

         - the 3D data array in the detector frame
         - the 2D mask array
         - the monitor values for normalization as a 1D array of length data.shape[0]
         - frames_logical as a 1D array of length the original number of 2D frames, 0 if
           a frame was removed, 1 if it wasn't. It can be used later to crop goniometer
           motor values accordingly.

        """

    @staticmethod
    def load_frame(
        frame,
        mask2d,
        monitor,
        frames_per_point,
        detector,
        loading_roi,
        flatfield=None,
        background=None,
        hotpixels=None,
        normalize="skip",
        bin_during_loading=False,
        debugging=False,
    ):
        """
        Load a frame and apply correction to it.

        :param frame: the frame to be loaded
        :param mask2d: a numpy array of the same shape as frame
        :param monitor: the volue of the intensity monitor for this frame
        :param frames_per_point: number of images summed to yield the 2D data
         (e.g. in a series measurement), used when defining the threshold for hot pixels
        :param detector: an instance of the class Detector
        :param loading_roi: user-defined region of interest, it may be larger than the
         physical size of the detector
        :param flatfield: the 2D flatfield array
        :param hotpixels: the 2D hotpixels array
        :param background: the 2D background array to subtract to the data
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory space for large 2D detectors.
        :param debugging: set to True to see plots
        :return:
        """
        frame, mask2d = detector.mask_detector(
            frame,
            mask2d,
            nb_frames=frames_per_point,
            flatfield=flatfield,
            background=background,
            hotpixels=hotpixels,
        )

        if normalize == "sum_roi":
            monitor = util.sum_roi(array=frame, roi=detector.sum_roi)

        frame = frame[loading_roi[0] : loading_roi[1], loading_roi[2] : loading_roi[3]]

        if bin_during_loading:
            frame = util.bin_data(
                frame,
                (detector.binning[1], detector.binning[2]),
                debugging=debugging,
            )

        return frame, mask2d, monitor

    @abstractmethod
    def motor_positions(self, setup, **kwargs):
        """
        Retrieve motor positions.

        This method is beamline dependent. It must be implemented in the child classes.

        :param setup: an instance of the class Setup
        :param kwargs: beamline_specific parameters, see the documentation for the
         child class.
        :return: the diffractometer motors positions for the particular setup. The
         energy (1D array or number) and the sample to detector distance are expected to
         be the last elements of the tuple in this order.
        """

    @staticmethod
    @abstractmethod
    def read_device(logfile, device_name, **kwargs):
        """
        Extract the scanned device positions/values.

        :param logfile: the logfile created in Setup.create_logfile()
        :param device_name: name of the scanned device
        :param kwargs: beamline_specific parameters, which may include part of the
         totality of the following keys:

          - 'scan_number': int, number of the scan (e.g. for ID01)

        :return: the positions/values of the device as a numpy 1D array
        """

    @staticmethod
    @abstractmethod
    def read_monitor(setup, **kwargs):
        """
        Load the default monitor for intensity normalization of the considered beamline.

        :param setup: an instance of the class Setup
        :param kwargs: beamline_specific parameter

          - 'scan_number': int, number of the scan (e.g. for ID01)

        :return: the default monitor values
        """

    def remove_circle(self, stage_name, index):
        """
        Remove the circle at index from the list of sample circles.

        :param stage_name: supported stage name, 'sample' or 'detector'
        :param index: index of the circle to be removed from the list
        """
        if stage_name not in self.valid_names:
            raise NotImplementedError(
                f"'{stage_name}' is not implemented,"
                f" available are {list(self.valid_names.keys())}"
            )
        nb_circles = len(self.__getattribute__(self.valid_names[stage_name]))
        if nb_circles > 0:
            valid.valid_item(
                index,
                allowed_types=int,
                min_included=0,
                max_included=nb_circles - 1,
                name="index",
            )
            del self.__getattribute__(self.valid_names[stage_name])[index]

    def rotation_matrix(self, stage_name, angles):
        """
        Calculate a 3D rotation matrix given rotation axes and angles.

        :param stage_name: supported stage name, 'sample' or 'detector'
        :param angles: list of angular values in degrees for the stage circles
         during the measurement
        :return: the rotation matrix as a numpy ndarray of shape (3, 3)
        """
        self.valid_name(stage_name)
        nb_circles = len(self.__getattribute__(self.valid_names[stage_name]))
        if isinstance(angles, Number):
            angles = (angles,)
        valid.valid_container(
            angles,
            container_types=(list, tuple, np.ndarray),
            length=nb_circles,
            item_types=Real,
            name="angles",
        )

        # create a list of rotation matrices corresponding to the circles,
        # index 0 corresponds to the most outer circle
        rotation_matrices = [
            RotationMatrix(circle, angles[idx]).get_matrix()
            for idx, circle in enumerate(
                self.__getattribute__(self.valid_names[stage_name])
            )
        ]

        # calculate the total tranformation matrix by rotating back
        # from outer circles to inner circles
        return np.array(reduce(np.matmul, rotation_matrices))

    @staticmethod
    def select_frames(data, frames_pattern=None):
        """
        Select frames, update the monitor and create a logical array.

        Override this method in the child classes of you want to implement a particular
        behavior, for example if two frames were taken at a same motor position and you
        want to delete one or average them...

        :param data: a 3D data array
        :param frames_pattern: 1D array of int, of length data.shape[0]. If
         frames_pattern is 0 at index, the frame at data[index] will be skipped,
         if 1 the frame will added to the stack.
        :return:
         - the updated 3D data, eventually cropped along the first axis
         - a 1D array of length the original number of 2D frames, 0 if a frame was
           removed, 1 if it wasn't. It can be used later to crop goniometer motor values
           accordingly.

        """
        if frames_pattern is None:
            frames_pattern = np.ones(data.shape[0], dtype=int)
        valid.valid_1d_array(
            frames_pattern,
            length=data.shape[0],
            allow_none=True,
            allowed_types=Integral,
            allowed_values=(0, 1),
            name="frames_pattern",
        )
        return data[frames_pattern != 0], frames_pattern

    def valid_name(self, stage_name):
        """
        Check if the stage is defined.

        :param stage_name: supported stage name, 'sample' or 'detector'
        """
        if stage_name not in self.valid_names:
            raise NotImplementedError(
                f"'{stage_name}' is not implemented,"
                f" available are {list(self.valid_names.keys())}"
            )


class DiffractometerCRISTAL(Diffractometer):
    """
    Define CRISTAL goniometer: 2 sample circles + 2 detector circles.

    The laboratory frame uses the CXI convention (z downstream, y vertical up,
    x outboard).

    - sample: mgomega, mgphi
    - detector: gamma, delta.

    """

    sample_rotations = ["x-", "y+"]
    detector_rotations = ["y+", "x-"]

    def __init__(self, sample_offsets):
        super().__init__(
            sample_circles=self.sample_rotations,
            detector_circles=self.detector_rotations,
            sample_offsets=sample_offsets,
        )

    @staticmethod
    def find_detector(
        logfile,
        actuators,
        root,
        detector_shape,
        data_path="scan_data",
        pattern="^data_[0-9][0-9]$",
    ):
        """
        Look for the entry corresponding to the detector data in CRISTAL dataset.

        :param logfile: the logfile created in Setup.create_logfile()
        :param actuators: dictionary defining the entries corresponding to actuators
        :param root: root folder name in the data file
        :param detector_shape: tuple or list of two integer (nb_pixels_vertical,
         nb_pixels_horizontal)
        :param data_path: string, name of the subfolder when the scan data is located
        :param pattern: string, pattern corresponding to the entries where the detector
         data could be located
        :return: numpy array of the shape of the detector dataset
        """
        # check input arguments
        valid.valid_container(
            root, container_types=str, min_length=1, name="cristal_find_data"
        )
        if not root.startswith("/"):
            root = "/" + root
        valid.valid_container(
            detector_shape,
            container_types=(tuple, list),
            item_types=int,
            length=2,
            name="cristal_find_data",
        )
        valid.valid_container(
            data_path, container_types=str, min_length=1, name="cristal_find_data"
        )
        if not data_path.startswith("/"):
            data_path = "/" + data_path
        valid.valid_container(
            pattern, container_types=str, min_length=1, name="cristal_find_data"
        )

        if "detector" in actuators:
            return logfile[root + data_path + "/" + actuators["detector"]][:]

        # loop over the available keys at the defined path in the file
        # and check the shape of the corresponding dataset
        nb_pix_ver, nb_pix_hor = detector_shape
        for key in list(logfile[root + data_path]):
            if bool(re.match(pattern, key)):
                obj_shape = logfile[root + data_path + "/" + key][:].shape
                if nb_pix_ver in obj_shape and nb_pix_hor in obj_shape:
                    # founc the key corresponding to the detector
                    print(
                        f"subdirectory '{key}' contains the detector images,"
                        f" shape={obj_shape}"
                    )
                    return logfile[root + data_path + "/" + key][:]
        raise ValueError(
            f"Could not find detector data using data_path={data_path} "
            f"and pattern={pattern}"
        )

    def goniometer_values(self, setup, **kwargs):
        """
        Retrieve goniometer motor positions for a BCDI rocking scan.

        :param setup: the experimental setup: Class Setup
        :return: a tuple of angular values in degrees (rocking angular step, grazing
         incidence angles, inplane detector angle, outofplane detector angle). The
         grazing incidence angles are the positions of circles below the rocking circle.
        """
        # load the motor positions
        (
            mgomega,
            mgphi,
            inplane_angle,
            outofplane_angle,
            energy,
            detector_distance,
        ) = self.motor_positions(setup=setup)

        # define the circles of interest for BCDI
        if setup.rocking_angle == "outofplane":  # mgomega rocking curve
            grazing = None  # nothing below mgomega at CRISTAL
            tilt_angle = mgomega
        elif setup.rocking_angle == "inplane":  # phi rocking curve
            grazing = (mgomega[0],)
            tilt_angle = mgphi
        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')

        setup.check_setup(
            grazing_angle=grazing,
            inplane_angle=inplane_angle,
            outofplane_angle=outofplane_angle,
            tilt_angle=tilt_angle,
            detector_distance=detector_distance,
            energy=energy,
        )

        # CRISTAL goniometer, 2S+2D (sample: mgomega, mgphi / detector: gamma, delta)
        self.sample_angles = (mgomega, mgphi)
        self.detector_angles = (inplane_angle, outofplane_angle)

        return tilt_angle, grazing, inplane_angle[0], outofplane_angle[0]

    def load_data(
        self,
        detector,
        setup,
        flatfield=None,
        hotpixels=None,
        background=None,
        normalize="skip",
        bin_during_loading=False,
        debugging=False,
        **kwargs,
    ):
        """
        Load CRISTAL data including detector/background corrections.

        It will look for the correct entry 'detector' in the dictionary 'actuators',
        and look for a dataset with compatible shape otherwise.

        :param detector: an instance of the class Detector
        :param setup: an instance of the class Setup
        :param flatfield: the 2D flatfield array
        :param hotpixels: the 2D hotpixels array
        :param background: the 2D background array to subtract to the data
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory space for large 2D detectors.
        :param debugging: set to True to see plots
        :return:
         - the 3D data array in the detector frame
         - the 2D mask array
         - the monitor values for normalization

        """
        if setup.actuators is None:
            raise ValueError("'actuators' parameter required")

        # look for the detector entry (keep changing at CRISTAL)
        if setup.custom_scan:
            raise NotImplementedError("custom scan not implemented for CRISTAL")
        group_key = list(setup.logfile.keys())[0]
        tmp_data = self.find_detector(
            logfile=setup.logfile,
            actuators=setup.actuators,
            root=group_key,
            detector_shape=(detector.nb_pixel_y, detector.nb_pixel_x),
        )

        # find the number of images
        nb_img = tmp_data.shape[0]

        data, mask2d, monitor, loading_roi = self.init_data_mask(
            detector=detector,
            setup=setup,
            normalize=normalize,
            nb_frames=nb_img,
            bin_during_loading=bin_during_loading,
        )

        # loop over frames, mask the detector and normalize / bin
        for idx in range(nb_img):
            data[idx, :, :], mask2d, monitor[idx] = self.load_frame(
                frame=tmp_data[idx, :, :],
                mask2d=mask2d,
                monitor=monitor[idx],
                frames_per_point=1,
                detector=detector,
                loading_roi=loading_roi,
                flatfield=flatfield,
                background=background,
                hotpixels=hotpixels,
                normalize=normalize,
                bin_during_loading=bin_during_loading,
                debugging=debugging,
            )
            sys.stdout.write("\rLoading frame {:d}".format(idx + 1))
            sys.stdout.flush()
        return data, mask2d, monitor, loading_roi

    def motor_positions(self, setup, **kwargs):
        """
        Load the scan data and extract motor positions.

        It will look for the correct entry 'rocking_angle' in the dictionary
        Setup.actuators, and use the default entry otherwise.

        :param setup: an instance of the class Setup
        :return: (mgomega, mgphi, gamma, delta, energy) values
        """
        if not setup.custom_scan:
            group_key = list(setup.logfile.keys())[0]
            energy = (
                self.cristal_load_motor(
                    datafile=setup.logfile,
                    root="/" + group_key + "/CRISTAL/",
                    actuator_name="Monochromator",
                    field_name="energy",
                )
                * 1000
            )  # in eV
            if abs(energy - setup.energy) > 1:
                # difference larger than 1 eV
                print(
                    f"\nWarning: user-defined energy = {setup.energy:.1f} eV different "
                    f"from the energy recorded in the datafile = {energy[0]:.1f} eV\n"
                )

            scanned_motor = self.cristal_load_motor(
                datafile=setup.logfile,
                root="/" + group_key,
                actuator_name="scan_data",
                field_name=setup.actuators.get("rocking_angle", "actuator_1_1"),
            )

            if setup.rocking_angle == "outofplane":
                mgomega = scanned_motor  # mgomega is scanned
                mgphi = self.cristal_load_motor(
                    datafile=setup.logfile,
                    root="/" + group_key + "/CRISTAL/",
                    actuator_name="i06-c-c07-ex-mg_phi",
                    field_name="position",
                )
            elif setup.rocking_angle == "inplane":
                mgphi = scanned_motor  # mgphi is scanned
                mgomega = self.cristal_load_motor(
                    datafile=setup.logfile,
                    root="/" + group_key + "/CRISTAL/",
                    actuator_name="i06-c-c07-ex-mg_omega",
                    field_name="position",
                )
            else:
                raise ValueError('Wrong value for "rocking_angle" parameter')

            delta = self.cristal_load_motor(
                datafile=setup.logfile,
                root="/" + group_key + "/CRISTAL/Diffractometer/",
                actuator_name="I06-C-C07-EX-DIF-DELTA",
                field_name="position",
            )
            gamma = self.cristal_load_motor(
                datafile=setup.logfile,
                root="/" + group_key + "/CRISTAL/Diffractometer/",
                actuator_name="I06-C-C07-EX-DIF-GAMMA",
                field_name="position",
            )

            # remove user-defined sample offsets (sample: mgomega, mgphi)
            mgomega = mgomega - self.sample_offsets[0]
            mgphi = mgphi - self.sample_offsets[1]

        else:  # manually defined custom scan
            mgomega = setup.custom_motors["mgomega"]
            delta = setup.custom_motors["delta"]
            gamma = setup.custom_motors["gamma"]
            mgphi = setup.custom_motors.get("mgphi", 0)
            energy = setup.energy

        # check if mgomega needs to be divided by 1e6
        # (data taken before the implementation of the correction)
        if isinstance(mgomega, float) and abs(mgomega) > 360:
            mgomega = mgomega / 1e6
        elif isinstance(mgomega, (tuple, list, np.ndarray)) and any(
            abs(val) > 360 for val in mgomega
        ):
            mgomega = mgomega / 1e6

        return mgomega, mgphi, gamma, delta, energy, setup.distance

    @staticmethod
    def cristal_load_motor(datafile, root, actuator_name, field_name):
        """
        Try to load the dataset at the defined entry and returns it.

        Patterns keep changing at CRISTAL.

        :param datafile: h5py File object of CRISTAL .nxs scan file
        :param root: string, path of the data up to the last subfolder
         (not included). This part is expected to not change over time
        :param actuator_name: string, name of the actuator
         (e.g. 'I06-C-C07-EX-DIF-KPHI'). Lowercase and uppercase will be tested when
         trying to load the data.
        :param field_name: name of the field under the actuator name (e.g. 'position')
        :return: the dataset if found or 0
        """
        # check input arguments
        valid.valid_container(
            root, container_types=str, min_length=1, name="cristal_load_motor"
        )
        if not root.startswith("/"):
            root = "/" + root
        valid.valid_container(
            actuator_name, container_types=str, min_length=1, name="cristal_load_motor"
        )

        # check if there is an entry for the actuator
        if actuator_name not in datafile[root].keys():
            actuator_name = actuator_name.lower()
            if actuator_name not in datafile[root].keys():
                actuator_name = actuator_name.upper()
                if actuator_name not in datafile[root].keys():
                    print(
                        f"\nCould not find the entry for the actuator'{actuator_name}'"
                    )
                    print(
                        f"list of available actuators: {list(datafile[root].keys())}\n"
                    )
                    return 0

        # check if the field is a valid entry for the actuator
        try:
            dataset = datafile[root + "/" + actuator_name + "/" + field_name][:]
        except KeyError:  # try lowercase
            try:
                dataset = datafile[
                    root + "/" + actuator_name + "/" + field_name.lower()
                ][:]
            except KeyError:  # try uppercase
                try:
                    dataset = datafile[
                        root + "/" + actuator_name + "/" + field_name.upper()
                    ][:]
                except KeyError:  # nothing else that we can do
                    print(
                        f"\nCould not find the field '{field_name}'"
                        f" in the actuator'{actuator_name}'"
                    )
                    print(
                        "list of available fields:"
                        f" {list(datafile[root + '/' + actuator_name].keys())}\n"
                    )
                    return 0
        return dataset

    @staticmethod
    def read_device(logfile, device_name, **kwargs):
        """
        Extract the scanned device positions/values at CRISTAL beamline.

        :param logfile: the logfile created in Setup.create_logfile()
        :param device_name: name of the scanned device
        :return: the positions/values of the device as a numpy 1D array
        """
        group_key = list(logfile.keys())[0]
        print(f"Trying to load values for {device_name}...", end="")
        try:
            device_values = logfile["/" + group_key + "/scan_data/" + device_name][:]
            print("found!")
        except KeyError:
            print(f"no device {device_name} in the logfile")
            device_values = []
        return np.asarray(device_values)

    def read_monitor(self, setup, **kwargs):
        """
        Load the default monitor for a dataset measured at CRISTAL.

        :param setup: an instance of the class Setup
        :return: the default monitor values
        """
        if setup.actuators is not None:
            monitor_name = setup.actuators.get("monitor", "data_04")
            return self.read_device(logfile=setup.logfile, device_name=monitor_name)
        return None


class DiffractometerID01(Diffractometer):
    """
    Define ID01 goniometer: 3 sample circles + 2 detector circles.

    The laboratory frame uses the CXI convention (z downstream, y vertical up,
    x outboard).

    - sample: mu, eta, phi
    - detector: nu,del.

    """

    sample_rotations = ["y-", "x-", "y-"]
    detector_rotations = ["y-", "x-"]
    motor_table = {
        "old_names": {
            "mu": "Mu",
            "eta": "Eta",
            "phi": "Phi",
            "nu": "Nu",
            "delta": "Delta",
            "energy": "Energy",
        },
        "new_names": {
            "mu": "mu",
            "eta": "eta",
            "phi": "phi",
            "nu": "nu",
            "delta": "del",
            "energy": "nrj",
        },
    }

    def __init__(self, sample_offsets):
        super().__init__(
            sample_circles=self.sample_rotations,
            detector_circles=self.detector_rotations,
            sample_offsets=sample_offsets,
        )

    def goniometer_values(self, setup, **kwargs):
        """
        Retrieve goniometer motor positions for a BCDI rocking scan.

        :param setup: the experimental setup: Class Setup
        :param kwargs:
         - 'scan_number': the scan number to load

        :return: a tuple of angular values in degrees (rocking angular step, grazing
         incidence angles, inplane detector angle, outofplane detector angle). The
         grazing incidence angles are the positions of circles below the rocking circle.
        """
        # load kwargs
        scan_number = kwargs["scan_number"]

        # check some parameter
        valid.valid_item(
            scan_number, allowed_types=int, min_excluded=0, name="scan_number"
        )

        # load motor positions
        (
            mu,
            eta,
            phi,
            inplane_angle,
            outofplane_angle,
            energy,
            detector_distance,
        ) = self.motor_positions(
            setup=setup,
            scan_number=scan_number,
        )

        # define the circles of interest for BCDI
        if setup.rocking_angle == "outofplane":  # eta rocking curve
            grazing = (mu,)  # mu below eta but not used at ID01
            tilt_angle = eta
        elif setup.rocking_angle == "inplane":  # phi rocking curve
            grazing = (mu, eta)  # mu below eta but not used at ID01
            tilt_angle = phi
        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')

        setup.check_setup(
            grazing_angle=grazing,
            inplane_angle=inplane_angle,
            outofplane_angle=outofplane_angle,
            tilt_angle=tilt_angle,
            detector_distance=detector_distance,
            energy=energy,
        )

        # ID01 goniometer, 3S+2D (sample: eta, chi, phi / detector: nu,del)
        self.sample_angles = (mu, eta, phi)
        self.detector_angles = (inplane_angle, outofplane_angle)

        return tilt_angle, grazing, inplane_angle, outofplane_angle

    def load_data(
        self,
        detector,
        setup,
        flatfield=None,
        hotpixels=None,
        background=None,
        normalize="skip",
        bin_during_loading=False,
        debugging=False,
        **kwargs,
    ):
        """
        Load ID01 data, apply filters and concatenate it for phasing.

        :param detector: an instance of the class Detector
        :param setup: an instance of the class Setup
        :param flatfield: the 2D flatfield array
        :param hotpixels: the 2D hotpixels array
        :param background: the 2D background array to subtract to the data
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory space for large 2D detectors.
        :param debugging: set to True to see plots
        :param kwargs:
         - 'scan_number': int, the scan number to load

        :return:
         - the 3D data array in the detector frame
         - the 2D mask array
         - the monitor values for normalization

        """
        scan_number = kwargs.get("scan_number")
        if scan_number is None:
            raise ValueError("'scan_number' parameter required")
        if detector.template_imagefile is None:
            raise ValueError("'template_imagefile' must be defined to load the images.")
        ccdfiletmp = os.path.join(detector.datadir, detector.template_imagefile)
        data_stack = None
        if not setup.custom_scan:
            # create the template for the image files
            labels = setup.logfile[str(scan_number) + ".1"].labels  # motor scanned
            labels_data = setup.logfile[str(scan_number) + ".1"].data  # motor scanned

            # find the number of images
            try:
                ccdn = labels_data[labels.index(detector.counter("ID01")), :]
            except ValueError:
                try:
                    print(detector.counter("ID01"), "not in the list, trying 'ccd_n'")
                    ccdn = labels_data[labels.index("ccd_n"), :]
                except ValueError:
                    raise ValueError(
                        "ccd_n not in the list, the detector name may be wrong",
                    )
            nb_img = len(ccdn)
        else:
            ccdn = None  # not used for custom scans
            # create the template for the image files
            if len(setup.custom_images) == 0:
                raise ValueError("No image number provided in 'custom_images'")

            if len(setup.custom_images) > 1:
                nb_img = len(setup.custom_images)
            else:  # the data is stacked into a single file
                npzfile = np.load(ccdfiletmp % setup.custom_images[0])
                data_stack = npzfile[list(npzfile.files)[0]]
                nb_img = data_stack.shape[0]

        data, mask2d, monitor, loading_roi = self.init_data_mask(
            detector=detector,
            setup=setup,
            normalize=normalize,
            nb_frames=nb_img,
            bin_during_loading=bin_during_loading,
            scan_number=scan_number,
        )

        # loop over frames, mask the detector and normalize / bin
        for idx in range(nb_img):
            if data_stack is not None:
                # custom scan with a stacked data loaded
                ccdraw = data_stack[idx, :, :]
            else:
                if setup.custom_scan:
                    # custom scan with one file per frame
                    i = int(setup.custom_images[idx])
                else:
                    i = int(ccdn[idx])
                e = fabio.open(ccdfiletmp % i)
                ccdraw = e.data

            data[idx, :, :], mask2d, monitor[idx] = self.load_frame(
                frame=ccdraw,
                mask2d=mask2d,
                monitor=monitor[idx],
                frames_per_point=1,
                detector=detector,
                loading_roi=loading_roi,
                flatfield=flatfield,
                background=background,
                hotpixels=hotpixels,
                normalize=normalize,
                bin_during_loading=bin_during_loading,
                debugging=debugging,
            )
            sys.stdout.write("\rLoading frame {:d}".format(idx + 1))
            sys.stdout.flush()
        return data, mask2d, monitor, loading_roi

    def motor_positions(self, setup, **kwargs):
        """
        Load the scan data and extract motor positions.

        Stages names for data previous to ?2017? start with a capital letter.

        :param setup: an instance of the class Setup
        :param kwargs:
         - 'scan_number': the scan number to load

        :return: (mu, eta, phi, nu, delta, energy) values
        """
        # load and check kwargs
        scan_number = kwargs["scan_number"]

        old_names = False
        if not setup.custom_scan:
            motor_names = setup.logfile[str(scan_number) + ".1"].motor_names
            # positioners
            motor_values = setup.logfile[str(scan_number) + ".1"].motor_positions
            # positioners
            labels = setup.logfile[str(scan_number) + ".1"].labels  # motor scanned
            labels_data = setup.logfile[str(scan_number) + ".1"].data  # motor scanned

            try:
                _ = motor_values[motor_names.index("nu")]  # positioner
            except ValueError:
                print("'nu' not in the list, trying 'Nu'")
                _ = motor_values[motor_names.index("Nu")]  # positioner
                print("Defaulting to old ID01 motor names")
                old_names = True

            if old_names:
                motor_table = self.motor_table["old_names"]
            else:
                motor_table = self.motor_table["new_names"]

            if motor_table["mu"] in labels:
                mu = labels_data[labels.index(motor_table["mu"]), :]  # scanned
            else:
                mu = motor_values[motor_names.index(motor_table["mu"])]  # positioner

            if motor_table["eta"] in labels:
                eta = labels_data[labels.index(motor_table["eta"]), :]  # scanned
            else:
                eta = motor_values[motor_names.index(motor_table["eta"])]  # positioner

            if motor_table["phi"] in labels:
                phi = labels_data[labels.index(motor_table["phi"]), :]  # scanned
            else:
                phi = motor_values[motor_names.index(motor_table["phi"])]  # positioner

            if motor_table["delta"] in labels:
                delta = labels_data[labels.index(motor_table["delta"]), :]  # scanned
            else:  # positioner
                delta = motor_values[motor_names.index(motor_table["delta"])]

            if motor_table["nu"] in labels:
                nu = labels_data[labels.index(motor_table["nu"]), :]  # scanned
            else:  # positioner
                nu = motor_values[motor_names.index(motor_table["nu"])]

            if motor_table["energy"] in labels:
                raw_energy = labels_data[labels.index(motor_table["energy"]), :]
                # energy scanned, override the user-defined energy
                energy = raw_energy * 1000.0  # switch to eV
            else:  # positioner
                energy = motor_values[motor_names.index(motor_table["energy"])]

            # remove user-defined sample offsets (sample: mu, eta, phi)
            mu = mu - self.sample_offsets[0]
            eta = eta - self.sample_offsets[1]
            phi = phi - self.sample_offsets[2]

        else:  # manually defined custom scan
            mu = setup.custom_motors["mu"]
            eta = setup.custom_motors["eta"]
            phi = setup.custom_motors["phi"]
            delta = setup.custom_motors["delta"]
            nu = setup.custom_motors["nu"]
            energy = setup.energy

        detector_distance = self.retrieve_distance(setup=setup) or setup.distance

        return mu, eta, phi, nu, delta, energy, detector_distance

    @staticmethod
    def read_device(logfile, device_name, **kwargs):
        """
        Extract the scanned device positions/values at ID01 beamline.

        :param logfile: the logfile created in Setup.create_logfile()
        :param device_name: name of the scanned device
        :param kwargs:
         - 'scan_number': int, the scan number to load

        :return: the positions/values of the device as a numpy 1D array
        """
        scan_number = kwargs.get("scan_number")
        if scan_number is None:
            raise ValueError("'scan_number' parameter required")

        labels = logfile[str(scan_number) + ".1"].labels  # motor scanned
        labels_data = logfile[str(scan_number) + ".1"].data  # motor scanned
        print(f"Trying to load values for {device_name}...", end="")
        try:
            device_values = list(labels_data[labels.index(device_name), :])
            print("found!")
        except ValueError:  # device not in the list
            print(f"no device {device_name} in the logfile")
            device_values = []
        return np.asarray(device_values)

    def read_monitor(self, setup, **kwargs):
        """
        Load the default monitor for a dataset measured at ID01.

        :param setup: an instance of the class Setup
        :param kwargs:
         - 'scan_number': int, the scan number to load

        :return: the default monitor values
        """
        scan_number = kwargs.get("scan_number")
        if scan_number is None:
            raise ValueError("'scan_number' parameter required")
        if setup.actuators is not None:
            monitor_name = setup.actuators.get("monitor", "exp1")
            return self.read_device(
                logfile=setup.logfile, scan_number=scan_number, device_name=monitor_name
            )
        return None

    @staticmethod
    def retrieve_distance(setup) -> Optional[float]:
        """
        Load the spec file and retrieve the detector distance if it has been calibrated.

        :param setup: an instance of the class Setup
        :return: the detector distance in meters or None
        """
        path = util.find_file(
            filename=setup.detector.specfile, default_folder=setup.detector.rootdir
        )

        distance = None
        found_distance = 0
        with open(path, "r") as file:
            lines = file.readlines()
            for line in lines:
                if line.startswith("#UDETCALIB"):
                    words = line.split(",")
                    for word in words:
                        if word.startswith("det_distance_COM"):
                            distance = float(word[17:])
                            found_distance += 1

        if found_distance > 1:
            print(
                "multiple dectector distances found in the spec file, using"
                f"{distance} m."
            )
        return distance


class DiffractometerNANOMAX(Diffractometer):
    """
    Define NANOMAX goniometer: 2 sample circles + 2 detector circles.

    The laboratory frame uses the CXI convention (z downstream, y vertical up,
    x outboard).

    - sample: theta, phi
    - detector: gamma,delta.

    """

    sample_rotations = ["x-", "y-"]
    detector_rotations = ["y-", "x-"]

    def __init__(self, sample_offsets):
        super().__init__(
            sample_circles=self.sample_rotations,
            detector_circles=self.detector_rotations,
            sample_offsets=sample_offsets,
        )

    def goniometer_values(self, setup, **kwargs):
        """
        Retrieve goniometer motor positions for a BCDI rocking scan.

        :param setup: the experimental setup: Class Setup
        :return: a tuple of angular values in degrees (rocking angular step, grazing
         incidence angles, inplane detector angle, outofplane detector angle). The
         grazing incidence angles are the positions of circles below the rocking circle.
        """
        # load the motor positions
        (
            theta,
            phi,
            inplane_angle,
            outofplane_angle,
            energy,
            detector_distance,
        ) = self.motor_positions(setup=setup)

        # define the circles of interest for BCDI
        if setup.rocking_angle == "outofplane":  # theta rocking curve
            grazing = None  # nothing below theta at NANOMAX
            tilt_angle = theta
        elif setup.rocking_angle == "inplane":  # phi rocking curve
            grazing = (theta,)
            tilt_angle = phi
        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')

        setup.check_setup(
            grazing_angle=grazing,
            inplane_angle=inplane_angle,
            outofplane_angle=outofplane_angle,
            tilt_angle=tilt_angle,
            detector_distance=detector_distance,
            energy=energy,
        )

        # NANOMAX goniometer, 2S+2D (sample: theta, phi / detector: gamma,delta)
        self.sample_angles = (theta, phi)
        self.detector_angles = (inplane_angle, outofplane_angle)

        return tilt_angle, grazing, inplane_angle, outofplane_angle

    def load_data(
        self,
        detector,
        setup,
        flatfield=None,
        hotpixels=None,
        background=None,
        normalize="skip",
        bin_during_loading=False,
        debugging=False,
        **kwargs,
    ):
        """
        Load NANOMAX data, apply filters and concatenate it for phasing.

        :param detector: an instance of the class Detector
        :param setup: an instance of the calss Setup
        :param flatfield: the 2D flatfield array
        :param hotpixels: the 2D hotpixels array
        :param background: the 2D background array to subtract to the data
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory space for large 2D detectors.
        :param debugging: set to True to see plots
        :return:

         - the 3D data array in the detector frame
         - the 2D mask array
         - the monitor values for normalization

        """
        if debugging:
            print(
                str(setup.logfile["entry"]["description"][()])[3:-2]
            )  # Reading only useful symbols

        if setup.custom_scan:
            raise NotImplementedError("custom scan not implemented for NANOMAX")
        group_key = list(setup.logfile.keys())[0]  # currently 'entry'
        try:
            tmp_data = setup.logfile["/" + group_key + "/measurement/merlin/frames"][:]
        except KeyError:
            tmp_data = setup.logfile["/" + group_key + "measurement/Merlin/data"][()]

        # find the number of images
        nb_img = tmp_data.shape[0]

        data, mask2d, monitor, loading_roi = self.init_data_mask(
            detector=detector,
            setup=setup,
            normalize=normalize,
            nb_frames=nb_img,
            bin_during_loading=bin_during_loading,
        )

        # loop over frames, mask the detector and normalize / bin
        for idx in range(nb_img):
            data[idx, :, :], mask2d, monitor[idx] = self.load_frame(
                frame=tmp_data[idx, :, :],
                mask2d=mask2d,
                monitor=monitor[idx],
                frames_per_point=1,
                detector=detector,
                loading_roi=loading_roi,
                flatfield=flatfield,
                background=background,
                hotpixels=hotpixels,
                normalize=normalize,
                bin_during_loading=bin_during_loading,
                debugging=debugging,
            )
            sys.stdout.write("\rLoading frame {:d}".format(idx + 1))
            sys.stdout.flush()
        return data, mask2d, monitor, loading_roi

    def motor_positions(self, setup, **kwargs):
        """
        Load the scan data and extract motor positions.

        :param setup: an instance of the class Setup
        :return: (theta, phi, gamma, delta, energy) values
        """
        if not setup.custom_scan:
            # Detector positions
            group_key = list(setup.logfile.keys())[0]  # currently 'entry'

            # positionners
            delta = setup.logfile["/" + group_key + "/snapshot/delta"][:]
            gamma = setup.logfile["/" + group_key + "/snapshot/gamma"][:]
            energy = setup.logfile["/" + group_key + "/snapshot/energy"][:]

            if setup.rocking_angle == "inplane":
                try:
                    phi = setup.logfile["/" + group_key + "/measurement/gonphi"][:]
                except KeyError:
                    raise KeyError(
                        "phi not in measurement data,"
                        ' check the parameter "rocking_angle"'
                    )
                theta = setup.logfile["/" + group_key + "/snapshot/gontheta"][:]
            else:
                try:
                    theta = setup.logfile["/" + group_key + "/measurement/gontheta"][:]
                except KeyError:
                    raise KeyError(
                        "theta not in measurement data,"
                        ' check the parameter "rocking_angle"'
                    )
                phi = setup.logfile["/" + group_key + "/snapshot/gonphi"][:]

            # remove user-defined sample offsets (sample: theta, phi)
            theta = theta - self.sample_offsets[0]
            phi = phi - self.sample_offsets[1]

        else:  # manually defined custom scan
            theta = setup.custom_motors["theta"]
            phi = setup.custom_motors["phi"]
            delta = setup.custom_motors["delta"]
            gamma = setup.custom_motors["gamma"]
            energy = setup.energy

        return theta, phi, gamma, delta, energy, setup.distance

    @staticmethod
    def read_device(logfile, device_name, **kwargs):
        """
        Extract the scanned device positions/values at Nanomax beamline.

        :param logfile: the logfile created in Setup.create_logfile()
        :param device_name: name of the scanned device
        :return: the positions/values of the device as a numpy 1D array
        """
        group_key = list(logfile.keys())[0]  # currently 'entry'
        print(f"Trying to load values for {device_name}...", end="")
        try:
            device_values = logfile["/" + group_key + "/measurement/" + device_name][:]
            print("found!")
        except KeyError:
            print(f"No device {device_name} in the logfile")
            device_values = []
        return np.asarray(device_values)

    def read_monitor(self, setup, **kwargs):
        """
        Load the default monitor for a dataset measured at NANOMAX.

        :param setup: an instance of the class Setup
        :return: the default monitor values
        """
        return self.read_device(logfile=setup.logfile, device_name="alba2")


class DiffractometerP10(Diffractometer):
    """
    Define P10 goniometer: 4 sample circles + 2 detector circles.

    The laboratory frame uses the CXI convention (z downstream, y vertical up,
    x outboard).

    - sample: mu, om, chi, phi
    - detector: gamma, delta.

    """

    sample_rotations = ["y+", "x-", "z+", "y-"]
    detector_rotations = ["y+", "x-"]
    default_offsets = (0, 0, 90, 0)

    def __init__(self, sample_offsets):
        super().__init__(
            sample_circles=self.sample_rotations,
            detector_circles=self.detector_rotations,
            sample_offsets=sample_offsets,
            default_offsets=self.default_offsets,
        )

    def goniometer_values(self, setup, **kwargs):
        """
        Retrieve goniometer motor positions for a BCDI rocking scan.

        :param setup: the experimental setup: Class Setup
        :return: a tuple of angular values in degrees (rocking angular step, grazing
         incidence angles, inplane detector angle, outofplane detector angle). The
         grazing incidence angles are the positions of circles below the rocking circle.
        """
        # load the motor positions
        (
            mu,
            om,
            chi,
            phi,
            inplane_angle,
            outofplane_angle,
            energy,
            detector_distance,
        ) = self.motor_positions(setup=setup)

        # define the circles of interest for BCDI
        if setup.rocking_angle == "outofplane":  # om rocking curve
            grazing = (mu,)
            tilt_angle = om
        elif setup.rocking_angle == "inplane":  # phi rocking curve
            grazing = (mu, om, chi)
            tilt_angle = phi
        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')

        setup.check_setup(
            grazing_angle=grazing,
            inplane_angle=inplane_angle,
            outofplane_angle=outofplane_angle,
            tilt_angle=tilt_angle,
            detector_distance=detector_distance,
            energy=energy,
        )

        # P10 goniometer, 4S+2D (sample: mu, omega, chi, phi / detector: gamma, delta)
        self.sample_angles = (mu, om, chi, phi)
        self.detector_angles = (inplane_angle, outofplane_angle)

        return tilt_angle, grazing, inplane_angle, outofplane_angle

    def load_data(
        self,
        detector,
        setup,
        flatfield=None,
        hotpixels=None,
        background=None,
        normalize="skip",
        bin_during_loading=False,
        debugging=False,
        **kwargs,
    ):
        """
        Load P10 data, apply filters and concatenate it for phasing.

        :param detector: an instance of the class Detector
        :param setup: an instance of the class Setup
        :param flatfield: the 2D flatfield array
        :param hotpixels: the 2D hotpixels array
        :param background: the 2D background array to subtract to the data
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip to do nothing'
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory space for large 2D detectors.
        :param debugging: set to True to see plots
        :return:

         - the 3D data array in the detector frame
         - the 2D mask array
         - the monitor values for normalization

        """
        if detector.template_imagefile is None:
            raise ValueError("'template_imagefile' must be defined to load the images.")
        # template for the master file
        ccdfiletmp = os.path.join(detector.datadir, detector.template_imagefile)
        is_series = setup.is_series
        if not setup.custom_scan:
            h5file = h5py.File(ccdfiletmp, "r")

            # find the number of images
            # (i.e. points, not including series at each point)
            if is_series:
                nb_img = len(list(h5file["entry/data"]))
            else:
                idx = 0
                nb_img = 0
                while True:
                    data_path = "data_" + str("{:06d}".format(idx + 1))
                    try:
                        nb_img += len(h5file["entry"]["data"][data_path])
                        idx += 1
                    except KeyError:
                        break
            print("Number of points :", nb_img)
        else:
            h5file = None  # this will be define directly in the while loop
            # create the template for the image files
            if len(setup.custom_images) > 0:
                nb_img = len(setup.custom_images)
            else:
                raise ValueError("No image number provided in 'custom_images'")

        # initialize arrays and loading ROI
        data, mask2d, monitor, loading_roi = self.init_data_mask(
            detector=detector,
            setup=setup,
            normalize=normalize,
            nb_frames=nb_img,
            bin_during_loading=bin_during_loading,
        )

        # loop over frames, mask the detector and normalize / bin
        start_index = 0  # offset when not is_series
        for point_idx in range(nb_img):
            idx = 0
            series_data = []
            series_monitor = []
            if setup.custom_scan:
                # custom scan with one file per frame/series of frame, no master file in
                # this case, load directly data files.
                i = int(setup.custom_images[idx])
                ccdfiletmp = (
                    detector.rootdir
                    + detector.sample_name
                    + "_{:05d}".format(i)
                    + "/e4m/"
                    + detector.sample_name
                    + "_{:05d}".format(i)
                    + detector.template_file
                )
                h5file = h5py.File(ccdfiletmp, "r")  # load the data file
                data_path = "data_000001"
            else:
                # normal scan, h5file is in this case the master .h5 file
                data_path = "data_" + str("{:06d}".format(point_idx + 1))

            while True:
                try:
                    try:
                        tmp_data = h5file["entry"]["data"][data_path][idx]
                    except OSError:
                        raise OSError("hdf5plugin is not installed")

                    # a single frame from the (eventual) series is loaded
                    ccdraw, mask2d, temp_mon = self.load_frame(
                        frame=tmp_data,
                        mask2d=mask2d,
                        monitor=monitor[idx],
                        frames_per_point=1,
                        detector=detector,
                        loading_roi=loading_roi,
                        flatfield=flatfield,
                        background=background,
                        hotpixels=hotpixels,
                        normalize=normalize,
                        bin_during_loading=bin_during_loading,
                        debugging=debugging,
                    )
                    series_data.append(ccdraw)
                    series_monitor.append(temp_mon)

                    if not is_series:
                        sys.stdout.write(
                            "\rLoading frame {:d}".format(start_index + idx + 1)
                        )
                        sys.stdout.flush()
                    idx = idx + 1
                except IndexError:  # reached the end of the series
                    break
                except ValueError:  # something went wrong
                    break

            if len(series_data) == 0:
                raise ValueError(
                    f"Check the parameter 'is_series', current value {is_series}"
                )
            if is_series:
                data[point_idx, :, :] = np.asarray(series_data).sum(axis=0)
                if normalize == "sum_roi":
                    monitor[point_idx] = np.asarray(series_monitor).sum()
                sys.stdout.write("\rSeries: loading frame {:d}".format(point_idx + 1))
                sys.stdout.flush()
            else:
                tempdata_length = len(series_data)
                data[start_index : start_index + tempdata_length, :, :] = np.asarray(
                    series_data
                )

                if normalize == "sum_roi":
                    monitor[start_index : start_index + tempdata_length] = np.asarray(
                        series_monitor
                    )
                start_index += tempdata_length
                if start_index == nb_img:
                    break
        return data, mask2d, monitor, loading_roi

    def motor_positions(self, setup, **kwargs):
        """
        Load the .fio file from the scan and extract motor positions.

        :param setup: an instance of the class Setup
        :return: (om, phi, chi, mu, gamma, delta, energy) values
        """
        if not setup.custom_scan:
            with open(setup.logfile, "r") as fio:
                index_om = None
                index_phi = None
                om = []
                phi = []
                chi = None
                mu = None
                gamma = None
                delta = None
                energy = None

                fio_lines = fio.readlines()
                for line in fio_lines:
                    this_line = line.strip()
                    words = this_line.split()

                    if (
                        "Col" in words and "om" in words
                    ):  # om scanned, template = ' Col 0 om DOUBLE\n'
                        index_om = int(words[1]) - 1  # python index starts at 0
                    if (
                        "om" in words
                        and "=" in words
                        and setup.rocking_angle == "inplane"
                    ):  # om is a positioner
                        om = float(words[2])

                    if (
                        "Col" in words and "phi" in words
                    ):  # phi scanned, template = ' Col 0 phi DOUBLE\n'
                        index_phi = int(words[1]) - 1  # python index starts at 0
                    if (
                        "phi" in words
                        and "=" in words
                        and setup.rocking_angle == "outofplane"
                    ):  # phi is a positioner
                        phi = float(words[2])

                    if (
                        "chi" in words and "=" in words
                    ):  # template for positioners: 'chi = 90.0\n'
                        chi = float(words[2])
                    if (
                        "del" in words and "=" in words
                    ):  # template for positioners: 'del = 30.05\n'
                        delta = float(words[2])
                    if (
                        "gam" in words and "=" in words
                    ):  # template for positioners: 'gam = 4.05\n'
                        gamma = float(words[2])
                    if (
                        "mu" in words and "=" in words
                    ):  # template for positioners: 'mu = 0.0\n'
                        mu = float(words[2])
                    if (
                        "fmbenergy" in words and "=" in words
                    ):  # template for positioners: 'mu = 0.0\n'
                        energy = float(words[2])

                    if index_om is not None and util.is_float(words[0]):
                        # reading data and index_om is defined (outofplane case)
                        om.append(float(words[index_om]))
                    if index_phi is not None and util.is_float(words[0]):
                        # reading data and index_phi is defined (inplane case)
                        phi.append(float(words[index_phi]))

                if setup.rocking_angle == "outofplane":
                    om = np.asarray(om, dtype=float)
                else:  # phi
                    phi = np.asarray(phi, dtype=float)

                # remove user-defined sample offsets (sample: mu, om, chi, phi)
                mu = mu - self.sample_offsets[0]
                om = om - self.sample_offsets[1]
                chi = chi - self.sample_offsets[2]
                phi = phi - self.sample_offsets[3]

        else:  # manually defined custom scan
            om = setup.custom_motors["om"]
            chi = setup.custom_motors["chi"]
            phi = setup.custom_motors["phi"]
            delta = setup.custom_motors["delta"]
            gamma = setup.custom_motors["gamma"]
            mu = setup.custom_motors["mu"]
            energy = setup.energy

        return mu, om, chi, phi, gamma, delta, energy, setup.distance

    @staticmethod
    def read_device(logfile, device_name, **kwargs):
        """
        Extract the scanned device positions/values at P10 beamline.

        :param logfile: the logfile created in Setup.create_logfile()
        :param device_name: name of the scanned device
        :return: the positions/values of the device as a numpy 1D array
        """
        device_values = []
        index_device = None  # index of the column corresponding to the device in .fio
        print(f"Trying to load values for {device_name}...", end="")
        with open(logfile, "r") as fio:
            fio_lines = fio.readlines()
            for line in fio_lines:
                this_line = line.strip()
                words = this_line.split()

                if "Col" in words and device_name in words:
                    # device_name scanned, template = ' Col 0 motor_name DOUBLE\n'
                    index_device = int(words[1]) - 1  # python index starts at 0

                if index_device is not None and util.is_float(words[0]):
                    # we are reading data and index_motor is defined
                    device_values.append(float(words[index_device]))

        if index_device is None:
            print(f"no device {device_name} in the logfile")
        else:
            print("found!")
        return np.asarray(device_values)

    def read_monitor(self, setup, **kwargs):
        """
        Load the default monitor for a dataset measured at P10.

        :param setup: an instance of the class Setup
        :return: the default monitor values
        """
        monitor = self.read_device(logfile=setup.logfile, device_name="ipetra")
        if len(monitor) == 0:
            monitor = self.read_device(logfile=setup.logfile, device_name="curpetra")
        return monitor


class DiffractometerP10SAXS(DiffractometerP10):
    """
    Define P10 goniometer for the USAXS setup: 1 sample circle, no detector circle.

    The laboratory frame uses the CXI convention (z downstream, y vertical up,
    x outboard).

    - sample: phi (names hprz or sprz at the beamline)

    """

    sample_rotations = ["y+"]
    detector_rotations: List[str] = []

    def __init__(self):
        super().__init__(sample_offsets=(0,))

    def goniometer_values(self, setup, **kwargs):
        """
        Retrieve goniometer motor positions for a CDI tomographic scan.

        :param setup: the experimental setup: Class Setup
        :return: a tuple of angular values in degrees (rocking angular step, grazing
         incidence angles, inplane detector angle, outofplane detector angle). The
         grazing incidence angles are the positions of circles below the rocking circle.
        """
        # load the motor positions
        phi, energy, detector_distance = self.motor_positions(setup=setup)

        # define the circles of interest for CDI
        # no circle yet below phi at P10
        if setup.rocking_angle == "inplane":  # phi rocking curve
            grazing = (0,)
            tilt_angle = phi
        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')

        setup.check_setup(
            grazing_angle=grazing,
            inplane_angle=0,
            outofplane_angle=0,
            tilt_angle=tilt_angle,
            detector_distance=detector_distance,
            energy=energy,
        )

        # P10 SAXS goniometer, 1S + 0D (sample: phi / detector: None)
        self.sample_angles = (phi,)
        self.detector_angles = (0, 0)

        return tilt_angle, grazing, 0, 0

    def motor_positions(self, setup, **kwargs):
        """
        Load the .fio file from the scan and extract motor positions.

        :param setup: an instance of the class Setup
        :return: (phi, energy) values
        """
        if setup.rocking_angle != "inplane":
            raise ValueError('Wrong value for "rocking_angle" parameter')

        if not setup.custom_scan:
            index_phi = None
            phi = []

            with open(setup.logfile, "r") as fio:
                fio_lines = fio.readlines()
                for line in fio_lines:
                    this_line = line.strip()
                    words = this_line.split()

                    if "Col" in words and ("sprz" in words or "hprz" in words):
                        # sprz or hprz (SAXS) scanned
                        # template = ' Col 0 sprz DOUBLE\n'
                        index_phi = int(words[1]) - 1  # python index starts at 0
                        print(words, "  Index Phi=", index_phi)
                    if index_phi is not None and util.is_float(words[0]):
                        # we are reading data and index_phi is defined
                        phi.append(float(words[index_phi]))

            phi = np.asarray(phi, dtype=float)
        else:
            phi = setup.custom_motors["phi"]
        return phi, setup.energy, setup.distance


class DiffractometerSIXS(Diffractometer):
    """
    Define SIXS goniometer: 2 sample circles + 3 detector circles.

    The laboratory frame uses the CXI convention (z downstream, y vertical up,
    x outboard).

    - sample: beta, mu
    - detector: beta, gamma, del.

    """

    sample_rotations = ["x-", "y+"]
    detector_rotations = ["x-", "y+", "x-"]

    def __init__(self, sample_offsets):
        super().__init__(
            sample_circles=self.sample_rotations,
            detector_circles=self.detector_rotations,
            sample_offsets=sample_offsets,
        )

    def goniometer_values(self, setup, **kwargs):
        """
        Retrieve goniometer motor positions for a BCDI rocking scan at SIXS.

        :param setup: the experimental setup: Class Setup
        :return: a tuple of angular values in degrees (rocking angular step, grazing
         incidence angles, inplane detector angle, outofplane detector angle). The
         grazing incidence angles are the positions of circles below the rocking circle.
        """
        # load the motor positions
        (
            beta,
            mu,
            inplane_angle,
            outofplane_angle,
            energy,
            detector_distance,
        ) = self.motor_positions(setup=setup)

        # define the circles of interest for BCDI
        if setup.rocking_angle == "inplane":  # mu rocking curve
            grazing = (beta,)  # beta below the whole diffractomter at SIXS
            tilt_angle = mu
        elif setup.rocking_angle == "outofplane":
            raise NotImplementedError(
                "outofplane rocking curve not implemented for SIXS"
            )
        else:
            raise ValueError("Out-of-plane rocking curve not implemented for SIXS")

        setup.check_setup(
            grazing_angle=grazing,
            inplane_angle=inplane_angle,
            outofplane_angle=outofplane_angle,
            tilt_angle=tilt_angle,
            detector_distance=detector_distance,
            energy=energy,
        )

        # SIXS goniometer, 2S+3D (sample: beta, mu / detector: beta, gamma, del)
        self.sample_angles = (beta, mu)
        self.detector_angles = (beta, inplane_angle, outofplane_angle)

        return tilt_angle, grazing, inplane_angle, outofplane_angle

    def load_data(
        self,
        detector,
        setup,
        flatfield=None,
        hotpixels=None,
        background=None,
        normalize="skip",
        bin_during_loading=False,
        debugging=False,
        **kwargs,
    ):
        """
        Load data, apply filters and concatenate it for phasing at SIXS.

        :param detector: an instance of the class Detector
        :param setup: an instance of the class Setup
        :param flatfield: the 2D flatfield array
        :param hotpixels: the 2D hotpixels array
        :param background: the 2D background array to subtract to the data
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory space for large 2D detectors.
        :param debugging: set to True to see plots
        :return:

         - the 3D data array in the detector frame
         - the 2D mask array
         - the monitor values for normalization

        """
        # load the data
        if setup.custom_scan:
            raise NotImplementedError("custom scan not implemented for NANOMAX")
        if detector.name == "Merlin":
            tmp_data = setup.logfile.merlin[:]
        else:  # Maxipix
            if setup.beamline == "SIXS_2018":
                tmp_data = setup.logfile.mfilm[:]
            else:
                try:
                    tmp_data = setup.logfile.mpx_image[:]
                except AttributeError:
                    try:
                        tmp_data = setup.logfile.maxpix[:]
                    except AttributeError:
                        # the alias dictionnary was probably not provided
                        tmp_data = setup.logfile.image[:]

        # find the number of images
        nb_img = tmp_data.shape[0]

        # initialize arrays and loading ROI
        data, mask2d, monitor, loading_roi = self.init_data_mask(
            detector=detector,
            setup=setup,
            normalize=normalize,
            nb_frames=nb_img,
            bin_during_loading=bin_during_loading,
        )

        # loop over frames, mask the detector and normalize / bin
        for idx in range(nb_img):
            data[idx, :, :], mask2d, monitor[idx] = self.load_frame(
                frame=tmp_data[idx, :, :],
                mask2d=mask2d,
                monitor=monitor[idx],
                frames_per_point=1,
                detector=detector,
                loading_roi=loading_roi,
                flatfield=flatfield,
                background=background,
                hotpixels=hotpixels,
                normalize=normalize,
                bin_during_loading=bin_during_loading,
                debugging=debugging,
            )
            sys.stdout.write("\rLoading frame {:d}".format(idx + 1))
            sys.stdout.flush()
        return data, mask2d, monitor, loading_roi

    def motor_positions(self, setup, **kwargs):
        """
        Load the scan data and extract motor positions at SIXS.

        :param setup: an instance of the class Setup
        :return: (beta, mu, gamma, delta, energy) values
        """
        if not setup.custom_scan:
            mu = setup.logfile.mu[:]  # scanned
            delta = setup.logfile.delta[0]  # not scanned
            gamma = setup.logfile.gamma[0]  # not scanned
            try:
                beta = setup.logfile.basepitch[0]  # not scanned
            except AttributeError:  # data recorder changed after 11/03/2019
                try:
                    beta = setup.logfile.beta[0]  # not scanned
                except AttributeError:
                    # the alias dictionnary was probably not provided
                    beta = 0

            # remove user-defined sample offsets (sample: beta, mu)
            beta = beta - self.sample_offsets[0]
            mu = mu - self.sample_offsets[1]

        else:  # manually defined custom scan
            beta = setup.custom_motors["beta"]
            delta = setup.custom_motors["delta"]
            gamma = setup.custom_motors["gamma"]
            mu = setup.custom_motors["mu"]
        return beta, mu, gamma, delta, setup.energy, setup.distance

    @staticmethod
    def read_device(logfile, device_name, **kwargs):
        """
        Extract the scanned device positions/values at SIXS beamline.

        :param logfile: the logfile created in Setup.create_logfile()
        :param device_name: name of the scanned device
        :return: the positions/values of the device as a numpy 1D array
        """
        print(f"Trying to load values for {device_name}...", end="")
        try:
            device_values = getattr(logfile, device_name)
            print("found!")
        except AttributeError:
            print(f"No device {device_name} in the logfile")
            device_values = []
        return np.asarray(device_values)

    def read_monitor(self, setup, **kwargs):
        """
        Load the default monitor for a dataset measured at SIXS.

        :param setup: an instance of the class Setup
        :return: the default monitor values
        """
        if setup.beamline is None:
            raise ValueError("'beamline' parameter required")
        if setup.beamline == "SIXS_2018":
            return self.read_device(logfile=setup.logfile, device_name="imon1")
        # SIXS_2019
        monitor = self.read_device(logfile=setup.logfile, device_name="imon0")
        if len(monitor) == 0:  # the alias dictionnary was probably not provided
            monitor = self.read_device(logfile=setup.logfile, device_name="intensity")
        return monitor


class Diffractometer34ID(Diffractometer):
    """
    Define 34ID goniometer: 3 sample circles + 2 detector circles.

    The laboratory frame uses the CXI convention (z downstream, y vertical up,
    x outboard).

    - sample: theta (inplane), chi, phi (out of plane)
    - detector: delta (inplane), gamma).

    """

    sample_rotations = ["y+", "z-", "y+"]
    detector_rotations = ["y+", "x-"]
    default_offsets = (0, 90, 0)
    motor_table = {
        "theta": "Theta",
        "chi": "Chi",
        "phi": "Phi",
        "gamma": "Gamma",
        "delta": "Delta",
        "energy": "Energy",
        "detector_distance": "camdist",
    }

    def __init__(self, sample_offsets):
        super().__init__(
            sample_circles=self.sample_rotations,
            detector_circles=self.detector_rotations,
            sample_offsets=sample_offsets,
            default_offsets=self.default_offsets,
        )

    def goniometer_values(self, setup, **kwargs):
        """
        Retrieve goniometer motor positions for a BCDI rocking scan.

        :param setup: the experimental setup: Class Setup
        :param kwargs:
         - 'scan_number': the scan number to load

        :return: a tuple of angular values in degrees (rocking angular step, grazing
         incidence angles, inplane detector angle, outofplane detector angle). The
         grazing incidence angles are the positions of circles below the rocking circle.
        """
        # load kwargs
        scan_number = kwargs["scan_number"]

        # check some parameter
        valid.valid_item(
            scan_number, allowed_types=int, min_excluded=0, name="scan_number"
        )

        # load the motor positions
        (
            theta,
            chi,
            phi,
            inplane_angle,
            outofplane_angle,
            energy,
            detector_distance,
        ) = self.motor_positions(setup=setup, scan_number=scan_number)

        # define the circles of interest for BCDI
        if setup.rocking_angle == "inplane":
            # theta is the inplane rotation around the vertical axis at 34ID
            grazing = None  # theta (inplane) is below phi
            tilt_angle = theta
        elif setup.rocking_angle == "outofplane":
            # phi is the incident angle (out of plane rotation) at 34ID
            grazing = (theta, chi)
            tilt_angle = phi
        else:
            raise ValueError('Wrong value for "rocking_angle" parameter')

        setup.check_setup(
            grazing_angle=grazing,
            inplane_angle=inplane_angle,
            outofplane_angle=outofplane_angle,
            tilt_angle=tilt_angle,
            detector_distance=detector_distance,
            energy=energy,
        )

        # 34ID-C goniometer, 3S+2D (sample: theta (inplane), chi (close to 90 deg),
        # phi (out of plane)   detector: delta (inplane), gamma)
        self.sample_angles = (theta, chi, phi)
        self.detector_angles = (inplane_angle, outofplane_angle)

        return tilt_angle, grazing, inplane_angle, outofplane_angle

    def load_data(
        self,
        detector,
        setup,
        flatfield=None,
        hotpixels=None,
        background=None,
        normalize="skip",
        bin_during_loading=False,
        debugging=False,
        **kwargs,
    ):
        """
        Load 34ID-C data including detector/background corrections.

        :param detector: an instance of the class Detector
        :param setup: an instance of the class Setup
        :param flatfield: the 2D flatfield array
        :param hotpixels: the 2D hotpixels array
        :param background: the 2D background array to subtract to the data
        :param normalize: 'monitor' to return the default monitor values, 'sum_roi' to
         return a monitor based on the integrated intensity in the region of interest
         defined by detector.sum_roi, 'skip' to do nothing
        :param bin_during_loading: if True, the data will be binned in the detector
         frame while loading. It saves a lot of memory space for large 2D detectors.
        :param debugging: set to True to see plots
        """
        scan_number = kwargs.get("scan_number")
        if scan_number is None:
            raise ValueError("'scan_number' parameter required")
        if detector.template_imagefile is None:
            raise ValueError("'template_imagefile' must be defined to load the images.")
        ccdfiletmp = os.path.join(detector.datadir, detector.template_imagefile)
        data_stack = None
        if not setup.custom_scan:
            # create the template for the image files
            labels = setup.logfile[str(scan_number) + ".1"].labels  # motor scanned
            labels_data = setup.logfile[str(scan_number) + ".1"].data  # motor scanned

            # find the number of images
            try:
                nb_img = len(labels_data[labels.index("Monitor"), :])
            except ValueError:
                try:
                    print("'Monitor' not in the list, trying 'Detector'")
                    nb_img = len(labels_data[labels.index("Detector"), :])
                except ValueError:
                    raise ValueError(
                        "'Detector' not in the list, can't retrieve "
                        "the number of frames",
                    )
        else:
            # create the template for the image files
            if len(setup.custom_images) == 0:
                raise ValueError("No image number provided in 'custom_images'")

            if len(setup.custom_images) > 1:
                nb_img = len(setup.custom_images)
            else:  # the data is stacked into a single file
                npzfile = np.load(ccdfiletmp % setup.custom_images[0])
                data_stack = npzfile[list(npzfile.files)[0]]
                nb_img = data_stack.shape[0]

        data, mask2d, monitor, loading_roi = self.init_data_mask(
            detector=detector,
            setup=setup,
            normalize=normalize,
            nb_frames=nb_img,
            bin_during_loading=bin_during_loading,
            scan_number=scan_number,
        )

        # loop over frames, mask the detector and normalize / bin
        for idx in range(nb_img):
            if data_stack is not None:
                # custom scan with a stacked data loaded
                ccdraw = data_stack[idx, :, :]
            else:
                if setup.custom_scan:
                    # custom scan with one file per frame
                    i = int(setup.custom_images[idx])
                else:
                    i = idx
                try:
                    ccdraw = util.image_to_ndarray(
                        filename=ccdfiletmp % i,
                        convert_grey=True,
                        cmap="gray",
                        debug=False,
                    )
                except TypeError:
                    raise ValueError(
                        "Error in string formatting of the image filename, "
                        "check the value of 'template_imagefile'"
                    )

            data[idx, :, :], mask2d, monitor[idx] = self.load_frame(
                frame=ccdraw,
                mask2d=mask2d,
                monitor=monitor[idx],
                frames_per_point=1,
                detector=detector,
                loading_roi=loading_roi,
                flatfield=flatfield,
                background=background,
                hotpixels=hotpixels,
                normalize=normalize,
                bin_during_loading=bin_during_loading,
                debugging=debugging,
            )
            sys.stdout.write("\rLoading frame {:d}".format(idx + 1))
            sys.stdout.flush()
        return data, mask2d, monitor, loading_roi

    def motor_positions(self, setup, **kwargs):
        """
        Load the scan data and extract motor positions.

        :param setup: an instance of the class Setup
        :param kwargs:
         - 'scan_number': the scan number to load

        :return: (theta, phi, delta, gamma, energy) values
        """
        # load and check kwargs
        scan_number = kwargs["scan_number"]

        if not setup.custom_scan:
            motor_names = setup.logfile[str(scan_number) + ".1"].motor_names
            # positioners
            motor_values = setup.logfile[str(scan_number) + ".1"].motor_positions
            # positioners
            labels = setup.logfile[str(scan_number) + ".1"].labels  # motor scanned
            labels_data = setup.logfile[str(scan_number) + ".1"].data  # motor scanned

            if self.motor_table["theta"] in labels:  # scanned
                theta = labels_data[labels.index(self.motor_table["theta"]), :]
            else:  # positioner
                theta = motor_values[motor_names.index(self.motor_table["theta"])]

            if self.motor_table["chi"] in labels:  # scanned
                chi = labels_data[labels.index(self.motor_table["chi"]), :]
            else:  # positioner
                chi = motor_values[motor_names.index(self.motor_table["chi"])]

            if self.motor_table["phi"] in labels:  # scanned
                phi = labels_data[labels.index(self.motor_table["phi"]), :]
            else:  # positioner
                phi = motor_values[motor_names.index(self.motor_table["phi"])]

            if self.motor_table["delta"] in labels:  # scanned
                delta = labels_data[labels.index(self.motor_table["delta"]), :]
            else:  # positioner
                delta = motor_values[motor_names.index(self.motor_table["delta"])]

            if self.motor_table["gamma"] in labels:  # scanned
                gamma = labels_data[labels.index(self.motor_table["gamma"]), :]
            else:  # positioner
                gamma = motor_values[motor_names.index(self.motor_table["gamma"])]

            if self.motor_table["energy"] in labels:  # scanned
                raw_energy = labels_data[labels.index(self.motor_table["energy"]), :]
                # energy scanned, override the user-defined energy
                energy = raw_energy * 1000.0  # switch to eV
            else:  # positioner
                energy = motor_values[motor_names.index(self.motor_table["energy"])]

            detector_distance = motor_values[
                motor_names.index(self.motor_table["detector_distance"])
            ]

            # remove user-defined sample offsets (sample: mu, eta, phi)
            theta = theta - self.sample_offsets[0]
            chi = chi - self.sample_offsets[1]
            phi = phi - self.sample_offsets[2]

        else:  # manually defined custom scan
            theta = setup.custom_motors["theta"]
            chi = setup.custom_motors["chi"]
            phi = setup.custom_motors["phi"]
            gamma = setup.custom_motors["gamma"]
            delta = setup.custom_motors["delta"]
            detector_distance = setup.distance
            energy = setup.energy

        return theta, chi, phi, delta, gamma, energy, detector_distance

    @staticmethod
    def read_device(logfile, device_name, **kwargs):
        """
        Extract the scanned device positions/values at 34ID-C beamline.

        :param logfile: the logfile created in Setup.create_logfile()
        :param device_name: name of the scanned device
        :param kwargs:
         - 'scan_number': int, the scan number to load

        :return: the positions/values of the device as a numpy 1D array
        """
        scan_number = kwargs.get("scan_number")
        if scan_number is None:
            raise ValueError("'scan_number' parameter required")

        labels = logfile[str(scan_number) + ".1"].labels  # motor scanned
        labels_data = logfile[str(scan_number) + ".1"].data  # motor scanned
        print(f"Trying to load values for {device_name}...", end="")
        try:
            device_values = list(labels_data[labels.index(device_name), :])
            print("found!")
        except ValueError:  # device not in the list
            print(f"no device {device_name} in the logfile")
            device_values = []
        return np.asarray(device_values)

    def read_monitor(self, setup, **kwargs):
        """
        Load the default monitor for a dataset measured at 34ID-C.

        :param setup: an instance of the class Setup
        :param kwargs:
         - 'scan_number': int, the scan number to load

        :return: the default monitor values
        """
        scan_number = kwargs.get("scan_number")
        if scan_number is None:
            raise ValueError("'scan_number' parameter required")
        if setup.actuators is not None:
            monitor_name = setup.actuators.get("monitor", "Monitor")
            return self.read_device(
                logfile=setup.logfile, scan_number=scan_number, device_name=monitor_name
            )
        return None
