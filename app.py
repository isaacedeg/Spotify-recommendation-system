import streamlit as st
from functions import *

def main():
    spr_sidebar()        
    if st.session_state.app_mode == 'Home':
        home_page()
    if st.session_state.app_mode == 'Result':
        result_page()
    if st.session_state.app_mode == 'About' :
        About_page()
# Run main()
if __name__ == '__main__':
    main()