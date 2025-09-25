#
#   G e p g _ s t a t e m a n a g e r . p y
#
#   Last Update: IH250903 
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
        if 'stored_state_buffer' not in st.session_state:
            st.session_state.stored_state_buffer = io.BytesIO()
        if 'buffer_filled' not in st.session_state:
            st.session_state.buffer_filled = False
        if 'use_stored_data' not in st.session_state:
            st.session_state.use_stored_data = False
  

    def save_state_to_pickle_and_download(self):
        
        for key in st.session_state:
            print(f"Storing {key}") 
        
        pickle.dump(st.session_state, st.session_state.stored_state_buffer)
        st.session_state.buffer_filled = True
        st.session_state.stored_state_buffer.seek(0)
        st.sidebar.download_button(
            label="Download State",
            data=st.session_state.stored_state_buffer,
            file_name="gasepo_playground_state.pkl",
            mime="application/octet-stream"
        )

    def load_state_from_pickle(self,file_path="gasepo_playground_state.pkl"):
        try:
            with open(file_path, "rb") as f:
                loaded_state = pickle.load(f)
                for key, value in loaded_state.items():
                    st.session_state[key] = value
                    st.write(f"Loaded {key}") 
        except FileNotFoundError:
            st.warning("No saved state found. Starting fresh!")

    def load_state_from_buffer(self):
        if st.session_state.stored_state_buffer is not {} and st.session_state.buffer_filled:
                st.write("Loading state from buffer...")
                loaded_state = pickle.load(st.session_state.stored_state_buffer)
                for key, value in loaded_state.items():
                    st.session_state[key] = value
                    print(f"Loaded {key}: value is {value}"[:80])
                st.session_state.stored_state_buffer.seek(0)  # Reset buffer pointer
        st.session_state.use_stored_data = True
        

    def reset_session_state(self):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.session_state.gel_image_uploaded = None  # Reset the uploaded image state
        st.session_state.buffer_filled = False
        st.session_state.use_stored_data = False
        st.write("Session state has been reset, stored status has been cleared.")

        st.rerun()
        
    def hasToUseStoredData(self):
        #IH250903 alternatively to using this class function, i is also possible to use
        # st.session_state.use_stored_data directly (for better readability) 
        return st.session_state.use_stored_data
     
    def finalize_streamlit_run(self):
        # has to be called at the end of the streamlit processing 
        st.session_state.use_stored_data = False