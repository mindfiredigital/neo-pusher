"""This module reads data from google drive and dropbox"""
import re
import pandas as pd


class GetLink:
    """Class for formatting and handling Google Drive and Dropbox links"""

    @staticmethod
    def get_google_drive_file_id(link):
        """
        Extracts the file ID from a Google Drive link.

        Parameters:
        link (str): The Google Drive link.

        Returns:
        str: The extracted file ID, or None if no ID is found.
        """
        regex = (
            r"(?:/d/|id=|open\?id=|file/d/|drive.google.com/file/d/|"
            r"drive.google.com/open\?id=|drive.google.com/uc\?id=|"
            r"drive.google.com/file/d/|drive.google.com/open\?id=|"
            r"drive.google.com/uc\?id=)([a-zA-Z0-9_-]{33,})"
        )

        match = re.search(regex, link)
        return match.group(1) if match else None

    @staticmethod
    def read_csv_from_drive(link):
        """
        Reads a CSV file from a Google Drive link.

        Parameters:
        link (str): The Google Drive link.

        Returns:
        tuple: A string representation of the first 5 rows of the DataFrame and the formatted link.
        """
        file_id = GetLink.get_google_drive_file_id(link)
        # print("file ids")
        if file_id:
            formatted_link = f"https://drive.google.com/uc?export=download&id={file_id}"
            try:
                data = pd.read_csv(formatted_link)
                return data.head(5).to_string(), formatted_link
            except Exception as e:
                print(f"Error reading CSV file from Google Drive: {e}")
                return None, formatted_link
        else:
            print("Invalid Google Drive link.")
            return None, link

    @staticmethod
    def get_dropbox_link(link):
        """
        Reads a CSV file from a Dropbox link.

        Parameters:
        link (str): The Dropbox link.

        Returns:
        tuple: A string representation of the first 5 rows of the DataFrame and the formatted link.
        """
        formatted_link = link.replace(
            "www.dropbox.com", "dl.dropboxusercontent.com"
        ).replace("?dl=0", "")
        try:
            df = pd.read_csv(formatted_link)
            return df.head(5).to_string(), formatted_link
        except Exception as e:
            print(f"Error reading CSV file from Dropbox: {e}")
            return None, formatted_link
