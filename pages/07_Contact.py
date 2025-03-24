import streamlit as st
import pandas as pd

# --- CONFIG PAGE ---
st.set_page_config(
    page_title="LOU Rugby - Contact",
    page_icon=":rugby_football:",
    layout="wide")

# --- SETUP PAGE ---
st.title("Contact title")

# --- FORMULAIRE DE CONTACT ---
with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
    Name=st.text_input(label='Votre nom') #Collect user feedback
    Email=st.text_input(label='Votre email') #Collect user feedback
    Message=st.text_input(label='Votre message') #Collect user feedback
    submitted = st.form_submit_button('Envoi')
    if submitted:
        st.write("Merci d'avoir pris contact. Nous réponderons dès que possible.") #Show a thankyou message once the form is submitted