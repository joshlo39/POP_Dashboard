import streamlit as st
from utils import extract_images_from_pdf
import tempfile
import os
import zipfile
from io import BytesIO

def splitter():
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
        for filename in os.listdir(save_dir):
            if filename.endswith("png"):
                os.remove(os.path.join(save_dir, filename))

        

