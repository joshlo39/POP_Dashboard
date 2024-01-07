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
# from pypdf import PdfReader, PdfWriter
# from reportlab.pdfgen import canvas
# from reportlab.lib.pagesizes import letter
# def create_pdf_with_hyperlink_test(file_path, url, text, x, y):
#     can = canvas.Canvas(file_path, pagesize=letter)
#     can.drawString(x, y, text)
#     can.linkURL(url, (x, y, x + 100, y + 10), relative=1)
#     can.save()

# def add_hyperlink_to_pdf(input_pdf_path, output_pdf_path, url, text, x, y, page_number):
#     # Create a new PDF with the hyperlink
#     packet = io.BytesIO()
#     can = canvas.Canvas(packet, pagesize=letter)
#     can.drawString(x, y, text)
#     can.linkURL(url, (x, y, x + 100, y + 10), relative=1)
#     can.save()

    # # Move to the beginning of the StringIO buffer
    # packet.seek(0)
    # new_pdf = PdfReader(packet)
    #
    # # Read the existing PDF
    # existing_pdf = PdfReader(input_pdf_path)
    # writer = PdfWriter()
    #
    # # Add all pages from the existing PDF
    # for i, page in enumerate(existing_pdf.pages):
    #     with open("page.pdf", "wb") as f:
    #         writer.write(f)
    #     if i == page_number:
    #         page.merge_page(new_pdf.pages[0])
    #     writer.add_page(page)

    # Write the output PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)
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

