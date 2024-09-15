import streamlit as st
import tempfile
import os
import zipfile

from io import BytesIO
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from utils import *
from genericpath import isfile

def splitter():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 
              'https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file']
    DELEGATED_EMAIL = 'renan@peaceofpilearning.com'
    creds = Credentials.from_service_account_file('service_credentials.json', scopes=SCOPES)
    delegated_credentials = creds.with_subject(DELEGATED_EMAIL)
    drive_service = build('drive', 'v3', credentials=delegated_credentials)
    sheets_service = build('sheets', 'v4', credentials=creds)
    first_page = False
    st.header("PDF Splitter")
    
    if st.selectbox("Would you like Splitter to skip pages?", ("Yes", "No"),index = 1) == "Yes":
        pages_to_skip = add_skip_page_form()
    else:
        pages_to_skip = []

    question_bank_sheet_range = st.text_input("Range of Cells" ,value = "Sheet1!G1329:G1376")
    if st.selectbox("Does the pdf have a page with less than 4 questions?", ("Yes", "No"),index = 1) == "Yes":
        single_question_pages = add_page_direction_form()
    else: 
        single_question_pages = []

    print(f"Pages to skip: {pages_to_skip}")

    page_number_dict = {}
    for page_number, direction in single_question_pages:
        if page_number in page_number_dict:
            page_number_dict[page_number].append(direction)
        else:
            page_number_dict[page_number] = [direction]

    print("PAGE NUMBER DICT: ", page_number_dict)

    pdf_file = st.file_uploader("Upload a POP PDF file", type="pdf")

    image_folder_path = "./temp_images/"
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)  
    #clear previous image files from temp_images folder
    for filename in os.listdir(image_folder_path):        
        if filename.endswith("png"):
            os.remove(os.path.join(image_folder_path , filename))
    if pdf_file is not None:
        # Create a temporary directory to save the PDF file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Construct the file path
            pdf_path = os.path.join(temp_dir, pdf_file.name)
            
            # Write the uploaded PDF file to the temporary file
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.getvalue())

            # extract_images_from_pdf(pdf_path,image_folder_path)
            extract_images_from_pdf_2(pdf_path,image_folder_path,page_number_dict,pages_to_skip)
            
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'a', zipfile.ZIP_DEFLATED) as zip_file:
            for image_file_name in os.listdir(image_folder_path):
                image_path = os.path.join(image_folder_path, image_file_name)
                zip_file.write(image_path, image_file_name)
        zip_buffer.seek(0)

        st.download_button(
            label="Download Images as Zip",
            data=zip_buffer,
            file_name="images.zip",
            mime="application/zip"
        )

        save_dir = ("./temp_images/")
        folder_name = st.text_input("Name of Folder: ")
        question_bank_sheet_id = "1NR1R1TFrkmbO7FSilfjV9VbEd28aPYY_lJf9NIApZjo"
        urls = []

        if st.button("Send to Drive") and folder_name:
            folder_id = create_drive_folder(drive_service, folder_name, parent_id='11Q2QJQKN45aGdSe_pUsjyheI6T18y7IS')  # Replace 'My Folder Name' and parent_id as needed
            #sort save_dir by page_number

            file_names = [f for f in os.listdir(save_dir) if os.path.isfile(os.path.join(save_dir, f))]
            sorted_file_names = sort_files_by_page_number(file_names, first_page)
            print("SORTED FILE NAMES: ", sorted_file_names)

            for filename in sorted_file_names:
                file_path = os.path.join(save_dir, filename)
                if os.path.isfile(file_path):
                    mime_type = "application/octet-stream"
                    url = upload_file_to_folder(drive_service, file_path, mime_type, folder_id)
                    urls.append(url)
            #sort urls by page number
            cellContent = get_cell_content(sheets_service,question_bank_sheet_id,question_bank_sheet_range)
            print("Cell Content: ", cellContent)
            update_sheet_cell(sheets_service,question_bank_sheet_id,question_bank_sheet_range,urls,cellContent)  
                    
            print("URLS: ", urls)   

        for filename in os.listdir(save_dir):        
            if filename.endswith("png"):
                os.remove(os.path.join(save_dir, filename))
                    

