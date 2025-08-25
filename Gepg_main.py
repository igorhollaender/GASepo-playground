#
#
#   G e p g _ m a i n . p y
#
# ------------------------------------------
#   G A S e p o  P l a y g r o u n d  Main
#
#   Last Update: IH250825
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

from Gepg_imageloader import GelImageLoader
from Gepg_RIOselector import ROISelector    


GASepoPG_version = "250825b"
  
uploaded_buffer = None  

def main():

    # ---- initialize session state
    if 'gel_image_uploaded' not in st.session_state:   
        st.session_state.gel_image_uploaded = None

    Gepg_GUIsetup()

    with st.expander("Image Upload"):
        gel_image_loader = GelImageLoader()
        if gel_image_loader.gel_image_uploaded is  None:
            st.stop()  # Stop execution if no image is uploaded 
        st.session_state.gel_image_uploaded = gel_image_loader.gel_image_uploaded

    # with st.expander("Lane selector"):  
    #IH250825 WORKAROUND for some issue with streamlit_drawable_canvas, the canvas 
    # is not working properly if placed directly in the expander

    ROI_selector = ROISelector(gel_image_8bit=gel_image_loader.gel_image_8bit)
    ROI_selector.select_ROI() 
      
    with st.expander("Testing Plotly"): 
        TestingPlotly()


def Gepg_GUIsetup():

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
        
    

def TestingPlotly():
    # testing plotly
    fig = px.line (x=[1,2,3,4,5,6,7,8,9,10],
                y=[10,20,30,40,50,60,70,80,90,100])

    st.plotly_chart(fig, use_container_width=True)
               
    

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