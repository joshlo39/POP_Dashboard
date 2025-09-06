from re import sub
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
from reportlab.lib.pagesizes import letter 
from utils import * 
from Filters import Filters 
from Names import Names
from googleapiclient.http import MediaFileUpload
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
    filterData = Filters()
    student_names = Names()
    st.title("Peace of Pi: PDF Merger")
    default_sheet = "Sheet1!C2:C2458"
    range_name = st.text_input("Enter the name of the sheet and the range of cells you want to download:"
                            ,value = default_sheet)
    default_URL = "https://docs.google.com/spreadsheets/d/1oos0L31aEqjPWYuF4ey23AbAs_8X8HJjPSJgFDmTuRs/edit?gid=0#gid=0"
    range_name = range_name.upper()
    spreadsheet_url = st.text_input("Enter the URL of the spreadsheet:"
                                    ,value = default_URL)
    spreadsheet_id = spreadsheet_url.split('/')[-2]
    names = student_names.names 
    student_name = st.selectbox("Select a student name:", names)
    if student_name:
        if st.button("Update Cell"):
            if update_sheet_cell(sheets_service, spreadsheet_id, "Dashboard!A1", student_name):
                st.success("Cell updated successfully!")
                
     
                    
    #-----------------Settup--------------------#
    # This is where the sheet columns have to match the input box label 
    practice_tests = filterData.practice_tests

    sheet_name = range_name.split("!")[0]
    category_range = sheet_name + "!" + "K" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "K" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    difficulty_range = sheet_name + "!" + "H" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "H" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    section_range = sheet_name + "!" + "B" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "B" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    correctness_range = sheet_name + "!" + "D" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "D" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    test_range = sheet_name + "!" + "A" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "A" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    solutions_range = sheet_name + "!" + "F" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "F" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    sub_category_one_range= sheet_name + "!" + "L" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "L" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    sub_category_two_range= sheet_name + "!" + "M" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "M" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    sub_category_three_range= sheet_name + "!" + "N" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "N" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    solutions_images_range = sheet_name + "!" + "E" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "E" + (range_name.split("!")[1].split(":")[1].split()[0][1:])
    calulator_range = sheet_name + "!" + "P" + (range_name.split("!")[1].split(":")[0].split()[0][1:]) + ":" + "P" + (range_name.split("!")[1].split(":")[1].split()[0][1:])

 
    #Array of ranges 
    range_list = [category_range, difficulty_range, section_range, correctness_range,test_range,solutions_range,solutions_images_range,sub_category_one_range,sub_category_two_range,sub_category_three_range,calulator_range]

    #variable to store the hardcoded values for each dropdown
    category = filterData.category    
    sub_category_one = filterData.sub_category_one
    sub_category_two = filterData.sub_category_two
    sub_category_three = filterData.sub_category_three
    difficulty = filterData.difficulty
    correctness = filterData.correctness
    section = filterData.section
    calculator = filterData.calculator

    if 'practice_tests' not in st.session_state:
        st.session_state['practice_tests'] = practice_tests.copy()
    number_of_pages = st.number_input("Number of pages per PDF", min_value=1, value=4)

    new_test = st.text_input("Add a new practice test:")
    if st.button("Add Test"):
        if new_test:
            st.session_state['practice_tests'].append(new_test)
            save_practice_tests(st.session_state['practice_tests'], 'practice_tests.json')
            st.success(f"Added {new_test} to the list of practice tests!")
        else:
            st.error("Practice Test not saved")

    st.subheader("Filter")
    selected_tests = set(st.multiselect("Practice Tests:", practice_tests))
    selected_difficulty = set(st.multiselect("Difficulty", difficulty))
    selected_category = set(st.multiselect("Category", category))
    selected_category_one = set(st.multiselect("Sub-Category 1",sub_category_one))
    selected_category_two = set(st.multiselect("Sub-Category 2",sub_category_two))
    selected_category_three = set(st.multiselect("Sub-Category 3",sub_category_three))
    selected_correctness = set(st.multiselect("Correct or Incorrect", correctness.values()))
    selected_section = set(st.multiselect("Section/Module", section))
    selected_calculator = set(st.multiselect("Calculator", calculator))

    #Hit sheet api and pass in the range of cells to grab the data from 
    download_result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=range_name, includeGridData=True).execute()
    filtered_dataset = sheets_service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=range_list).execute()

    #store the values into individual array
    category_values = filtered_dataset['valueRanges'][0].get('values') or ["NA"]
    difficulty_values = filtered_dataset['valueRanges'][1].get('values') or ["NA"]
    section_values = filtered_dataset['valueRanges'][2].get('values') or ["NA"]
    correctness_values = filtered_dataset['valueRanges'][3].get('values') or ["NA"]
    test_values = filtered_dataset['valueRanges'][4].get('values') or ["NA"]
    sub_category_one_values = filtered_dataset['valueRanges'][7].get('values') or ["NA"]
    sub_category_two_values = filtered_dataset['valueRanges'][8].get('values') or ["NA"]
    sub_category_three_values = filtered_dataset['valueRanges'][9].get('values') or ["NA"]
    calculator_values = filtered_dataset['valueRanges'][10].get('values') or ["NA"]

    # Flags to check if filters are active
    is_category_filter = len(selected_category) > 0
    is_difficulty_filter = len(selected_difficulty) > 0
    is_section_filter = len(selected_section) > 0
    is_correctness_filter = len(selected_correctness) > 0
    is_test_filter = len(selected_tests) > 0
    is_subcategory1_filter = len(selected_category_one) > 0
    is_subcategory2_filter = len(selected_category_two) > 0
    is_subcategory3_filter = len(selected_category_three) > 0
    is_calculator_filter = len(selected_calculator) > 0

    save_dir = 'downloaded_pngs'

    #-----------------Normal Packet--------------------#
    if st.button("Generate PDF"):
        hyperlinks = []

        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        for filename in os.listdir(save_dir):
            if filename.endswith(".png"):
                os.remove(os.path.join(save_dir, filename))
        pdf_path = 'downloaded_pngs/merged.pdf'
        

        #i dont think this does anything important 
        video_hyperlinks = []
        for number_of_rows, row in enumerate(download_result['sheets'][0]['data'][0]['rowData']):
            for num_of_row_values, cell in enumerate((row['values'])):
                # Check if cell meets all active filters
                #the logic is if the filter is not active then reurns true for that particular filter
                    if 'hyperlink' in cell:
                        video_hyperlinks.append(cell['hyperlink'])     
        print(selected_difficulty)
        idx = 0 # Index of the current cell
        for number_of_rows, row in enumerate(download_result['sheets'][0]['data'][0]['rowData']):
            for num_of_row_values, cell in enumerate((row['values'])):
                # Check if cell meets all active filters
                #the logic is if the filter is not active then reurns true for that particular filter
                if (not is_category_filter or category_values[idx][0] in selected_category) and \
                (not is_difficulty_filter or difficulty_values[idx][0] in selected_difficulty) and \
                (not is_section_filter or section_values[idx][0] in selected_section) and \
                (not is_correctness_filter or correctness_values[idx][0] in selected_correctness) and \
                    (not is_test_filter or test_values[idx][0] in selected_tests) and \
                    (not is_subcategory1_filter or sub_category_one_values[idx][0] in selected_category_one) and \
                    (not is_subcategory2_filter or sub_category_two_values[idx][0] in selected_category_two) and \
                    (not is_subcategory3_filter or sub_category_three_values[idx][0] in selected_category_three) and \
                    (not is_calculator_filter or calculator_values[idx][0] in selected_calculator):
                    if 'hyperlink' in cell:
                        hyperlinks.append(cell['hyperlink'])     
                
                idx += 1
                
        os.makedirs(save_dir, exist_ok=True)
        for idx, url in enumerate(hyperlinks):
            try:
                if 'drive.google.com' in url:
                    file_id = extract_drive_file_id(url)
                    if not file_id:
                        print(f"Failed to extract file ID from URL: {url}")
                        continue  # Skip this URL

                    file_path = os.path.join(save_dir, f'image_{idx + 1}.png')
                    download_drive_file(drive_service, file_id, file_path)
                else:
                    print(f"Failed to download or invalid content type for URL: {url}")
            except Exception as e:
                print(f"Request failed for URL {url}: {e}")


        
        # # Download images
        # for idx, url in enumerate(hyperlinks):
        #     try:
        #         if 'drive.google.com' in url:
        #             file_id = url.split('/')[-2]
        #             file_path = os.path.join(save_dir, f'image_{idx + 1}.png')
        #             download_drive_file(drive_service, file_id, file_path)
        #         else:
        #             print(f"Failed to download or invalid content type for URL: {url}")
        #     except Exception as e:
        #         print(f"Request failed for URL {url}: {e}")
                
        
        images = []
        
        
        #hyperlinks for video 
        solutions_result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=solutions_range, includeGridData=True).execute()
        solution_data = solutions_result['sheets'][0]['data'][0]['rowData']


        #video hyperlinks comes in order
        #images don't come in order 
        #------Images------#
        image_paths = []
        inner_array = []
        file_names = [f for f in os.listdir(save_dir) if f != 'random.txt'] 

        if 'merged.pdf' in file_names:
            file_names.remove('merged.pdf')

        file_names.sort(key = lambda x: int(x.split('_')[1].split('.')[0]))
        get_rick_rolled = "https://www.youtube.com/watch?v=B_OhHIja95g"

        for idx, filename in enumerate(file_names):
            if filename.endswith(".png"):
                filepath = os.path.join(save_dir, filename)

                inner_array.append((filepath, (f" ", get_rick_rolled)))
                
                if len(inner_array) == 4:
                    image_paths.append(sorted(inner_array))
                    inner_array = []
        #if there is a non-full page of images, then append it to the end of the outer array
        if inner_array:
            image_paths.append(inner_array)

        if number_of_pages == 4:
            create_pdf_with_2x2_images_hyperlinks_small_hyperlink('downloaded_pngs/merged.pdf', image_paths )
        elif number_of_pages == 2:
            create_pdf_two_questions_per_page('downloaded_pngs/merged.pdf', image_paths )
        elif number_of_pages == 1:
            create_pdf_one_question_per_page('downloaded_pngs/merged.pdf', image_paths )
        else:
            st.error("Invalid number of pages per PDF")


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
        for filename in os.listdir(save_dir):
            if filename.endswith(".pdf"):
                os.remove(os.path.join(save_dir, filename))
