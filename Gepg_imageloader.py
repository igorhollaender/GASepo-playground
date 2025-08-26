#
#   G e p g _ i m a g e l o a d e r . p y
#
#   Last Update: IH250826
# 
# 
#
# ------------------------------------------
#   Notes:
# ------------------------------------------

import cv2
import numpy as np
from PIL import Image
import plotly.express as px
import streamlit as st


class GelImageLoader:
    def __init__(self):
        self.gel_image_uploaded = None
        self.gel_image_bytes = None
        self.gel_image_CV = None
        self.gel_image_16bit_normalized = None
        self.gel_image_8bit = None
        self.load_image()

    def load_image(self):
        self.gel_image_uploaded = st.file_uploader(
                "Upload a gel image file", 
                type=["tif","tiff"]
        )

        if self.gel_image_uploaded is None:
            st.button("Upload predefined test file",on_click=self.load_predefined_test_image)

        if self.gel_image_uploaded is None:
            st.stop()            

        self.gel_image_bytes = np.asarray(bytearray(self.gel_image_uploaded.read()), dtype=np.uint8)
        self.gel_image_CV = cv2.imdecode(self.gel_image_bytes, cv2.IMREAD_UNCHANGED)           

        if self.gel_image_CV is None:
            st.error("Failed to read image. Make sure it's a valid 16-bit TIFF.")
            st.stop()
        
        st.write(f"Image shape: {self.gel_image_CV.shape}, dtype: {self.gel_image_CV.dtype}")

        # Normalize for display (Streamlit/PIL can't show 16-bit directly)
        self.gel_image_16bit_normalized = cv2.normalize(self.gel_image_CV, None, 0, 255, cv2.NORM_MINMAX)
        self.gel_image_8bit = np.uint8(self.gel_image_16bit_normalized)
            
        # Convert to RGB if needed
        if len(self.gel_image_8bit.shape) == 2:
            st.image(self.gel_image_8bit, caption="16-bit Grayscale Image", width=300, use_container_width=False)
        else:
            st.image(cv2.cvtColor(self.gel_image_8bit, cv2.COLOR_BGR2RGB), caption="16-bit Color Image", width=300, use_container_width=False)
                
    #IH250826 TODO this does not work as expected, correction needed
    def load_predefined_test_image(self):
        # Load a predefined test image (for demo purposes)
        self.gel_image_CV = cv2.imread("resources/20240417_Gel1_10s_02.tif", cv2.IMREAD_UNCHANGED)
        if self.gel_image_CV is None:
            st.error("Failed to load predefined test image.")
            st.stop()
        self.gel_image_16bit_normalized = cv2.normalize(self.gel_image_CV, None, 0, 255, cv2.NORM_MINMAX)
        self.gel_image_8bit = np.uint8(self.gel_image_16bit_normalized)
        self.gel_image_uploaded = self.gel_image_CV             
        st.image(self.gel_image_8bit, caption="16-bit Grayscale Image (for testing)", width=300, use_container_width=False)
        
        