import os
import random
import subprocess
import sys
from datetime import datetime
from typing import List, Optional, Tuple


def get_sample_files(
    folder_path: str,
    number_of_files: int,
    ignore_extensions: Optional[List[str]] = None
) -> List[str]:
    """
    Returns a random sample of file paths from the specified folder, excluding files with certain extensions.

    Args:
        folder_path (str): Path to the folder containing files.
        number_of_files (int): Number of files to sample.
        ignore_extensions (Optional[List[str]]): List of file extensions to ignore.
            Defaults to ['.DS_Store', '.ini'].

    Returns:
        List[str]: A list of sampled file paths. Returns an empty list if no files are found.
    """
    if ignore_extensions is None:
        ignore_extensions = ['.DS_Store', '.ini']

    try:
        all_files = os.listdir(folder_path)
    except Exception as e:
        print(f"Error reading folder '{folder_path}': {e}")
        return []

    files = [
        os.path.join(folder_path, f)
        for f in all_files
        if os.path.isfile(os.path.join(folder_path, f)) and not any(f.endswith(ext) for ext in ignore_extensions)
    ]

    if not files:
        print('No files found in the specified folder.')
        return []

    return random.sample(files, min(number_of_files, len(files)))


def analyze_files_by_creation_date(
    folder_path: str,
    ignore_extensions: Optional[List[str]] = None
) -> Optional[Tuple[Tuple[str, datetime], Tuple[str, datetime]]]:
    """
    Scans the folder and returns the file with the earliest creation date and the file with the latest creation date.

    Args:
        folder_path (str): Path to the folder containing files.
        ignore_extensions (Optional[List[str]]): List of file extensions to ignore.
            Defaults to ['.DS_Store', '.ini'].

    Returns:
        Optional[Tuple[Tuple[str, datetime], Tuple[str, datetime]]]:
            A tuple containing two tuples:
                ((oldest_file_name, oldest_date), (recent_file_name, recent_date)).
            Returns None if no files are found.
    """
    if ignore_extensions is None:
        ignore_extensions = ['.DS_Store', '.ini']

    try:
        all_files = os.listdir(folder_path)
    except Exception as e:
        print(f"Error reading folder '{folder_path}': {e}")
        return None

    files = [
        os.path.join(folder_path, f)
        for f in all_files
        if os.path.isfile(os.path.join(folder_path, f)) and not any(f.endswith(ext) for ext in ignore_extensions)
    ]

    if not files:
        print('No files found in the specified folder.')
        return None

    oldest_file = min(files, key=os.path.getmtime)
    recent_file = max(files, key=os.path.getmtime)

    oldest_date = datetime.fromtimestamp(os.path.getmtime(oldest_file))
    recent_date = datetime.fromtimestamp(os.path.getmtime(recent_file))

    return ((os.path.basename(oldest_file), oldest_date),
            (os.path.basename(recent_file), recent_date))


def open_file_in_default_app(file_path: str) -> None:
    """
    Opens the specified file using the default application associated with its file type.

    Args:
        file_path (str): Path to the file to open.
    """
    try:
        if sys.platform.startswith('darwin'):
            subprocess.run(['open', file_path], check=True)
        elif os.name == 'nt':
            os.startfile(file_path)  # Windows
        elif os.name == 'posix':
            subprocess.run(['xdg-open', file_path], check=True)
        else:
            print(f"Unsupported operating system: cannot open file {
                  file_path}")
    except Exception as e:
        print(f"Failed to open file {file_path}: {e}")
