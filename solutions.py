import streamlit as st
import sys
import gspread
import requests
import os
import streamlit_authenticator as stauth
import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
from PIL import Image
import pyrebase


def solutions_packet():
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




    st.title("Solutions Packet")
    default_sheet = "Practice Test Analysis!C2:C40"
    range_name = st.text_input("Enter the name of the sheet and the range of cells you want to download:"
                            ,value = default_sheet)
    default_URL = "https://docs.google.com/spreadsheets/d/1RjkWwLxLb9dk8OjNYY6CwxTw4NXOaTO955qKuslNgBE/edit#gid=0"
    range_name = range_name.upper()
    spreadsheet_url = st.text_input("Enter the URL of the spreadsheet:"
                                    ,value = default_URL)
    spreadsheet_id = spreadsheet_url.split('/')[-2]
    names = [
    "Adriana Vingerhoets", "Aanya Naipaul", "Adriana Vingerhoets", "Alejandro Moreno",
    "Andrea Murzi", "Andres Camargo", "Angelo Socarras", "Antonio De Castilho",
    "Arielle Socol", "Bella Morales", "Brigida Sarcona", "Camila Moran",
    "Cristina Macias", "Daisy Stein", "Daniel Esparragoza", "Daniel Sutton",
    "Daniela Duran", "Daniela Padron", "Daniella Vargas", "David Ramirez",
    "Diego Gutierrez", "Dylan Medina", "Eden Ohayon", "Elizabeth Chinea",
    "Emilia Sarcona", "Esteban Chiquito", "Fabiana Tejera", "Freddy Romero",
    "Gabriela Sobrinho", "Gabriella Alfonso", "Gabriella Suao", "Giovanna Musiello",
    "Isabella Torres", "Jade Shim-You", "Jett Pinkerton", "Jielianne Rodriguez",
    "Juan Rodriguez", "Julia Tavares", "Justin Cardenas", "Kirsten Chong",
    "Lauren Kettlewell", "Liam Lesentier", "Lily Quintero", "Lola Shaoul",
    "Lucas Delgado", "Melany Rodriguez", "Mia Vasquez", "Michelle Mendez",
    "Natalie Fernandez", "Nathaly Gonzalez Henriquez", "Nicholas Santiago",
    "Nicolas Alvarez", "Niya Bourdon", "Noah Gomberg", "Ofri Ezra", "Paula Cohen",
    "Paulina Baquero", "Roberto Gamarra", "Rocket Pinkerton", "Sabrina Bianco",
    "Sofia Aleman", "Sol Pereyra Lopez", "Sophia Loszynski", "Sydney Young",
    "Thomas Dos Santos Lara", "Timothy Kinigopoulo", "Tom Sela", "Valerie Duran",
    "Renan De Souza", "Zoe Mcmahon"
    ]
    student_name = st.selectbox("Select a student name:", names)
    if student_name:
        if st.button("Update Cell"):
            if update_sheet_cell(sheets_service, spreadsheet_id, "Dashboard!A1", student_name):
                st.success("Cell updated successfully!")
     



