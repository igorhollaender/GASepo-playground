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

# Set up window
st.title("GASepo Playground Ver.250812e")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.sidebar.header("GASepo Playground Controls")

# Upload and prepare image data
gel_image_uploaded = st.file_uploader(
    "Upload a gel image file", 
    type=["tif","tiff"])
#
#if gel_image_uploaded is not None:
#    gel_image_bytes = gel_image_uploaded.getvalue()
#    gel_image_PIL = Image.open(io.BytesIO(gel_image_bytes))
#    gel_image_original = np.array(gel_image_PIL)   

if gel_image_uploaded is not None:
    # Convert uploaded file to bytes
    gel_image_bytes = np.asarray(bytearray(gel_image_uploaded.read()), dtype=np.uint8)

    # Read image using OpenCV with unchanged depth
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



#-------------------------------------------

# #



#     # convert RGBA/RGB to BGR for OpenCV
#     if gel_image_PIL.mode == 'RGBA':  # IH250812 check this!!!
#         gel_image_BGR = cv2.cvtColor(np.array(gel_image_PIL), cv2.COLOR_RGBA2BGR)
#     else:
#         gel_image_BGR = cv2.cvtColor(np.array(gel_image_PIL), cv2.COLOR_RGB2BGR)
    
#     st.image(gel_image_PIL, caption="Gel Image", use_container_width=True)
    
else:
    st.write("Please upload a gel image file to proceed")
    