#-----------------End of Normal Packet--------------------#





#-----------------Solutions Packet--------------------#      
    if st.button("Generate Solutions"):
        
        download_result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=solutions_images_range, includeGridData=True).execute()
        filtered_dataset = sheets_service.spreadsheets().values().batchGet(spreadsheetId=spreadsheet_id, ranges=range_list).execute()
        solutions_result = sheets_service.spreadsheets().get(spreadsheetId=spreadsheet_id, ranges=solutions_range, includeGridData=True).execute()
        solution_data = solutions_result['sheets'][0]['data'][0]['rowData']

        #-------Getting hyperlink for the images and downloading the images-------#
        hyperlinks = []
        idx = 0 # Index of the current cell
        for number_of_rows, row in enumerate(download_result['sheets'][0]['data'][0]['rowData']):
            for num_of_row_values, cell in enumerate((row['values'])):
                # Check if cell meets all active filters
                #the logic is if the filter is not active then reurns true for that particular filter
                if (not is_category_filter or category_values[idx][0] in selected_category) and \
                (not is_difficulty_filter or difficulty_values[idx][0] in selected_difficulty) and \
                (not is_section_filter or section_values[idx][0] in selected_section) and \
                (not is_correctness_filter or correctness_values[idx][0] in selected_correctness) and \
                (not is_test_filter or test_values[idx][0] in selected_tests) and \
                (not is_subcategory1_filter or sub_category_one_values[idx][0] in selected_category_one) and \
                (not is_subcategory2_filter or sub_category_two_values[idx][0] in selected_category_two) and \
                (not is_subcategory3_filter or sub_category_three_values[idx][0] in selected_category_three) and \
                (not is_calculator_filter or calculator_values[idx][0] in selected_calculator):
                    if 'hyperlink' in cell:
                        hyperlinks.append(cell['hyperlink'])     
                
                idx += 1
                
        os.makedirs(save_dir, exist_ok=True)
        # Delete images from folder
        for filename in os.listdir(save_dir):
            if filename.endswith(".png"):
                os.remove(os.path.join(save_dir, filename))
        pdf_path = 'downloaded_pngs/merged.pdf'
        
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

        #-------END: Getting hyperlink for the images and downloading the images-------#

        #-----------------Getting all video link--------------------#
        video_hyperlinks = [] 
        for i, item in enumerate(solution_data):
            if (not is_category_filter or category_values[i][0] in selected_category) and \
                (not is_difficulty_filter or difficulty_values[i][0] in selected_difficulty) and \
                (not is_section_filter or section_values[i][0] in selected_section) and \
                (not is_correctness_filter or correctness_values[i][0] in selected_correctness) and \
                (not is_test_filter or test_values[i][0] in selected_tests) and \
                (not is_subcategory1_filter or sub_category_one_values[i][0] in selected_category_one) and \
                (not is_subcategory2_filter or sub_category_two_values[i][0] in selected_category_two) and \
                (not is_subcategory3_filter or sub_category_three_values[i][0] in selected_category_three):
                for idx, value in enumerate(item['values']):
                    if 'userEnteredFormat' in value and 'textFormat' in value['userEnteredFormat'] and 'link' in value['userEnteredFormat']['textFormat']:
                        uri = value['userEnteredFormat']['textFormat']['link']['uri']
                        video_hyperlinks.append(uri)
                    else:
                        #if there is no hyperlink, then add a default hyperlink
                        video_hyperlinks.append('https://www.youtube.com/watch?v=B_OhHIja95g')
        #------Images------#
        image_paths = []
        inner_array = []
        
        file_names = [f for f in os.listdir(save_dir) if f != 'random.txt'] 
        file_names.sort(key = lambda x: int(x.split('_')[1].split('.')[0]))
        for idx, filename in enumerate(file_names):
            if filename.endswith(".png"):
                filepath = os.path.join(save_dir, filename)
                inner_array.append((filepath, (f" ", video_hyperlinks[idx] if len(video_hyperlinks) > 0 else 'https://www.youtube.com/watch?v=B_OhHIja95g')))
                
                if len(inner_array) == 4:
                    image_paths.append(sorted(inner_array))
                    inner_array = []
        #if there is a non-full page of images, then append it to the end of the outer array
        if inner_array:
            image_paths.append(inner_array)
        if len(video_hyperlinks) > 0:
            create_pdf_with_2x2_images_hyperlinks('downloaded_pngs/merged.pdf', image_paths )
        else:
            create_pdf_with_2x2_images_hyperlinks_small_hyperlink('downloaded_pngs/merged.pdf', image_paths )
    

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
        for filename in os.listdir(save_dir):
            if filename.endswith(".pdf"):
                os.remove(os.path.join(save_dir, filename))

         

    
    
    
    
    
    
    
    
    
    
    
    
    
     
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
