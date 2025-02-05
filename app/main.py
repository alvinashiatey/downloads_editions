import argparse
import logging
from app import config, file_utils, pdf_utils

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Booklet PDF from your Downloads folder.")
    parser.add_argument("--folder", default=config.DOWNLOADS_FOLDER,
                        help="Folder path to scan for files")
    parser.add_argument(
        "--files", type=int, default=config.NUMBER_OF_FILES, help="Number of files to use")
    args = parser.parse_args()

    try:
        files = file_utils.get_sample_files(args.folder, args.files)
        pdf_utils.create_booklet_pdf(files)
    except Exception as e:
        logger.exception("An error occurred during booklet creation.")


if __name__ == '__main__':
    main()
