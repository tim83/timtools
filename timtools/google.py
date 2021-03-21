#! /usr/bin/python3
"""Deals with downloading en uploading data from google sheets"""

import locale
import os
import pickle
import pandas as pd
from typing import List
import datetime as dt
import pytz

import google.oauth2.credentials
import googleapiclient.discovery
from apiclient.http import MediaIoBaseDownload, MediaFileUpload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow

from timtools import settings

SCOPES: List[str] = [
	'https://www.googleapis.com/auth/spreadsheets',
	'https://www.googleapis.com/auth/drive'
]


def _obtain_credentials() -> google.oauth2.credentials.Credentials:
	"""Logs the user in and returns the credentials"""

	token_file: str = os.path.join(settings.CACHE_DIR, '/google_token.pickle')

	# Load credentials if they exist
	if os.path.exists(token_file):
		with open(token_file, 'rb') as token:
			credentials = pickle.load(token)
	else:
		credentials = None

	# If there are no (valid) credentials available, let the user log in.
	if not credentials or not credentials.valid:
		if credentials and credentials.expired and credentials.refresh_token:
			credentials.refresh(Request())
		else:
			flow = InstalledAppFlow.from_client_secrets_file(
				settings.GOOGLE_CLIENT_SECRET_FILE,
				SCOPES
			)
			credentials = flow.run_local_server(port=0)
		# Save the credentials for the next run
		token_dir: str = os.path.dirname(token_file)
		if not os.path.exists(token_dir):
			os.mkdir(token_dir)
		with open(token_file, 'wb') as token:
			pickle.dump(credentials, token)

	return credentials


def _load_sheet_api() -> googleapiclient.discovery.Resource:
	"""Returns the API object for manipulating sheets"""
	credentials = _obtain_credentials()
	service = googleapiclient.discovery.build(
		'sheets', 'v4',
		credentials=credentials,
		cache_discovery=False
	)
	sheet = service.spreadsheets()
	return sheet


def _load_drive_api() -> googleapiclient.discovery.Resource:
	"""Returns the API object for manipulating files"""
	credentials = _obtain_credentials()
	service = googleapiclient.discovery.build(
		'drive', 'v3',
		credentials=credentials,
		cache_discovery=False
	)
	return service


def import_spreadsheet(
		sheet_id: str,
		selected_range: str,
		column_header: bool = True,
		row_index: bool = True
) -> pd.DataFrame:
	"""Import the content from a Google Sheet as a pandas dataframe
	:param sheet_id: The ID of the sheet (can be found in the URL of the sheet)
	:param selected_range: The range that contains the to be imported data (e.g. Blad1!A1:B5)
	:param column_header: Treat the first column as a header
	:param row_index: Treat the first row as a header
	:return The dataframe containing the selected data from the sheet"""

	sheet = _load_sheet_api()
	result = sheet.values().get(spreadsheetId=sheet_id, range=selected_range).execute()
	values = result.get('values', [])
	locale.setlocale(locale.LC_NUMERIC, '')

	if column_header:
		data_values = values[1:]
		column_headers = values[0]
	else:
		data_values = values
		column_headers = None
	data = pd.DataFrame(data_values, columns=column_headers, dtype="float")

	if row_index:
		data.set_index(column_headers[0], inplace=True)

	return data


def export_to_sheet(sheet_id: str, selected_range: str, data: pd.DataFrame):
	"""
	Exports data to a google sheet

	:rtype: None
	:param data: A matrix containing every match and its score
	:param sheet_id: The ID of the sheet (can be found in the URL of the sheet)
	:param selected_range: The range that contains the to be imported data (e.g. Blad1!A1:B5)
	"""
	sheet = _load_sheet_api()
	sheet.values().update(
		spreadsheetId=sheet_id,
		valueInputOption='RAW',
		range=selected_range,
		body=dict(
			majorDimension='ROWS',
			values=data.T.reset_index().T.values.tolist())
	).execute()


def upload_file(filename: str, file_id: str = None):
	""""
	Uploads or updates a file in Google Drive

	:rtype: None
	:param filename: The file thats needs to be uploaded
	:param file_id: The ID of the to be uploaded file if not provided, a new file will be created
	"""
	basename: str = os.path.basename(filename)
	title, ext = os.path.splitext(filename)

	drive_api = _load_drive_api()

	file_metadata = {'name': basename, 'title': title}

	media_body = MediaFileUpload(filename, resumable=True)

	if file_id is None:
		file = drive_api.files().create(
			body=file_metadata,
			media_body=media_body,
			fields='id'
		).execute()
		file_id = file.get('ID')
		print(f"The file ID is {file_id}")
	else:
		drive_api.files().update(
			fileId=file_id,
			body=file_metadata,
			media_body=media_body
		).execute()


def modifiedDate(file_id: str) -> dt.datetime:
	"""
	Returns the datetime when a file was last modified
	:param file_id: The file ID of the file
	:return: The modified time
	"""
	drive_api = _load_drive_api()
	file = drive_api.files().get(fileId=file_id, fields="modifiedTime").execute()
	date_str = file.get('modifiedTime')
	date = dt.datetime.strptime(date_str, '%Y-%m-%dT%H:%M:%S.%fZ')
	date_utc = date.replace(tzinfo=pytz.utc)
	return date_utc.astimezone()


if __name__ == "__main__":
	TEST_SHEET_ID = '1FdGvHITMbk_DyONFmE00IcZY79He2SWNUT35klXJu40'
	IMPORT_RANGE = 'Import Data!A1:F6'

	md = modifiedDate(
		TEST_SHEET_ID,
	)
	print(md)
