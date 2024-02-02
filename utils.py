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
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from reportlab.lib.colors import red  
import fitz #PyMuPdf




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
            img = Image.open(image_path)
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
    for y in range(0, int(page_height), interval):
        canvas.line(0, y, page_width, y)
        canvas.drawString(5, y, str(y))

    # Draw vertical lines
    for x in range(0, int(page_width), interval):
        canvas.line(x, 0, x, page_height)
        canvas.drawString(x, 5, str(x))




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
