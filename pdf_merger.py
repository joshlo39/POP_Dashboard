from re import sub
import streamlit as st
import os
from utils import *
from Filters import Filters
from Names import Names
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaFileUpload
import pyrebase
import firebase_admin
from firebase_admin import credentials
from PIL import Image
import io
import json
from reportlab.lib.pagesizes import letter

def pdf_merger(
    sheets_service,
    drive_service,
    practice_tests,
    difficulty,
    category,
    sub_category_one,
    sub_category_two,
    sub_category_three,
    calculator
):
    #------------Firebase Auth--------------#
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

    #------------Streamlit Config--------#
    student_names = Names()
    st.title("Peace of Pi: PDF Merger")
    
    default_sheet = "Sheet1!C2:C2458"
    range_name = st.text_input("Enter the name of the sheet and the range of cells you want to download:", value=default_sheet)
    default_URL = "https://docs.google.com/spreadsheets/d/1oos0L31aEqjPWYuF4ey23AbAs_8X8HJjPSJgFDmTuRs/edit?gid=0#gid=0"
    spreadsheet_url = st.text_input("Enter the URL of the spreadsheet:", value=default_URL)
    
    range_name = range_name.upper()
    spreadsheet_id = spreadsheet_url.split('/')[-2]
    
    names = student_names.names
    student_name = st.selectbox("Select a student name:", names)
    if student_name and st.button("Update Cell"):
        if update_sheet_cell(sheets_service, spreadsheet_id, "Dashboard!A1", student_name):
            st.success("Cell updated successfully!")
    
    number_of_pages = st.number_input("Number of questions per page (1, 2, or 4):", min_value=1,value=4)

    #-----------------Dropdown Selections--------------------#
    st.subheader("Filter")
    selected_tests = set(st.multiselect("Practice Tests:", practice_tests))
    selected_difficulty = set(st.multiselect("Difficulty", difficulty))
    selected_category = set(st.multiselect("Category", category))
    selected_category_one = set(st.multiselect("Sub-Category 1", sub_category_one))
    selected_category_two = set(st.multiselect("Sub-Category 2", sub_category_two))
    selected_category_three = set(st.multiselect("Sub-Category 3", sub_category_three))
    selected_correctness = set(st.multiselect("Correct or Incorrect", Filters().correctness.values()))
    selected_section = set(st.multiselect("Section/Module", Filters().section))
    selected_calculator = set(st.multiselect("Calculator", calculator))

    #-----------------Ranges--------------------#
    sheet_name = range_name.split("!")[0]
    col_indices = lambda col: f"{col}{range_name.split('!')[1].split(':')[0][1:]}:{col}{range_name.split('!')[1].split(':')[1][1:]}"
    
    category_range = sheet_name + "!" + col_indices("J")
    difficulty_range = sheet_name + "!" + col_indices("H")
    section_range = sheet_name + "!" + col_indices("B")
    correctness_range = sheet_name + "!" + col_indices("D")
    test_range = sheet_name + "!" + col_indices("A")
    solutions_range = sheet_name + "!" + col_indices("F")
    sub_category_one_range = sheet_name + "!" + col_indices("K")
    sub_category_two_range = sheet_name + "!" + col_indices("L")
    sub_category_three_range = sheet_name + "!" + col_indices("M")
    solutions_images_range = sheet_name + "!" + col_indices("E")
    calculator_range = sheet_name + "!" + col_indices("P")

    range_list = [
        category_range, difficulty_range, section_range, correctness_range,
        test_range, solutions_range, solutions_images_range,
        sub_category_one_range, sub_category_two_range, sub_category_three_range,
        calculator_range
    ]

    #-----------------Fetch Data--------------------#
    download_result = sheets_service.spreadsheets().get(
        spreadsheetId=spreadsheet_id, ranges=range_name, includeGridData=True
    ).execute()
    filtered_dataset = sheets_service.spreadsheets().values().batchGet(
        spreadsheetId=spreadsheet_id, ranges=range_list
    ).execute()

    def safe_get(values, idx):
        if not values or idx < 0 or idx >= len(values):
            return ""
        row = values[idx]
        if not isinstance(row, list):
            return str(row) if row is not None else ""
        return str(row[0]) if len(row) > 0 else ""

    #-----------------Extract Values--------------------#
    category_values = filtered_dataset['valueRanges'][0].get('values', [])
    difficulty_values = filtered_dataset['valueRanges'][1].get('values', [])
    section_values = filtered_dataset['valueRanges'][2].get('values', [])
    correctness_values = filtered_dataset['valueRanges'][3].get('values', [])
    test_values = filtered_dataset['valueRanges'][4].get('values', [])
    sub_category_one_values = filtered_dataset['valueRanges'][7].get('values', [])
    sub_category_two_values = filtered_dataset['valueRanges'][8].get('values', [])
    sub_category_three_values = filtered_dataset['valueRanges'][9].get('values', [])
    calculator_values = filtered_dataset['valueRanges'][10].get('values', [])

    #-----------------Flags--------------------#
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

    #-----------------Generate PDF--------------------#
    if st.button("Generate PDF"):
        hyperlinks = []
        os.makedirs(save_dir, exist_ok=True)
        for filename in os.listdir(save_dir):
            if filename.endswith(".png"):
                os.remove(os.path.join(save_dir, filename))

        idx = 0
        for row in download_result['sheets'][0]['data'][0]['rowData']:
            for cell in row['values']:
                cat_val = safe_get(category_values, idx)
                diff_val = safe_get(difficulty_values, idx)
                sect_val = safe_get(section_values, idx)
                corr_val = safe_get(correctness_values, idx)
                test_val = safe_get(test_values, idx)
                sub1_val = safe_get(sub_category_one_values, idx)
                sub2_val = safe_get(sub_category_two_values, idx)
                sub3_val = safe_get(sub_category_three_values, idx)
                calc_val = safe_get(calculator_values, idx)

                if (not is_category_filter or cat_val in selected_category) and \
                   (not is_difficulty_filter or diff_val in selected_difficulty) and \
                   (not is_section_filter or sect_val in selected_section) and \
                   (not is_correctness_filter or corr_val in selected_correctness) and \
                   (not is_test_filter or test_val in selected_tests) and \
                   (not is_subcategory1_filter or sub1_val in selected_category_one) and \
                   (not is_subcategory2_filter or sub2_val in selected_category_two) and \
                   (not is_subcategory3_filter or sub3_val in selected_category_three) and \
                   (not is_calculator_filter or calc_val in selected_calculator):
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
                # safe inline checks
                cat_val = safe_get(category_values, idx)
                diff_val = safe_get(difficulty_values, idx)
                sect_val = safe_get(section_values, idx)
                corr_val = safe_get(correctness_values, idx)
                test_val = safe_get(test_values, idx)
                sub1_val = safe_get(sub_category_one_values, idx)
                sub2_val = safe_get(sub_category_two_values, idx)
                sub3_val = safe_get(sub_category_three_values, idx)
                calc_val = safe_get(calculator_values, idx)

                if (not is_category_filter or cat_val in selected_category) and \
                   (not is_difficulty_filter or diff_val in selected_difficulty) and \
                   (not is_section_filter or sect_val in selected_section) and \
                   (not is_correctness_filter or corr_val in selected_correctness) and \
                   (not is_test_filter or test_val in selected_tests) and \
                   (not is_subcategory1_filter or sub1_val in selected_category_one) and \
                   (not is_subcategory2_filter or sub2_val in selected_category_two) and \
                   (not is_subcategory3_filter or sub3_val in selected_category_three) and \
                   (not is_calculator_filter or calc_val in selected_calculator):
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
            # use safe_get with index i for the filtering here too
            cat_val = safe_get(category_values, i)
            diff_val = safe_get(difficulty_values, i)
            sect_val = safe_get(section_values, i)
            corr_val = safe_get(correctness_values, i)
            test_val = safe_get(test_values, i)
            sub1_val = safe_get(sub_category_one_values, i)
            sub2_val = safe_get(sub_category_two_values, i)
            sub3_val = safe_get(sub_category_three_values, i)

            if (not is_category_filter or cat_val in selected_category) and \
                (not is_difficulty_filter or diff_val in selected_difficulty) and \
                (not is_section_filter or sect_val in selected_section) and \
                (not is_correctness_filter or corr_val in selected_correctness) and \
                (not is_test_filter or test_val in selected_tests) and \
                (not is_subcategory1_filter or sub1_val in selected_category_one) and \
                (not is_subcategory2_filter or sub2_val in selected_category_two) and \
                (not is_subcategory3_filter or sub3_val in selected_category_three):
                for idx2, value in enumerate(item.get('values', [])):
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
