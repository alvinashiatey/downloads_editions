import argparse
import logging
from app import config, file_utils, pdf_utils

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Generate a Booklet PDF from your Downloads folder.",
        epilog=(
            "This tool scans your Downloads folder (or another specified folder), "
            "selects a random sample of files, and generates a booklet PDF reflecting "
            "the digital clutter of your files. Use the --folder flag to specify a custom "
            "folder, and the --files flag to set how many files should be included. "
            "Example usage:\n"
            "    downloads-editions --folder ~/Downloads --files 24\n"
            "The generated PDF will be automatically opened in your default application."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        "--folder",
        default=config.DOWNLOADS_FOLDER,
        help="Folder path to scan for files (default: %(default)s)"
    )
    parser.add_argument(
        "--files",
        type=int,
        default=config.NUMBER_OF_FILES,
        help="Number of files to use (default: %(default)s)"
    )
    args = parser.parse_args()

    try:
        files = file_utils.get_sample_files(args.folder, args.files)
        pdf_utils.create_booklet_pdf(files)
    except Exception as e:
        logger.exception("An error occurred during booklet creation.")


if __name__ == '__main__':
    main()
