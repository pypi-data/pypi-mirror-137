"""
    @file:              base_patient_data_factory.py
    @Author:            Maxence Larose

    @Creation Date:     01/2022
    @Last modification: 01/2022

    @Description:       This file contains the class BasePatientDataFactory that is used as an abstract class used as a
                        reference for all other patient data factories.
"""

from abc import ABC, abstractmethod
import os
from typing import Dict, List, Optional

from ....data_model import PatientDataModel
from ...image.dicom_reader import DicomReader


class BasePatientDataFactory(ABC):
    """
    An abstract class that is used as a reference for all other patient data factories.
    """

    def __init__(
            self,
            path_to_images_folder: str,
            path_to_segmentations_folder: Optional[str],
            series_descriptions: Optional[Dict[str, List[str]]],
            verbose: bool
    ):
        """
        Constructor of the class BasePatientDataFactory.

        Parameters
        ----------
        path_to_images_folder : str
            Path to the folder containing the patient's image files.
        path_to_segmentations_folder: Optional[str]
            Path to the folder containing the patient's segmentation files.
        series_descriptions : Optional[Dict[str, List[str]]]
            A dictionary that contains the series descriptions of the images that absolutely needs to be extracted from
            the patient's file. Keys are arbitrary names given to the images we want to add and values are lists of
            series descriptions. The images associated with these series descriptions do not need to have a
            corresponding segmentation. In fact, the whole point of adding a way to specify the series descriptions that
            must be added to the dataset is to be able to add images without segmentation.
        verbose : bool
            True to log/print some information else False.

        Attributes
        ----------
        self._images_data : List[ImageDataModel]
            A list of the patient's images data.
        """
        self._path_to_images_folder = path_to_images_folder
        self._path_to_segmentations_folder = path_to_segmentations_folder
        self._series_descriptions = series_descriptions
        self._verbose = verbose

        dicom_reader = DicomReader(path_to_images_folder=self._path_to_images_folder)
        self._images_data = dicom_reader.get_images_data(self._verbose)

    @property
    def patient_name(self) -> str:
        """
        Patient name.

        Returns
        -------
        patient_name : str
            Patient name.
        """
        patient_name = self._images_data[0].dicom_header.PatientName

        return str(patient_name)

    @property
    def _paths_to_segmentations(self) -> List[str]:
        """
        A list of paths to the segmentation files.

        Returns
        -------
        paths_to_segmentations : List[str]
            A list of paths to the segmentation files.
        """
        paths_to_segmentations = []
        for segmentation_filename in os.listdir(self._path_to_segmentations_folder):
            path_to_dicom_folder = os.path.join(self._path_to_segmentations_folder, segmentation_filename)
            paths_to_segmentations.append(path_to_dicom_folder)

        return paths_to_segmentations

    @abstractmethod
    def create_patient_data(self) -> PatientDataModel:
        """
        Creates a tuple containing all the patient's data.

        Returns
        -------
        patient_data: PatientDataModel
            Patient data.
        """
        pass
