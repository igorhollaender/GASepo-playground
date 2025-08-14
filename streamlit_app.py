#
#   G A S e p o  P l a y g r o u n d
#
#   Last Update: IH250814
#
#

# ------------------------------------------
#   Notes:
#       to activate requirements.txt update:
#           visit https://share.streamlit.io/,
#           select your app, goto (...) and select Reboot  
#
# ------------------------------------------


import cv2
import io
import numpy as np
import pickle
from PIL import Image
import streamlit as st
from streamlit_drawable_canvas import st_canvas
from streamlit_cropper import st_cropper

GASepoPG_version = "250814e"
  
uploaded_buffer = None  

def main():

    # ---- initialize session state
    
    if 'gel_image_uploaded' not in st.session_state:   
        st.session_state.gel_image_uploaded = None

    # ---- set up GUI

    st.set_page_config(
        page_title="GASepo Playground",
        page_icon=":rocket:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title(f"GASepo Playground Ver.{GASepoPG_version}")
    st.sidebar.header("GASepo Playground Controls")
    if st.sidebar.button("Store status"):
        save_state_to_pickle_and_download()
        st.sidebar.write("Status stored successfully!")
    if st.sidebar.button("Load recent status"):
        load_state_from_pickle()
        st.sidebar.write("Status loaded successfully!")
    if st.sidebar.button("Load status from file"):
        global uploaded_buffer
        uploaded_buffer = st.sidebar.file_uploader(
            type=["pkl", "pickle"],
            label="Upload a saved state file",
            on_change=load_state_from_buffer 
        )
        st.sidebar.write("Status loaded successfully!")
    if st.sidebar.button("Reset"):
        reset_session_state()
        st.sidebar.write("Status reset successfully!")
    if st.sidebar.button("About"): 
        st.sidebar.write(
            "This is a playground for development of GASepo, a tool for analyzing gel electrophoresis images. "
            "You can upload images, draw on them, and explore various features."
        )
    


    # ---- get image

    gel_image_uploaded_temp = st.file_uploader(
            "Upload a gel image file", 
            type=["tif","tiff"]
    )

        
    if gel_image_uploaded_temp is not None:
        st.session_state.gel_image_uploaded = gel_image_uploaded_temp
        gel_image_bytes = np.asarray(bytearray(st.session_state.gel_image_uploaded.read()), dtype=np.uint8)
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
    
            gel_image_cropped = st_cropper(gel_image_CV)
            st.write("Cropped image dimensions:", gel_image_cropped.shape)
    else:
        st.write("Please upload a gel image file to proceed")
    
    

    # prepare canvas_1 for drawing

    # canvas_1_height, canvas_1_width = gel_image_display.shape[:2]
    # # Scale canvas for display if image is too wide
    # if canvas_1_width > 800:  #IH250812 HEURISTIC
    #     aspect_ratio = canvas_1_height / canvas_1_width
    #     canvas_1_width = 800
    #     canvas_1_height = int(canvas_1_width * aspect_ratio)

    # canvas_1 = st_canvas(
    #     fill_color="rgba(255, 165, 0, 0.3)",
    #     stroke_width=2,
    #     stroke_color="#FFA500",
    #     background_image=gel_image_display,
    #     # update_streamlit=realtime_update, # Enable real-time updates only for the 3rd point
    #     height=canvas_1_height,  #IH250812 NOT ACTIVE FOR NOW
    #     width=canvas_1_width,   # IH250812 NOT ACTIVE FOR NOW
    #     use_container_width=True,
    #     drawing_mode="point",
    #     # initial_drawing=initial_drawing if initial_drawing["objects"] else None,
    #     key="canvas_1",
    # )


#---- state management
# using pickle format for storing session state

def save_state_to_pickle_and_download():
    buffer = io.BytesIO()
    pickle.dump(st.session_state, buffer)
    buffer.seek(0)
    st.sidebar.download_button(
        label="Download State",
        data=buffer,
        file_name="gasepo_playground_state.pkl",
        mime="application/octet-stream"
    )

def load_state_from_pickle(file_path="gasepo_playground_state.pkl"):
    try:
        with open(file_path, "rb") as f:
            loaded_state = pickle.load(f)
            for key, value in loaded_state.items():
                st.session_state[key] = value
                st.write(f"Loaded {key}: value is {value}") 
    except FileNotFoundError:
        st.warning("No saved state found. Starting fresh!")

def load_state_from_buffer():
    global uploaded_buffer
    if uploaded_buffer is not None:
            loaded_state = pickle.load(uploaded_buffer)
            for key, value in loaded_state.items():
                st.session_state[key] = value
                st.write(f"Loaded {key}: value is {value}")


def reset_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.session_state.gel_image_uploaded = None  # Reset the uploaded image state
    st.write("Session state has been reset.")
    
#----------
if __name__ == "__main__":
    
    main()