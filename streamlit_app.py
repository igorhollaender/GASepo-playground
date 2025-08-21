#
#   G A S e p o  P l a y g r o u n d
#
#   Last Update: IH250821
#
#

# ------------------------------------------
#   Notes:
#       to activate requirements.txt update:
#           visit https://share.streamlit.io/,
#           select your app, goto (...) and select Reboot  
#
#       to activate requirements.txt update in github codespace:
#           1. stop the server (Ctrl+C in terminal)
#           2. run `pip install -r requirements.txt` in terminal
#           3. restart the server (run streamlit_app.py)
#              or use the full command:
#                streamlit run streamlit_app.py --server.enableCORS false --server.enableXsrfProtection false
#
# ------------------------------------------
#   IMPORTANT:
#       for drawing_canvas to work properly, you need to use
#       streamlit version 1.40 (1.42 does not work).
#       and drawing_canvas version 0.9.2.  (0.9.3 does not work).
# ------------------------------------------


import cv2
import io
import numpy as np
import pickle
from PIL import Image
import plotly.express as px
import streamlit as st
from streamlit_drawable_canvas import st_canvas
# from streamlit_cropper import st_cropper #IH

GASepoPG_version = "250821c"
  
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

    # File uploader for gel image
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
                
            # prepare canvas_1 for drawing

            canvas_1_height, canvas_1_width = gel_image_display.shape[:2]
            # Scale canvas for display if image is too wide
            if canvas_1_width > 800:  #IH250812 HEURISTIC
                aspect_ratio = canvas_1_height / canvas_1_width
                canvas_1_width = 800
                canvas_1_height = int(canvas_1_width * aspect_ratio)

            background_image = Image.fromarray(220-gel_image_display) # IH250821 invert image for better visibility on canvas
                           #IH250821 EXPERIMENTAL enhance high bands (thats why we use 200 and not 255)
            
            canvas_1 = st_canvas(

                fill_color="rgba(255, 165, 0, 0.3)",
                stroke_width=2,
                stroke_color="#FCE21B",
                background_image = background_image,
                update_streamlit=True, 
                height=canvas_1_height,
                width=canvas_1_width, 
                drawing_mode="transform",
                initial_drawing=canvas_1_initial_drawing(background_image,canvas_1_width,canvas_1_height),
                key="canvas_1",
                )
            
            # st.write(f"Canvas (json_data): {canvas_1.json_data}") 
            st.write(f"ROI:  " + 
                     f"left: {canvas_1.json_data['objects'][0]['left']},   " +
                     f"top: {canvas_1.json_data['objects'][0]['top']},   " +
                     f"width: {canvas_1.json_data['objects'][0]['width']},   " +
                     f"height: {canvas_1.json_data['objects'][0]['height']},   " +
                     f"angle: {canvas_1.json_data['objects'][0]['angle']},   " +
                       "")
            #IH250821 we assume the first object to be the expected ROI 

            
    else:
        st.write("Please upload a gel image file to proceed")
    
    


    
    

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
    

def canvas_1_initial_drawing(image: Image.Image, canvas_width: int, canvas_height):
     return {
     'version': '4.4.0', 
     'objects': [
         {
         'type': 'rect', 
         'version': '4.4.0', 
         'originX': 'left', 'originY': 'top', 
            'left': canvas_width*(0.5-0.04/2),   
            'top': canvas_height*0.2, 
            'width': canvas_width*0.04,
            'height': canvas_height*0.65, 
         'fill': 'rgba(255, 165, 0, 0.3)', 
         'stroke': '#FCE21B', 
            'strokeWidth': 2, 
            'strokeDashArray': None, 
            'strokeLineCap': 'butt', 
            'strokeDashOffset': 0, 
            'strokeLineJoin': 'miter', 
            'strokeUniform': True, 
            'strokeMiterLimit': 4, 
        'scaleX': 1, 'scaleY': 1, 
        'angle': 0, 
        'flipX': False, 'flipY': False, 
        'opacity': 1, 
        'shadow': None, 
        'visible': True, 
        'backgroundColor': '', 
        'fillRule': 'nonzero', 
        'paintFirst': 'fill', 
        'globalCompositeOperation': 
        'source-over', 
        'skewX': 0, 'skewY': 0, 
        'rx': 0, 'ry': 0}]}

#----------
if __name__ == "__main__":
    
    main()