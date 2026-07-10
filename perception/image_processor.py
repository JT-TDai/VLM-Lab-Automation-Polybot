import cv2
import numpy as np
import logging

class ImageProcessor:
    def __init__(self, roi_coords, apply_contrast_norm=True):
        # roi_coords: [x, y, w, h]
        self.x, self.y, self.w, self.h = roi_coords
        self.apply_contrast_norm = apply_contrast_norm
        logging.info("ImageProcessor initialized with ROI: %s", roi_coords)

    def capture_frame(self):
        # For demonstration, we create a dummy blank image simulating a 1080p camera
        img = np.zeros((1080, 1920, 3), dtype=np.uint8)
        # Draw a mock number in the ROI
        cv2.putText(img, "148.5", (self.x + 20, self.y + 50), 
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (200, 255, 200), 3)
        return img

    def preprocess_for_vlm(self, frame):
        # 1. ROI Extraction
        roi = frame[self.y : self.y + self.h, self.x : self.x + self.w]
        
        # 2. Contrast Normalization (Optional, based on config)
        if self.apply_contrast_norm:
            # Convert to grayscale for contrast adjustment
            gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
            # Apply CLAHE (Contrast Limited Adaptive Histogram Equalization)
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            enhanced_gray = clahe.apply(gray)
            # Convert back to BGR to maintain compatibility with standard VLM inputs
            processed_roi = cv2.cvtColor(enhanced_gray, cv2.COLOR_GRAY2BGR)
        else:
            processed_roi = roi
            
        return processed_roi
