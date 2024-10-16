from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import googleapiclient.errors

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

def change_ownership(file_id, new_email, drive_service):
    """
    Change the ownership of a specific file in Google Drive.

    :param file_id: ID of the file to change ownership for
    :param new_email: Email address of the new owner
    :param drive_service: Authenticated Google Drive service
    """
    try:
        # Define the new permission for the new owner
        new_permission = {
            'type': 'user',
            'role': 'owner',
            'emailAddress': new_email
        }

        # Transfer ownership of the file
        drive_service.permissions().create(
            fileId=file_id,           # File ID to change ownership for
            body=new_permission,      # The new permission details
            transferOwnership=True,    # Set transferOwnership to True
            #useDomainAdminAccess=True # Set useDomainAdminAccess to True
        ).execute()

        print(f"Ownership of file {file_id} has been transferred to {new_email}")

    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred in change_ownership: {e}")
        return None


def get_files_in_folder(drive_service, folder_id, owner_email):
    """
    Retrieve all files within a specific folder owned by a specific email.

    :param drive_service: Authenticated Google Drive service
    :param folder_id: ID of the folder to search for files
    :param owner_email: Email of the owner to filter files
    :return: A list of files inside the folder owned by the specified email
    """
    files = []
    page_token = None
    try:
        while True:
            # Search for files within the given folder
            response = drive_service.files().list(
                q=f"'{folder_id}' in parents and '{owner_email}' in owners",  # Query to get files inside the folder owned by the email
                spaces='drive',                 # Look in Google Drive
                fields='nextPageToken, files(id, name, owners(emailAddress))',  # Return file ID, name, and owners
                pageToken=page_token            # Handle pagination
            ).execute()

            files.extend(response.get('files', []))  # Append the files found
            page_token = response.get('nextPageToken', None)  # Check if more pages of results

            if page_token is None:
                break

    except googleapiclient.errors.HttpError as e:
        print(f"An error occurred in get_files_in_folder: {e}")
        return None

    return files


def transfer_folder_ownership(folder_id, new_email):
    """
    Transfer the ownership of all files in a folder to a new email.

    :param folder_id: The ID of the folder containing the files
    :param new_email: The email address of the new owner
    """
    # Define the scopes and service account credentials
    scopes = ['https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file']
    service_account_file = 'service_credentials.json'

    # Authenticate using the service account credentials
    creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    delegated_credentials = creds.with_subject(new_email)
    drive_service = build('drive', 'v3', credentials=delegated_credentials)
    owner_email = "editor@pdf-merger-405723.iam.gserviceaccount.com"
    # Get all the files in the specified folder
    files = get_files_in_folder(drive_service, folder_id, owner_email)
    if not files:
        print(f"No files found in folder with ID: {folder_id}")
        return 

    print(f"Files found in folder {folder_id}:")

    # Iterate over all files and change their ownership
    for file in files:
        print(f"File name: {file['name']} (File ID: {file['id']})")
        change_ownership(file['id'], new_email, drive_service)

def update_sheet_cell_with_reuploaded_folder(sheet_service,
                                             drive_service,
                                             spreadsheet_id,
                                             range_name
                                             ):
    pass
if __name__ == "__main__":
    # Example usage
    new_email = 'renan@peaceofpilearning.com'  # Replace with the email of the new owner
    spreadsheet_id = '1NR1R1TFrkmbO7FSilfjV9VbEd28aPYY_lJf9NIApZjo'
    range_name = input("Enter the range name (e.g., 'A1:B2'): ")
    #transfer_folder_ownership(folder_id,new_email)


    scopes = ['https://www.googleapis.com/auth/drive',
              'https://www.googleapis.com/auth/drive.file']
    service_account_file = 'service_credentials.json'

    # Authenticate using the service account credentials
    creds = Credentials.from_service_account_file(service_account_file, scopes=scopes)
    delegated_credentials = creds.with_subject(new_email)
    drive_service = build('drive', 'v3', credentials=delegated_credentials)

    sheets_service = build('sheets', 'v4', credentials=creds)
    print(get_cell_content(sheets_service, spreadsheet_id, range_name))