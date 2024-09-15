from statistics import variance
import gspread
import requests
import os
import streamlit_authenticator as stauth
import firebase_admin
import streamlit as st
from firebase_admin import credentials
from firebase_admin import auth
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials
from googleapiclient.http import MediaIoBaseDownload
import io
from PIL import Image
from googleapiclient.http import MediaFileUpload
import pyrebase
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.colors import red  
import fitz #PyMuPdf
import re

def add_skip_page_form():
    if 'skip_pages' not in st.session_state:
        st.session_state.skip_pages = {}
    container = st.container()
    with container:
        col1,_,_= st.columns(3)
        page_number = col1.number_input("Page Number", min_value=1, value=1, key=f"skip_page_{len(st.session_state.skip_pages)}")
        if st.button("Add Page"):
            st.session_state.skip_pages[page_number] = True
        if st.button("Submit", key='submit_pages'):
            st.write("Submitted skip pages:")
            st.write(st.session_state.skip_pages)
    return st.session_state.skip_pages

def add_page_direction_form():
    # Initialize session state for pair count if it doesn't exist
    if 'all_pairs' not in st.session_state:
        st.session_state.all_pairs = []

    container = st.container()

    with container:
        col1, col2, _ = st.columns(3)
        page_number = col1.number_input("Page Number", min_value=1, value=1, key=f"page_{len(st.session_state.all_pairs)}")
        direction = col2.selectbox("Direction", ["Left", "Right"], key=f"dir_{len(st.session_state.all_pairs)}")
        if st.button("Add Pair"):
            st.session_state.all_pairs.append((page_number, direction))

    # Submit button to display the submitted pairs
    if st.button("Submit", key='submit'):
        st.write("Submitted page number-direction pairs:")
        for pair in st.session_state.all_pairs:
            st.write(pair)
    return st.session_state.all_pairs

def update_sheet_cell(service, spreadsheet_id, range_name, value):
    body = {
        'values': [[value]]
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id, range=range_name,
        valueInputOption='USER_ENTERED', body=body).execute()
    return result

def download_drive_file(service, file_id, save_path):
        request = service.files().get_media(fileId=file_id)
        file = io.BytesIO()
        with open(save_path, 'wb') as fh:
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while done is False:
                status, done = downloader.next_chunk()

def smart_sort(arr):
    arr.sort(key=lambda x: int(x.split('-')[0]))
    return arr

def create_hyperlink_pdf(output_pdf_path, hyperlinks, link_text_positions):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)

    for link, position in zip(hyperlinks, link_text_positions):
        x, y = position
        c.setFillColorRGB(0, 0, 1)  # Blue color for hyperlink text
        c.drawString(x, y, "Video Link")  # Example text
        c.linkURL(url=link, rect=(x, y, x + 100, y + 10), relative=1)

    c.save()
    


