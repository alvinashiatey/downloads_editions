# app/config.py
import os
from reportlab.lib.pagesizes import HALF_LETTER, LETTER, landscape

# Environment-based config
USER_NAME = os.environ.get('USER') or os.environ.get(
    'LOGNAME') or os.environ.get('USERNAME')
DOWNLOADS_FOLDER = os.path.expanduser('~/Downloads')

# PDF dimensions and settings
HALF_WIDTH, HALF_HEIGHT = HALF_LETTER
LANDSCAPE_WIDTH, LANDSCAPE_HEIGHT = landscape(LETTER)
MARGIN = 10
PIXEL_SIZE = 40
TITLE_TEXT_LENGTH = 50
BOOKLET_PDF_PATH = os.path.join(os.path.sep, 'tmp', 'Booklet.pdf')
TEMP_PIXELATED_PATH = os.path.join(os.path.sep, 'tmp', 'temp_pixelated.jpg')

# Other settings
NUMBER_OF_FILES = 24
