#
#
#   G e p g _ m a i n . p y
#
# ------------------------------------------
#   G A S e p o  P l a y g r o u n d  Main
#
#   Last Update: IH250828
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
from Gepg_ROIselector import ROISelector    
from Gepg_statemanager import StateManager
from Gepg_laneprofilepresenter import LaneProfilePresenter 


GASepoPG_version = "250828a"
  
uploaded_buffer = None
stateManager = StateManager()   

def main():

    # ---- initialize session state

    if 'gel_image_uploaded' not in st.session_state:   
        st.session_state.gel_image_uploaded = None

    Gepg_GUIsetup()
    gel_image_loader = None
    gel_image_lane = None

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

    st.session_state.gel_image_lane = []    
    for lane_index in range(len(ROI_selector.lane_ROI)):
        st.session_state.gel_image_lane.append(ROI_selector.crop_rotated_rect(
            image=gel_image_loader.gel_image_8bit,
            centerleft  =  ROI_selector.get_ROIcenter_X(lane_index), #IH250821 we assume the first object to be the expected ROI 
                                                            #IH250825 TODO generalize for multiple lanes
            centertop   =  ROI_selector.get_ROIcenter_Y(lane_index),
            width       =  ROI_selector.get_ROIwidth(lane_index),
            height      =  ROI_selector.get_ROIheight(lane_index),
            angle       =  ROI_selector.get_ROIangle(lane_index)
        ))
    
    with st.expander("Lane Viewer"):
        cols = st.columns(3)  #IH250826 max 3 lanes supported for now
        for c in range(3):  
            cols[c].image(st.session_state.gel_image_lane[c], width=st.session_state.gel_image_lane[c].shape[1]//2) 
            lane_stroke = ROI_selector.get_ROIstyle(lane_index=c)['stroke']
            cols[c].write(f'<span style="background-color:{lane_stroke}; color:white">&nbsp;L{c+1}&nbsp;</span>', unsafe_allow_html=True)

    with st.expander("Lane Profile Plotter"):
        for c in range(3):  
            lane_profile_presenter = LaneProfilePresenter(st.session_state.gel_image_lane[c])
            fig = lane_profile_presenter.plot_image_and_column_sums() 
            st.plotly_chart(fig, use_container_width=True)



def Gepg_GUIsetup():

    global stateManager
    
    st.set_page_config(
        page_title="GASepo Playground",
        page_icon=":rocket:",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.title(f"GASepo Playground")
    st.subheader(f"Ver.{GASepoPG_version}")
    st.write('<span style="color:red">This is an experimental platform. Do not use for real analysis!</span>', unsafe_allow_html=True)

    st.sidebar.header("GASepo Playground Controls")
    if st.sidebar.button("Store status"):
        stateManager.save_state_to_pickle_and_download()
        st.sidebar.write("Status stored successfully!")
    if st.sidebar.button("Load recent status"):
        stateManager.load_state_from_pickle()
        st.sidebar.write("Status loaded successfully!")
    if st.sidebar.button("Load status from file"):
        global uploaded_buffer
        uploaded_buffer = st.sidebar.file_uploader(
            type=["pkl", "pickle"],
            label="Upload a saved state file",
            on_change=stateManager.load_state_from_buffer 
        )
        st.sidebar.write("Status loaded successfully!")
    if st.sidebar.button("Reset"):
        stateManager.reset_session_state()
        st.sidebar.write("Status reset successfully!")
    if st.sidebar.button("About"): 
        st.sidebar.write(
            "This is a playground for development of GASepo, a tool for analyzing gel electrophoresis images. "
            "You can upload images, draw on them, and explore various features."
        )
        
               
  
#----------
if __name__ == "__main__":
    
    main()