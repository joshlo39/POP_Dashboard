import streamlit as st
import sys
import gspread
import requests
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
from PIL import Image
import pyrebase
from pdf_merger import pdf_merger
from solutions import solutions_packet 

#------------Configuring Streamlit--------#
st.set_page_config(
    page_title='POP Dashboard',  # Your app title
    page_icon='Pop Icon.ico'  # Path to your favicon
)
#------------Authentication--------------#
admin_cred = credentials.Certificate('Firebase Admin SDK.json')
#firebase_admin.initialize_app(admin_cred)

firebaseConfig = {
    "apiKey": "AIzaSyAsytsTB2K_PRrtkuxMA8s8cCaup-5Zedc",
    "authDomain": "streamlit-pop-pdfmerger.firebaseapp.com",
    "databaseURL": "https://streamlit-pop-pdfmerger-default-rtdb.firebaseio.com/",
    "projectId": "streamlit-pop-pdfmerger",
    "storageBucket": "streamlit-pop-pdfmerger.appspot.com",
    "messagingSenderId": "574365299032",
    "appId": "1:574365299032:web:86bd2a476ade31a8df352d",
    "measurementId": "G-G8KW4CQV60"
}


firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',]
creds = Credentials.from_service_account_file('service_credentials.json', scopes=SCOPES)
sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

def main():
    
    with st.sidebar:
        selected_screen = st.selectbox("Select an option", ["PDF Merger", "Solutions Packet"]) 
    if selected_screen == "PDF Merger":
        pdf_merger()
    else:
        solutions_packet()

if __name__ == "__main__":
    main()
