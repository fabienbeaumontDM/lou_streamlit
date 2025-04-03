import streamlit as st
import streamlit_antd_components as sac
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# --- SETUP PAGE ---
def page_contact():
    st.markdown("""
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons/font/bootstrap-icons.css">
    <h1><i class="bi bi-envelope"></i> Contact</h1>
    """, unsafe_allow_html=True)

    # Avertissement
    sac.alert(label='En construction',
              description='Ce site est encore en cours de développement. Certaines fonctionnalités peuvent ne pas fonctionner comme prévu.',
              size='lg',
              radius='lg',
              variant='filled',
              color='red',
              banner=True,
              icon=True,
              closable=True)

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
    with st.form(key='columns_in_form2', clear_on_submit=True):  # Formulaire avec réinitialisation après soumission
        Name = st.text_input(label='Votre nom')  # Collecter le nom de l'utilisateur
        Email = st.text_input(label='Votre email')  # Collecter l'email de l'utilisateur
        Message = st.text_area(label='Votre message', height=150)  # Zone de texte plus grande pour le message
        submitted = st.form_submit_button('Envoi')

        if submitted:
            # Configuration de l'email
            sender_email = "fbeaumont.ecully@gmail.com"  # Remplacez par votre adresse mail
            sender_password = "Baptiste141004#"  # Remplacez par votre mot de passe mail
            recipient_email = "fbeaumont.ecully@gmail.com"  # Adresse de destination

            subject = f"Message de {Name} via le formulaire de contact"
            body = f"Nom : {Name}\nEmail : {Email}\n\nMessage :\n{Message}"

            # Créer l'email
            msg = MIMEMultipart()
            msg["From"] = sender_email
            msg["To"] = recipient_email
            msg["Subject"] = subject
            msg.attach(MIMEText(body, "plain"))

            try:
                # Envoyer l'email via le serveur SMTP de Gmail
                with smtplib.SMTP("smtp.gmail.com", 587) as server:
                    server.starttls()  # Sécuriser la connexion
                    server.login(sender_email, sender_password)  # Connexion au compte Gmail
                    server.sendmail(sender_email, recipient_email, msg.as_string())  # Envoyer l'email

                st.success("Votre message a été envoyé avec succès !")
            except Exception as e:
                st.error(f"Une erreur s'est produite lors de l'envoi de l'email : {e}")