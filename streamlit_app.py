#
#   G A S e p o     P l a y g r o u n d
#
#   Last Update: IH250812
#
#

import streamlit as st
import cv2
from PIL import Image
from streamlit_drawable_canvas import st_canvas

st.title("GASepo Playground Ver.250812a")
st.write(
    "Let's start building! For help and inspiration, head over to [docs.streamlit.io](https://docs.streamlit.io/)."
)
gel_image_uploaded = st.file_uploader(
    "Upload a gel image file", 
    type=["jpg", "jpeg", "png","tiff","tif"])
if gel_image_uploaded is not None:
    st.image(gel_image_uploaded, caption="Gel Image", use_container_width=True)
else:
    st.write("Please upload a gel image file to proceed")
    