def create_pdf_with_2x2_images_hyperlinks(output_pdf_path, image_details, max_image_width=306, max_image_height=396):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    page_width, page_height = letter
    print(f"page_width: {page_width}, page_height: {page_height}")

    for page_idx, page_content in enumerate(image_details):
        for image_idx, (image_path, hyperlink) in enumerate(page_content):
            # Calculate image position
            x = (page_width / 2) * (image_idx % 2)
            y = (page_height / 2) * (1 - (image_idx // 2))

            # Open and resize the image
            try:
                img = Image.open(image_path)
            except:
                print(f"Error opening image {image_path}")
                os.remove(image_path)
            img_width, img_height = img.size
            
            scale = min(max_image_width / img_width,max_image_height / img_height)
            img_width *= scale
            img_height *= scale

            # Adjust position to center the image in its quadrant
            x += (max_image_width - img_width) / 2
            y += (max_image_height - img_height) / 2

            # Add the image
            c.drawImage(image_path, x, y, width=img_width, height=img_height)

            # Add the hyperlink
            link_text, link_url = hyperlink
            text = c.beginText(x, y)  # Adjust the y-coordinate for hyperlink position
            text.setFont("Helvetica", 14)
            text.setFillColor(red)
            text.textLine(link_text)
            c.drawText(text)
            c.linkURL(link_url, (x, y, x + img_width, y+img_height), relative=0)

        # Create a new page if not the last page
        if page_idx < len(image_details) - 1:
            c.showPage()

    c.save()
 
def create_pdf_with_2x2_images_hyperlinks_small_hyperlink(output_pdf_path, image_details, max_image_width=306, max_image_height=396):
    c = canvas.Canvas(output_pdf_path, pagesize=letter)
    page_width, page_height = letter
    print(f"page_width: {page_width}, page_height: {page_height}")
    save_dir = "downloaded_pngs/"
    for page_idx, page_content in enumerate(image_details):
        for image_idx, (image_path, hyperlink) in enumerate(page_content):
            # Calculate image position
            x = (page_width / 2) * (image_idx % 2)
            y = (page_height / 2) * (1 - (image_idx // 2))

            # Open and resize the image
            try:
                img = Image.open(image_path)
            except:
                print(f"Error opening image {image_path}")
                os.remove(image_path)

            img_width, img_height = img.size
            
            scale = min(max_image_width / img_width,max_image_height / img_height)
            img_width *= scale
            img_height *= scale

            # Adjust position to center the image in its quadrant
            x += (max_image_width - img_width) / 2
            y += (max_image_height - img_height) / 2

            # Add the image
            c.drawImage(image_path, x, y, width=img_width, height=img_height)

            # Add the hyperlink
            link_text, link_url = hyperlink
            text = c.beginText(x, y)  # Adjust the y-coordinate for hyperlink position
            text.setFont("Helvetica", 14)
            text.setFillColor(red)
            text.textLine(link_text)
            c.drawText(text)
            c.linkURL(link_url, (x, y, x, y), relative=0)

        # Create a new page if not the last page
        if page_idx < len(image_details) - 1:
            c.showPage()

    c.save()   

def merge_pdfs(base_pdf_path, overlay_pdf_path, output_pdf_path):
    # Open the base PDF
    base_pdf = PdfReader(open(base_pdf_path, "rb"))

    # Open the overlay PDF with hyperlinks
    overlay_pdf = PdfReader(open(overlay_pdf_path, "rb"))

    # Create a PDF writer
    writer = PdfWriter()

    # Iterate through the base PDF pages and merge with overlay
    for i in range(len(base_pdf.pages)):
        page = base_pdf.pages[i]

        if i < len(overlay_pdf.pages):
            print("IM IN THIS BITCH")
            page.merge_page(overlay_pdf.pages[i])

        writer.add_page(page)

    # Write out the merged PDF
    with open(output_pdf_path, "wb") as f:
        writer.write(f)
        
def draw_grid(canvas, page_width, page_height, interval=50):
    canvas.setStrokeColorRGB(0.5, 0.5, 0.5)  # Grey color for the grid lines
    canvas.setLineWidth(1)

    # Draw horizontal lines
    for y in reversed(range(int(page_height),0,interval)):
        canvas.line(0, y, page_width, y)
        canvas.drawString(5, y, str(y))

    # Draw vertical lines
    for x in reversed(range(int(page_height),0,interval)):
        canvas.line(x, 0, x, page_height)
        canvas.drawString(x, 5, str(x))

def extract_images_from_pdf_2(pdf_path, output_folder,single_problem_pages,skip_pages_dict):

    pdf_document = fitz.open(pdf_path)

    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Split the page into left and right halves
        width, height = img.size

        strip_width = width // 2
        strip_height = height // 2

        # Process each half
        for side in ['Left', 'Right']:
            print(f"Page: {page_number + 1}, Side: {side}")
            x0 = 0 if side == 'Left' else strip_width
            strip_img = img.crop((x0, 0, x0 + strip_width, height))

            if page_number + 1 in skip_pages_dict:
                print(f"Skipping page {page_number + 1}")
                continue
            elif page_number + 1 in single_problem_pages and side in single_problem_pages[page_number + 1]:
                print(f"Page {page_number + 1} is a single problem page")
                if side == "Right":
                    strip_img.save(f"{output_folder}/page_{page_number + 1}_3_one_problem.png")
                else:
                    strip_img.save(f"{output_folder}/page_{page_number + 1}_1_problem.png")
                continue
            else:
                print(f"Page {page_number + 1} , Side {side}is a multi-problem strip")
                #crop strip into two quadrants
                for i in range(2):
                    if i == 1:
                        top = (height // 2) -25
                    else:
                        top = i * (height // 2)#either at 0 or at half
                    bottom = ((i + 1) * (height // 2)- 25)#either at half or at full 
                    quadrant_img = strip_img.crop((0, top, strip_width, bottom))

                    if side == "Right":
                        quadrant_img.save(f"{output_folder}/page_{page_number + 1}_{i+3}.png")
                    else:
                        quadrant_img.save(f"{output_folder}/page_{page_number + 1}_{i+1}.png")

    pdf_document.close()

        
def extract_images_from_pdf(pdf_path, output_folder):
    # Open the PDF
    pdf_document = fitz.open(pdf_path)

    for page_number in range(len(pdf_document)):
        # Get the page
        page = pdf_document.load_page(page_number)

        # Render the page to an image
        pix = page.get_pixmap()
        img = Image.open(io.BytesIO(pix.tobytes("png")))

        # Dimensions of each quadrant
        width, height = img.size
        quadrant_width = width // 2
        quadrant_height = height // 2

        # Crop each quadrant and save
        for i in range(2):
            for j in range(2):
                left = i * quadrant_width
                top = j * quadrant_height
                right = (i + 1) * quadrant_width
                bottom = (j + 1) * quadrant_height

                cropped_img = img.crop((left, top, right, bottom))
                cropped_img.save(f"{output_folder}/page_{page_number + 1}_quadrant_{i+1}_{j+1}.png")

    pdf_document.close()

def create_drive_folder(drive_service, name, parent_id=None):
    file_metadata = {
        'name': name,
        'mimeType': 'application/vnd.google-apps.folder'
    }
    if parent_id:
        file_metadata['parents'] = [parent_id]
    
    folder = drive_service.files().create(body=file_metadata, fields='id').execute()
    return folder.get('id')

def get_cell_content(sheet_service,spreadsheet_id, range_name):
    result = sheet_service.spreadsheets().values().get(
        spreadsheetId= spreadsheet_id,
        range = range_name
    ).execute()

    print("Result from getting cell content",result)

    values = result.get('values',[])
    
    if not values:
        print("No data found.")
    else:
        print("Values", values)
        return values

def upload_file_to_folder(drive_service, file_path, mime_type, folder_id):
    pop_email = "renan@peaceofpilearning.com"
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [folder_id]
    }
    media = MediaFileUpload(file_path, mimetype=mime_type)
    permission = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': pop_email
    }
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()

    #Sets the permission of the file to anyone with the link
    drive_service.permissions().create(
            fileId = file.get('id'),
            body = {"type": "anyone", "role": "reader"},
            fields = 'id'
    ).execute()
    
    shareable_url = f"https://drive.google.com/uc?id={file.get('id')}"
    return shareable_url

def update_sheet_cell(sheets_service,spreadsheet_id,range_name,urls,cellContent):
    values = []
    
    for idx, url in enumerate(urls):
        values.append([f'=HYPERLINK("{url}", "{cellContent[idx][0]}")'])
    body = {
        'values': values
    }

    result = sheets_service.spreadsheets().values().update(
        spreadsheetId = spreadsheet_id,
        range=range_name,
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
def sort_files_by_page_number(file_names, first_page=False):
    # Extract page numbers from file names and sort by page number
    page_number_file_mapping = []
    for file_name in file_names:
        match = re.search(r'page_(\d+)_', file_name)
        if match:
            page_number = int(match.group(1))
            if first_page and page_number == 1:
                continue  # Skip files for the first page if first_page is True
            page_number_file_mapping.append((page_number, file_name))
    
    # Sort the list by page number
    sorted_files = [file_name for _, file_name in sorted(page_number_file_mapping)]
    return sorted_files










