#
#   G e p g _ s t a t e m a n a g e r . p y
#
#   Last Update: IH250825
# 
# 
#
# ------------------------------------------
#   Notes:
# ------------------------------------------

import io
import pickle
import streamlit as st

class StateManager:
# using pickle format for storing session state
#IH250825 TODO update 

    def __init__(self):
        pass

    def save_state_to_pickle_and_download(self):
        buffer = io.BytesIO()
        pickle.dump(st.session_state, buffer)
        buffer.seek(0)
        st.sidebar.download_button(
            label="Download State",
            data=buffer,
            file_name="gasepo_playground_state.pkl",
            mime="application/octet-stream"
        )

    def load_state_from_pickle(self,file_path="gasepo_playground_state.pkl"):
        try:
            with open(file_path, "rb") as f:
                loaded_state = pickle.load(f)
                for key, value in loaded_state.items():
                    st.session_state[key] = value
                    st.write(f"Loaded {key}: value is {value}") 
        except FileNotFoundError:
            st.warning("No saved state found. Starting fresh!")

    def load_state_from_buffer(self):
        global uploaded_buffer
        if uploaded_buffer is not None:
                loaded_state = pickle.load(uploaded_buffer)
                for key, value in loaded_state.items():
                    st.session_state[key] = value
                    st.write(f"Loaded {key}: value is {value}")


    def reset_session_state(self):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.gel_image_uploaded = None  # Reset the uploaded image state
        st.write("Session state has been reset.")
        
