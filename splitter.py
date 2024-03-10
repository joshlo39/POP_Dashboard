import streamlit as st
from utils import extract_images_from_pdf
import tempfile
import os
import zipfile
from io import BytesIO
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from utils import create_drive_folder, upload_file_to_folder
def splitter():
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive',]
    creds = Credentials.from_service_account_file('service_credentials.json', scopes=SCOPES)
    drive_service = build('drive', 'v3', credentials=creds)
  
    st.header("PDF Splitter")
    pdf_file = st.file_uploader("Upload a POP PDF file", type="pdf")
    
    image_folder_path = "./temp_images/"
    if not os.path.exists(image_folder_path):
        os.makedirs(image_folder_path)  
    if pdf_file is not None:
        # Create a temporary directory to save the PDF file
        with tempfile.TemporaryDirectory() as temp_dir:
            # Construct the file path
            pdf_path = os.path.join(temp_dir, pdf_file.name)
            
            # Write the uploaded PDF file to the temporary file
            with open(pdf_path, "wb") as f:
                f.write(pdf_file.getvalue())

            # Now you can use the saved file path with your function
            extract_images_from_pdf(pdf_path,image_folder_path)
            
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
        if st.button("Send to Drive") and folder_name:
            print("Sending to Drive...")
            folder_id = create_drive_folder(drive_service, folder_name, parent_id='11Q2QJQKN45aGdSe_pUsjyheI6T18y7IS')  # Replace 'My Folder Name' and parent_id as needed
            local_folder_path = save_dir  # Replace with the path to your local folder
            for filename in os.listdir(local_folder_path):
                file_path = os.path.join(local_folder_path, filename)
                if os.path.isfile(file_path):
                    mime_type = 'application/octet-stream'  # You may want to set specific MIME types based on the file
                    upload_file_to_folder(drive_service, file_path, mime_type, folder_id)

        for filename in os.listdir(save_dir):
            if filename.endswith("png"):
                os.remove(os.path.join(save_dir, filename))
                
            

