import streamlit as st

# Function to display the main page with buttons
def main_page():
    st.title("Welcome")
    if st.button('Restaurant Optimizer'):
        st.session_state.page = 'optimizer'
        st.rerun()
    if st.button('Single Simulation'):
        st.session_state.page = 'simulator'
        st.rerun()

# Function to display the horses page
def optimizer_page():
    st.title("Restaurant Optimizer")
    st.write("Here is some information about horses.")
    if st.button('Back'):
        st.session_state.page = 'main'
        st.rerun()

# Function to display the cows page
def simulator_page():
    st.title("Single Simulation")
    st.write("Here is some information about cows.")
    if st.button('Back'):
        st.session_state.page = 'main'
        st.rerun()

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'main'

# Navigation logic
if st.session_state.page == 'main':
    main_page()
elif st.session_state.page == 'optimizer':
    optimizer_page()
elif st.session_state.page == 'simulator':
    simulator_page()