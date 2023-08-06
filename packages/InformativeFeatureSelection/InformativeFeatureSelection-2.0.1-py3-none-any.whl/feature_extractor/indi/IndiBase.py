from abc import ABC, abstractmethod
from typing import List, Tuple

import cv2
import numpy as np


class BaseINDI(ABC):

    @abstractmethod
    def process(self, data: List[np.ndarray], **kwargs) -> Tuple[int, int]:
        """
        :param data: list of length(n_classes) of numpy arrays of shape (n_samples, n_features)
        :return: indices of the two of the most relevant features in binary case
        """
        pass

    def process_from_image(self, image: np.ndarray, mask: np.ndarray) -> List[int]:
        """
        :param image: numpy array of shape (H, W, C)
        :param mask: numpy array which consist labels for the corresponding image. Zero values are ignored
        (background class)
        :return: indices of the two of the most relevant features
        """
        labels = np.unique(mask)
        data = []
        for label in labels:
            if label == 0:
                continue
            coords = (mask == label)
            class_values = image[coords]
            data.append(class_values)
        return self.process(data)

    def process_from_points(self, image: np.ndarray, points: List[List[List[int]]], labels: List[int]) -> List[int]:
        """
        :param image: numpy array of shape (H, W, C)
        :param points: list (polygons) of list (points) of lists (coords) with two coordinates of polygon which
        highlights class object
        :param labels: list of class labels for the corresponding polygon from "points"
        :return: indices of the two of the most relevant features
        """
        points = [self._convert_to_cv2_points(p) for p in points]
        mask = self._convert_polygons_to_mask(points, labels, image.shape[:2])
        return self.process_from_image(image, mask)

    def _convert_to_cv2_points(self, list_of_points: List[List[int]]) -> List[np.ndarray]:
        """
        Since cv2.fillPoly does not work with list of lists we should to convert points lists in np.ndarray with type
        np.int32
        :note use this method in pair with "_convert_polygons_to_mask"
        """
        cv2_formatted_points = []
        for points in list_of_points:
            points = np.array(points, dtype=np.int32)
            cv2_formatted_points.append(points)

        return cv2_formatted_points

    def _convert_polygons_to_mask(
            self,
            polygons: List[List[np.ndarray]],
            labels: List[int],
            mask_shape: Tuple[int]
    ) -> np.ndarray:
        assert len(polygons) == len(labels), "Number of polygons and corresponding number of labels should be equal"
        gt = np.zeros(mask_shape, dtype=np.uint8)
        for poly, label in zip(polygons, labels):
            gt = cv2.fillPoly(gt, poly, color=label)
        return gt
