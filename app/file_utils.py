import subprocess
import os
import random
from datetime import datetime


def get_sample_files(folder_path, number_of_files, ignore_extensions=None):
    """
    Returns a random sample of files from the specified folder.

    Parameters:
      folder_path: Path to the folder containing files.
      number_of_files: Number of files to sample.
      ignore_extensions: List of file extensions to ignore.

    Returns:
      A list of sampled file paths.
    """
    if ignore_extensions is None:
        ignore_extensions = ['.DS_Store', '.ini']

    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and not any(f.endswith(ext) for ext in ignore_extensions)
    ]

    if not files:
        print('No files found in the specified folder.')
        return []

    return random.sample(files, min(number_of_files, len(files)))


def analyze_files_by_creation_date(folder_path, ignore_extensions=None):
    """
    Scans the folder and returns:
      - The file with the earliest creation date (oldest added)
      - The file with the latest creation date (recently added)

    Parameters:
      folder_path: Path to the folder containing files.

    Returns:
      A tuple ((oldest_added_file, oldest_date), (recent_added_file, recent_date)).
      The creation dates are also returned as a formatted string.
    """
    if ignore_extensions is None:
        ignore_extensions = ['.DS_Store', '.ini']

    files = [
        os.path.join(folder_path, f)
        for f in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, f)) and not any(f.endswith(ext) for ext in ignore_extensions)
    ]

    if not files:
        print('No files found in the specified folder.')
        return None

    oldest_added_file = min(files, key=os.path.getmtime)
    recent_added_file = max(files, key=os.path.getmtime)

    return (
        (os.path.basename(oldest_added_file), datetime.fromtimestamp(
            os.path.getmtime(oldest_added_file))),
        (os.path.basename(recent_added_file), datetime.fromtimestamp(
            os.path.getmtime(recent_added_file)))
    )


def open_file_in_default_app(file_path):
    """
    Opens the specified file using the default application associated with its file type.

    Parameters:
      file_path: Path to the file to be opened.

    Returns:
      None
    """
    try:
        if os.name == 'nt':  # Windows
            os.startfile(file_path)
        elif os.name == 'posix':  # macOS and Linux
            subprocess.run(['open', file_path], check=True)
    except Exception as e:
        print(f"An error occurred while trying to open the file: {e}")
