import os
import random
from PIL import Image, ImageEnhance
from datetime import datetime
from pypdf import PdfWriter
from reportlab.lib.pagesizes import HALF_LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet

PAGE_WIDTH, PAGE_HEIGHT = HALF_LETTER
NUMBER_OF_FILES = 22
PDF_WRITER = PdfWriter()
PDF_PATH = 'Downloads.pdf'
TEMP_PIXELATED_PATH = 'temp_pixelated.png'
downloads_folder = os.path.expanduser('~/Downloads')
styles = getSampleStyleSheet()
title_style = styles["Normal"]
title_style.fontSize = 62
title_style.leading = 60
title_style.paddingLeft = 0


def justify_text(c, text, x, y, width):
    words = text.split('|')
    total_length = sum(c.stringWidth(word, "Helvetica", 12)
                       for word in words)  # Calculate total width of all words
    spaces_needed = len(words) - 1  # Number of spaces between words
    if spaces_needed == 0:
        c.drawString(x, y, text)
        return

    total_space = width - total_length
    space_between_words = total_space / spaces_needed

    current_x = x
    for word in words:
        c.drawString(current_x, y, word)  # Draw the word
        current_x += c.stringWidth(word, "Helvetica", 12) + \
            space_between_words  # Move x position


def shorten_text(text, max_length):
    return text if len(text) <= max_length else text[:max_length] + '...'


def page_number(c, page_num):
    c.drawRightString(PAGE_WIDTH-5, 10, f'{page_num}')


def generate_cover_page(c):
    cover_page = Paragraph(
        '''Downloads/<BR/>Downloads<BR/>.pdf''', title_style)
    cover_page_height = cover_page.wrapOn(c, PAGE_WIDTH, PAGE_HEIGHT)
    cover_page.drawOn(c, 0, PAGE_HEIGHT - cover_page_height[1])
    c.showPage()


def empty_page(c, page_num):
    c.setPageSize(HALF_LETTER)
    c.showPage()


def pixelate_image(image_path, pixel_size, brightness_factor=1.8):
    with Image.open(image_path) as img:
        img = img.convert("L")
        img_small = img.resize(
            (img.width // pixel_size, img.height // pixel_size),
            Image.NEAREST)
        temp_path = TEMP_PIXELATED_PATH
        img_pixelated = img_small.resize(img.size, Image.NEAREST)
        enhancer = ImageEnhance.Brightness(img_pixelated)
        img_pixelated = enhancer.enhance(brightness_factor)
        img_pixelated.save(temp_path)
    return temp_path


def remove_temp_files():
    if os.path.exists(TEMP_PIXELATED_PATH):
        os.remove(TEMP_PIXELATED_PATH)


def add_image(c, file):
    if file['extension'].lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
        pixelate_image_path = pixelate_image(file['path'], 30)
        image = ImageReader(pixelate_image_path)
        img_width, img_height = image.getSize()
        aspect_ratio = img_width / img_height
        new_width = PAGE_WIDTH - 20
        new_height = new_width / aspect_ratio
        c.drawImage(image, 10, PAGE_HEIGHT-new_height-10,
                    width=new_width, height=new_height)
        remove_temp_files()


def generate_pdf(structured_files):
    c = canvas.Canvas(PDF_PATH, pagesize=HALF_LETTER)
    generate_cover_page(c)
    empty_page(c, 2)
    for file in structured_files:
        c.setPageSize(HALF_LETTER)
        add_image(c, file)
        center_text = f'{file["date"]}|{
            file["extension"]}|{file["size"]}'
        justify_text(c, center_text, 10, PAGE_HEIGHT/2, PAGE_WIDTH-20)
        title = shorten_text(file['title'], 50)
        c_text = Paragraph(f'{title}', title_style)
        c_text_height = c_text.wrapOn(c, PAGE_WIDTH - 20, PAGE_HEIGHT)
        c_text.drawOn(c, 5, PAGE_HEIGHT - c_text_height[1])
        page_number(c, structured_files.index(file) + 1)
        c.showPage()
    empty_page(c, len(structured_files) + 2)
    c.save()


def randomly_pick_files(files, n):
    return random.sample(files, n)


def filter_files_no_folders(folder_path, files):
    return [file for file in files if os.path.isfile(os.path.join(folder_path, file))]


def sort_files(files):
    files.sort(key=lambda x: x.split('.')[-1])
    return files


def structure_files_to_dict(folder_path, files):
    return [
        {
            'title': file_name.split('.')[0],
            'date':  datetime.fromtimestamp(os.path.getmtime(os.path.join(folder_path, file_name))).strftime('%m.%d.%Y'),
            'extension': file_name.split('.')[-1],
            'size': os.path.getsize(os.path.join(folder_path, file_name)),
            'path': os.path.join(folder_path, file_name)
        }
        for file_name in files
    ]


def print_files(folder_path):
    if not os.path.exists(folder_path):
        print('Downloads folder does not exist')
        return

    files = os.listdir(folder_path)
    filtered_files = filter_files_no_folders(folder_path, files)
    random_files = randomly_pick_files(filtered_files, NUMBER_OF_FILES)
    sorted_files = sort_files(random_files)
    structured_files = structure_files_to_dict(folder_path, sorted_files)
    generate_pdf(structured_files)
    print('PDF generated')


if __name__ == '__main__':
    print_files(downloads_folder)
