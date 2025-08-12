#
#   G A S e p o  P l a y g r o u n d
#
#   Last Update: IH250812
#
#

import cv2
import numpy as np
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas

# Set up window
st.title("GASepo Playground Ver.250812c")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
st.sidebar.header("GASepo Playground Controls")

# Upload and prepare image data
gel_image_uploaded = st.file_uploader(
    "Upload a gel image file", 
    type=["jpg", "jpeg", "png","tiff","tif"])
if gel_image_uploaded is not None:
    st.image(gel_image_uploaded, caption="Gel Image", use_container_width=True)
    gel_image_PIL = Image.open(gel_image_uploaded)
    gel_image_original = np.array(gel_image_PIL)   
    # convert RGBA/RGB to BGR for OpenCV
    if gel_image_PIL.mode == 'RGBA':  # IH250812 check this!!!
        gel_image_BGR = cv2.cvtColor(np.array(gel_image_PIL), cv2.COLOR_RGBA2BGR)
    else:
        gel_image_BGR = cv2.cvtColor(np.array(gel_image_PIL), cv2.COLOR_RGB2BGR)
else:
    st.write("Please upload a gel image file to proceed")
    
