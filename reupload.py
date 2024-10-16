import logging
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Authenticate and initialize the Drive and Sheets services
scopes = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/drive.file',
          'https://www.googleapis.com/auth/spreadsheets']
try:
    creds = Credentials.from_service_account_file('service_credentials.json', scopes=scopes)
    drive_service = build('drive', 'v3', credentials=creds)
    sheets_service = build('sheets', 'v4', credentials=creds)
    logging.info("Successfully authenticated and initialized services.")
except Exception as e:
    logging.error(f"Failed to authenticate and initialize services: {e}")
    raise

def list_files_in_folder(drive_service, folder_id):
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        logging.info(f"Listed files in folder {folder_id}.")
        return results.get('files', [])
    except HttpError as error:
        logging.error(f"An error occurred while listing files in folder {folder_id}: {error}")
        return []
def create_file_name_mapping(old_folder_id,new_folder_id):
        #create a map where the key is the name of the file and the value is the url 
        #{name: new_url}
    old_files= list_files_in_folder(drive_service, old_folder_id)
    new_files= list_files_in_folder(drive_service, new_folder_id)
    file_name_mapping = {}
    for old_file in old_files:
        for new_file in new_files:
            if old_file['name'] == new_file['name']:
                file_name_mapping[old_file['name']] = new_file['id']
    logging.info(f"File name mapping: {file_name_mapping}")
    return file_name_mapping

def extract_file_name_from_url(url):
    """
    Extract the file ID from the given Google Drive URL.

    :param url: The URL of the file.
    :return: The file ID extracted from the URL.
    """
    try:
        # Extract the file ID from the URL
        file_id = url.split('/d/')[1].split('/')[0]
        logging.info(f"Extracted file ID: {file_id} from URL: {url}")
        return file_id
    except IndexError as e:
        logging.error(f"Failed to extract file ID from URL: {url}. Error: {e}")
        return None
def create_new_urls(file_name_mapping):
    new_urls = {}
    for file_name, new_file_id in file_name_mapping.items():
        new_url = f"https://drive.google.com/uc?id={new_file_id}"
        new_urls[file_name] = new_url
    logging.info(f"Created new URLs: {new_urls}")
    return new_urls

def update_sheet_with_new_urls(sheets_service, spreadsheet_id, range_name, url_mapping):
    values = []
    for idx,(file_name,new_url) in enumerate(url_mapping.items()):
        values.append([f'=HYPERLINK("{new_url}", "Q{idx+1}")'])  # Adjust the display text as needed

    body = {
        'values': values
    }

    try:
        result = sheets_service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption="USER_ENTERED",
            body=body
        ).execute()
        logging.info(f"Updated sheet {spreadsheet_id} with new URLs.")
        return result
    except HttpError as error:
        logging.error(f"An error occurred while updating the sheet {spreadsheet_id}: {error}")
        return None

def get_old_urls_from_folder(drive_service, folder_id):
    """
    Retrieve all old URLs from the specified folder.

    :param drive_service: Authorized Drive API service instance.
    :param folder_id: ID of the folder to retrieve URLs from.
    :return: List of URLs.
    """
    try:
        query = f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'"
        results = drive_service.files().list(q=query, fields="files(id, name, webViewLink)").execute()
        items = results.get('files', [])
        old_urls = [item['webViewLink'] for item in items]
        logging.info(f"Retrieved old URLs from folder {folder_id}.")
        return old_urls
    except HttpError as error:
        logging.error(f"An error occurred while retrieving old URLs from folder {folder_id}: {error}")
        return []
def sort_file_name_mapping(file_name_mapping):
    def extract_numbers(file_name):
        parts = file_name.split('_')
        return int(parts[1]), int(parts[2].split('.')[0])

    sorted_mapping = dict(sorted(file_name_mapping.items(), key=lambda item: extract_numbers(item[0])))
    return sorted_mapping
# Example usage
if __name__ == "__main__":
    old_folder_id = '1Q5WDQ3VCnmjvEzGV6JxR6vJacnx1QK7e'
    new_folder_id = '1NyN-sgRRfQKHXnZNLrtDjSpCvF12U1LD'
    spreadsheet_id = '1NR1R1TFrkmbO7FSilfjV9VbEd28aPYY_lJf9NIApZjo'
    range_name = f"{'Sheet1'}!G2788:G2795"  # Adjust the range as needed

    file_name_mapping= create_file_name_mapping(old_folder_id,new_folder_id)
    new_urls_mapping= create_new_urls(file_name_mapping)
    #TODO: Need to sort the new_urls_mapping by the file_name in order of number
    new_urls_mapping= sort_file_name_mapping(new_urls_mapping)
    logging.info(f"Sorted new URLs mapping: {new_urls_mapping}")
    try:
        update_sheet_with_new_urls(sheets_service, spreadsheet_id, range_name, new_urls_mapping)
    except Exception as e:
        logging.error(f"An error occurred while updating the sheet {spreadsheet_id}: {e}")

        