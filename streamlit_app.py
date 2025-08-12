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
st.title("GASepo Playground Ver.250812d")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.sidebar.header("GASepo Playground Controls")

# Upload and prepare image data
gel_image_uploaded = st.file_uploader(
    "Upload a gel image file", 
    type=["tif","tiff","png","jpg", "jpeg"])
if gel_image_uploaded is not None:
    gel_image_bytes = gel_image_uploaded.getvalue()
    gel_image_PIL = Image.open(io.Bytes(gel_image_bytes))
    gel_image_original = np.array(gel_image_PIL)   

    # convert RGBA/RGB to BGR for OpenCV
    if gel_image_PIL.mode == 'RGBA':  # IH250812 check this!!!
        gel_image_BGR = cv2.cvtColor(np.array(gel_image_PIL), cv2.COLOR_RGBA2BGR)
    else:
        gel_image_BGR = cv2.cvtColor(np.array(gel_image_PIL), cv2.COLOR_RGB2BGR)
    
    st.image(gel_image_PIL, caption="Gel Image", use_container_width=True)
    
else:
    st.write("Please upload a gel image file to proceed")
    
