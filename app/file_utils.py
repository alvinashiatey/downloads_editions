import os
import random
from datetime import datetime


def get_sample_files(folder_path, number_of_files, ignore_extensions=None):
    if ignore_extensions is None:
        ignore_extensions = ['.DS_Store', '.ini']
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path)
             if os.path.isfile(os.path.join(folder_path, f))]
    files = [f for f in files if not any(
        f.endswith(ext) for ext in ignore_extensions)]
    if len(files) == 0:
        print('No files found in the specified folder.')
        exit()
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
