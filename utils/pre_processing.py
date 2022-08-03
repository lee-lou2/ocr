import logging

import numpy as np
import cv2


class ImagePreprocessing:
    def __init__(self, image):
        self.kernel = np.ones((5, 5), np.uint8)
        self.post_gray_scale = False
        self.image = image

    def gray_scale(self):
        """그레이 변환"""
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.post_gray_scale = True
        return self

    def image_threshold(self):
        """대비"""
        if self.post_gray_scale:
            self.image = cv2.threshold(
                self.image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
            )[1]
        else:
            logging.warning("그레이 전환(gray_scale)이 선행 되어야 합니다")
        return self

    def remove_noise(self, kernel_size=5):
        """노이즈 제거"""
        self.image = cv2.medianBlur(self.image, ksize=kernel_size)
        return self

    def dilation(self):
        """팽창 - 인식된 이미지의 0이 아니면 모두 채움"""
        self.image = cv2.dilate(self.image, self.kernel, iterations=1)
        return self

    def erosion(self):
        """침식 - 겹쳐지는 부분에 하나라도 0이 있으면 제거"""
        self.image = cv2.erode(self.image, self.kernel, iterations=1)
        return self

    def opening(self):
        """열기 - 잡티나 작게 튀어나온 것들을 제거"""
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_OPEN, self.kernel)
        return self

    def closing(self):
        """닫기 - 전체적인 윤곽을 도드라지게 하는 효과"""
        self.image = cv2.morphologyEx(self.image, cv2.MORPH_CLOSE, self.kernel)
        return self

    def canny(self):
        """canny edge detection"""
        self.image = cv2.Canny(self.image, 100, 200)

    def deskew(self):
        """skew correction"""
        coords = np.column_stack(np.where(self.image > 0))
        angle = cv2.minAreaRect(coords)[-1]
        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle
        (h, w) = self.image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        self.image = cv2.warpAffine(
            self.image,
            M,
            (w, h),
            flags=cv2.INTER_CUBIC,
            borderMode=cv2.BORDER_REPLICATE,
        )

    def match_template(self, template):
        """template matching"""
        self.image = cv2.matchTemplate(self.image, template, cv2.TM_CCOEFF_NORMED)
