import streamlit as st
import os
import pyrebase
from firebase_admin import credentials
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

from pdf_merger import pdf_merger
from splitter import splitter
from add_filters import add_to_dropdown
from Filters import Filters

#-----------------Streamlit Config-----------------#
st.set_page_config(
    page_title='POP Dashboard',
    page_icon='Pop Icon.ico'
)

#-----------------Firebase Auth-----------------#
admin_cred = credentials.Certificate('Firebase Admin SDK.json')
# firebase_admin.initialize_app(admin_cred)

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

#-----------------Google API Setup-----------------#
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = Credentials.from_service_account_file('service_credentials.json', scopes=SCOPES)
sheets_service = build('sheets', 'v4', credentials=creds)
drive_service = build('drive', 'v3', credentials=creds)

#-----------------Main App-----------------#
def main():
    with st.sidebar:
        selected_screen = st.selectbox(
            "Select an option",
            ["PDF Merger", "Splitter", "Manage Dropdowns"]
        )

    filterData = Filters()

    if selected_screen == "PDF Merger":
        st.header("PDF Merger")

        # Load dropdowns from JSON, **no add inputs shown here**
        practice_tests = filterData.practice_tests
        difficulty = filterData.difficulty
        category = filterData.category
        sub_category_one = filterData.sub_category_one
        sub_category_two = filterData.sub_category_two
        sub_category_three = filterData.sub_category_three
        calculator = filterData.calculator

        pdf_merger(
            sheets_service=sheets_service,
            drive_service=drive_service,
            practice_tests=practice_tests,
            difficulty=difficulty,
            category=category,
            sub_category_one=sub_category_one,
            sub_category_two=sub_category_two,
            sub_category_three=sub_category_three,
            calculator=calculator
        )

    elif selected_screen == "Splitter":
        st.header("Splitter")
        splitter()

    else:  # Manage Dropdowns page
        st.header("Manage Dropdowns")

        # On this page, show input boxes to **add new dropdown values**
        add_to_dropdown('practice_tests', 'dropdowns/practice_tests.json', filterData.practice_tests)
        add_to_dropdown('difficulty', 'dropdowns/difficulty.json', filterData.difficulty)
        add_to_dropdown('category', 'dropdowns/category.json', filterData.category)
        add_to_dropdown('sub_category_one', 'dropdowns/sub_category_one.json', filterData.sub_category_one)
        add_to_dropdown('sub_category_two', 'dropdowns/sub_category_two.json', filterData.sub_category_two)
        add_to_dropdown('sub_category_three', 'dropdowns/sub_category_three.json', filterData.sub_category_three)
        add_to_dropdown('calculator', 'dropdowns/calculator.json', filterData.calculator)


if __name__ == "__main__":
    main()
