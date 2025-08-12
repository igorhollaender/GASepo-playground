#
#   G A S e p o  P l a y g r o u n d
#
#   Last Update: IH250812
#
#

import cv2
import io
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

GASepoPG_version = "250812f"

def main():
    gel_image_uploaded = st.file_uploader(
        "Upload a gel image file", 
        type=["tif","tiff"])
   
    if gel_image_uploaded is not None:
        gel_image_bytes = np.asarray(bytearray(gel_image_uploaded.read()), dtype=np.uint8)
        gel_image_CV = cv2.imdecode(gel_image_bytes, cv2.IMREAD_UNCHANGED)

        if gel_image_CV is None:
            st.error("Failed to read image. Make sure it's a valid 16-bit TIFF.")
        else:
            st.write(f"Image shape: {gel_image_CV.shape}, dtype: {gel_image_CV.dtype}")

            # Normalize for display (Streamlit/PIL can't show 16-bit directly)
            gel_image_normalized = cv2.normalize(gel_image_CV, None, 0, 255, cv2.NORM_MINMAX)
            gel_image_display = np.uint8(gel_image_normalized)

            # Convert to RGB if needed
            if len(gel_image_display.shape) == 2:
                st.image(gel_image_display, caption="16-bit Grayscale Image", use_container_width=True)
            else:
                st.image(cv2.cvtColor(gel_image_display, cv2.COLOR_BGR2RGB), caption="16-bit Color Image", use_container_width=True)
    else:
        st.write("Please upload a gel image file to proceed")
    

#----------
if __name__ == "__main__":
    st.set_page_config(
        page_title="GASepo Playground",
        page_icon=":rocket:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title(f"GASepo Playground Ver.{GASepoPG_version}")
    st.sidebar.header("GASepo Playground Controls")
    main()