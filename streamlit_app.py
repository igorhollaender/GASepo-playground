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

    # ---- get image

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
                st.image(gel_image_display, caption="16-bit Grayscale Image", width=300, use_container_width=False)
            else:
                st.image(cv2.cvtColor(gel_image_display, cv2.COLOR_BGR2RGB), caption="16-bit Color Image", width=300, use_container_width=False)
    else:
        st.write("Please upload a gel image file to proceed")
    
    # prepare canvas_1 for drawing

    canvas_1_height, canvas_1_width = gel_image_display.shape[:2]
    # Scale canvas for display if image is too wide
    if canvas_1_width > 800:  #IH250812 HEURISTIC
        aspect_ratio = canvas_1_height / canvas_1_width
        canvas_1_width = 800
        canvas_1_height = int(canvas_1_width * aspect_ratio)

    canvas_1 = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=2,
        stroke_color="#FFA500",
        background_image=gel_image_display,
        # update_streamlit=realtime_update, # Enable real-time updates only for the 3rd point
        height=canvas_1_height,  #IH250812 NOT ACTIVE FOR NOW
        width=canvas_1_width,   # IH250812 NOT ACTIVE FOR NOW
        use_container_width=True,
        drawing_mode="point",
        # initial_drawing=initial_drawing if initial_drawing["objects"] else None,
        key="canvas_1",
    )


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