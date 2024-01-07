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
from utils import * 
 
def pdf_merger():
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


    #------------Configuring Streamlit--------#
    st.title("Peace of Pi: PDF Merger")
    default_sheet = "Practice Exam Analysis!C218:C280"
    range_name = st.text_input("Enter the name of the sheet and the range of cells you want to download:"
                            ,value = default_sheet)
    default_URL = "https://docs.google.com/spreadsheets/d/1xilt_O28-BD4uSiXxIuOvczkDED04F2MIQK-imtpc48/edit#gid=0"
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
     
    #---------------Sidebar----------------#
    # student_names = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges="Templates!A2:A2", includeGridData=False).execute()
    # List of names

                    
                    
    #-----------------Settup--------------------#

    practice_tests = ["Ptest #1 (202003U)","Ptest #2 (202012A)","Ptest #3 (202010A)",
                    "Ptest #4 (202011U)","Ptest #5 (202012U)","Ptest #6 (202009U)",
                    "Ptest #7 (202010SD)","Ptest #8 (202010U)","Ptest #9 (202103A)","Ptest #10 (202103U)",
                    "Ptest #11 (201912U)","Ptest #12 (202009A)","Ptest #13 (202008A)","Ptest #14 (201911U)",
                    "Ptest #15 (202105U)","Ptest #16 (201905U)","Ptest #17 (201910U)","Ptest #18 (201905A)",
                    "Ptest #19 (201903U)","Ptest #20 (202105A)","Ptest #21 (202306U)","Ptest #22 (202304SD)",
                      "Ptest #23 (202305U)","D Practice Test #1", "D Practice Test #2", "D Practice Test #3"]
    

    sheet_name = range_name.split("!")[0]
    
    category_range = sheet_name + "!" + "K" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "K" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    difficulty_range = sheet_name + "!" + "I" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "I" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    section_range = sheet_name + "!" + "B" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "B" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    correctness_range = sheet_name + "!" + "D" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "D" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    test_range = sheet_name + "!" + "A" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "A" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    range_list = [category_range, difficulty_range, section_range, correctness_range,test_range]

    
    category = ["HOA","PSDA","PAM","GEOM"]
    difficulty = ["1","2","3","4","5"]
    correctness = {
        "Correct":"1",
        "Incorrect":"0"
        }
    section = ["1","2","2E","2H","3","4"]
    
    st.subheader("Filters")
    selected_tests = set(st.multiselect("Practice Tests:", practice_tests))
    selected_difficulty = set(st.multiselect("Difficulty", difficulty))
    selected_category = set(st.multiselect("Category", category))
    
    selected_correctness = set(st.multiselect("Correct or Incorrect", correctness.values()))
    
    selected_section = set(st.multiselect("Section/Module", section))
    
    if st.button("Generate PDF"):
        hyperlinks = []
        #GET Calls to Google Sheets API
        download_result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=range_name, includeGridData=True).execute()
        filtered_dataset = sheets_service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=range_list).execute()

        #store the values into individual array
        category_values = filtered_dataset['valueRanges'][0]['values']
        difficulty_values = filtered_dataset['valueRanges'][1]['values']
        section_values = filtered_dataset['valueRanges'][2]['values']
        correctness_values = filtered_dataset['valueRanges'][3]['values']
        test_values = filtered_dataset['valueRanges'][4]['values']

        # Flags to check if filters are active
        is_category_filter = len(selected_category) > 0
        is_difficulty_filter = len(selected_difficulty) > 0
        is_section_filter = len(selected_section) > 0
        is_correctness_filter = len(selected_correctness) > 0
        is_test_filter = len(selected_tests) > 0
        
        
        idx = 0 # Index of the current cell
        for number_of_rows, row in enumerate(download_result['sheets'][0]['data'][0]['rowData']):
            for num_of_row_values, cell in enumerate((row['values'])):
                # Check if cell meets all active filters
                #the logic is if the filter is not active then reurns true for that particular filter
                if (not is_category_filter or category_values[idx][0] in selected_category) and \
                (not is_difficulty_filter or difficulty_values[idx][0] in selected_difficulty) and \
                (not is_section_filter or section_values[idx][0] in selected_section) and \
                (not is_correctness_filter or correctness_values[idx][0] in selected_correctness) and \
                (not is_test_filter or test_values[idx][0] in selected_tests):
                    if 'hyperlink' in cell:
                        hyperlinks.append(cell['hyperlink'])     
                
                idx += 1
                
                
        save_dir = 'downloaded_pngs'
        os.makedirs(save_dir, exist_ok=True)
        
        # Download images
        for idx, url in enumerate(hyperlinks):
            try:
                if 'drive.google.com' in url:
                    file_id = url.split('/')[-2]
                    file_path = os.path.join(save_dir, f'image_{idx + 1}.png')
                    download_drive_file(drive_service, file_id, file_path)
                else:
                    print(f"Failed to download or invalid content type for URL: {url}")
            except Exception as e:
                print(f"Request failed for URL {url}: {e}")
                
        
        images = []
        
        #Convert images to pdf
        file_names = os.listdir(save_dir)
        file_names.remove('merged.pdf') 
        file_names.sort(key = lambda x: int(x.split('_')[1].split('.')[0]))
        print(f"file_names: {file_names}")
        for filename in (file_names):
            if filename.endswith(".png"):
                filepath = os.path.join(save_dir, filename)
                image = (Image.open(filepath))
                images.append(image.convert('RGB'))
                
        

        pdf_path = os.path.join(save_dir,'merged.pdf')
        if len(images) > 0:
            images[0].save(pdf_path, save_all=True, append_images=images[1:])
        else:
            st.error("No images to merge")

        # Delete images from folder
        for filename in os.listdir(save_dir):
            if filename.endswith(".png"):
                os.remove(os.path.join(save_dir, filename))
        pdf_path = 'downloaded_pngs/merged.pdf'
        
        #open pdf for user to download
        if os.path.exists(pdf_path):
            with open(pdf_path, 'rb') as f:
                btn = st.download_button(
                    label = "Merged PDF",
                    data = f,
                    file_name = 'merged.pdf',
                    mime = 'application/octet-stream'
                )

                
    if st.button("Generate Solutions"):
        hyperlinks = []
        #GET Calls to Google Sheets API
        solutions_range = sheet_name + "!" + "F" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "F" + (range_name.split("!")[1].split(":")[1].split()[0][1:])

                    
       
    # #USER AUTHENTICATION
    # def user_logged_in():
    #     return st.session_state['user_token'] is not None
        

    # if 'user_token' not in st.session_state:
    #     st.session_state['user_token'] = None          
    # choices = st.selectbox("Select an option", ["Login", "Signup"])
    # #login
    # email = st.text_input("Email")
    # password = st.text_input("Password", type="password")

    # if choices == "Signup":
    #     submit = st.button("Create my account")
    #     if submit:
    #         try:
    #             user = auth.create_user_with_email_and_password(email, password)
    #             st.success("Account created successfully")
    #         except firebase_admin.auth.EmailAlreadyExistsError:
    #             st.error("Email already exists")
    # else:
    #     if st.button("Login"):
    #         try:
    #             user = auth.sign_in_with_email_and_password(email, password)
    #             st.session_state['user_token'] = user['idToken']
    #             st.success("Logged in successfully")
    #         except:
    #             st.error("Invalid email/password")

    # if user_logged_in():
    #     main()
    # else:
    #     st.info("Please login/signup to continue")
