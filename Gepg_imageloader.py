#
#   G e p g _ i m a g e l o a d e r . p y
#
#   Last Update: IH250925
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
        if 'load_predefined_test_image' not in st.session_state:  
            st.session_state.load_predefined_test_image = False  

        self.gel_image_uploaded = None
        self.gel_image_bytes = None
        self.gel_image_CV = None
        self.gel_image_16bit_normalized = None
        self.gel_image_8bit = None
        self.load_image()

    def on_upload_change():
        st.session_state.load_predefined_test_image = False
        
    def load_image(self):
        self.gel_image_uploaded = st.file_uploader(
                "Upload a gel image file (16bit TIFF)", 
                type=["tif","tiff"],
                on_change=GelImageLoader.on_upload_change   
        )

        if st.button("Upload predefined test file"):
            st.session_state.load_predefined_test_image = True
            st.rerun()

        print(f"self.gel_image_uploaded =  {self.gel_image_uploaded}")
        print(f"st.session_state.use_stored_data =  {st.session_state.use_stored_data}")

        #if st.session_state.use_stored_data:
        #    self.gel_image_uploaded = st.session_state.gel_image_uploaded
        
        if self.gel_image_uploaded is not None:
            self.gel_image_bytes = np.asarray(bytearray(self.gel_image_uploaded.read()), dtype=np.uint8)
            self.gel_image_CV = cv2.imdecode(self.gel_image_bytes, cv2.IMREAD_UNCHANGED)
        elif st.session_state.load_predefined_test_image:
            self.gel_image_CV = cv2.imread("resources/20240417_Gel1_10s_02.tif", cv2.IMREAD_UNCHANGED)
            self.gel_image_uploaded = self.gel_image_CV 
        
        if self.gel_image_uploaded is None:
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
                
