import streamlit as st

# --- SETUP PAGE ---
def page_contact():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-envelope"></i> Contact</h1>
    """, unsafe_allow_html=True)
    st.write("""
    ## Contactez-nous
    
    Pour toute question ou suggestion, n'hésitez pas à nous contacter.
    
    ### Informations de Contact
        - Adresse : 405 Avenue Jean Jaurès, Lyon 69007
        - Tél : +33 (0)4 78 00 81 90
        - Mail : association@lourugby.fr

    Heures d’ouverture : Du lundi au vendredi : 9h00–12h00  14h00–18h00
    """)
    
    # --- FORMULAIRE DE CONTACT ---
    with st.form(key='columns_in_form2',clear_on_submit=True): #set clear_on_submit=True so that the form will be reset/cleared once it's submitted
        Name=st.text_input(label='Votre nom') #Collect user feedback
        Email=st.text_input(label='Votre email') #Collect user feedback
        Message=st.text_input(label='Votre message') #Collect user feedback
        submitted = st.form_submit_button('Envoi')
        if submitted:
            st.write("Merci d'avoir pris contact. Nous réponderons dès que possible.") #Show a thankyou message once the form is submitted