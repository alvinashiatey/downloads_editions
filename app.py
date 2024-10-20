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

NAME = os.environ.get('USER') or os.environ.get(
    'LOGNAME') or os.environ.get('USERNAME')
PAGE_WIDTH, PAGE_HEIGHT = HALF_LETTER
NUMBER_OF_FILES = 22
MARGIN = 15
PDF_WRITER = PdfWriter()
PDF_PATH = 'Downloads.pdf'
TEMP_PIXELATED_PATH = 'temp_pixelated.png'
downloads_folder = os.path.expanduser('~/Downloads')
styles = getSampleStyleSheet()
title_style = styles["Normal"]
title_style.paddingLeft = 0


def about_project_page(c, folder_path):
    c.setPageSize(HALF_LETTER)
    about_style = styles["Normal"]
    about_style.fontSize = 12
    about_style.leading = 12 * 1.2
    about_style.paddingLeft = 0

    about_text = f'''This edition delves into {NAME.capitalize()}'s Download folder, capturing its contents as of {datetime.now().strftime(
        '%m.%d.%Y')}. It reflects on the digital clutter that accumulates over time and the narratives hidden within the files we download. The files in this edition were randomly selected, with pixelated images to ensure privacy. This project is an ongoing exploration of digital archives.'''
    about_text = about_text.replace('\n', '<BR/>')
    about_text = Paragraph(about_text, about_style)
    about_text_height = about_text.wrapOn(
        c, PAGE_WIDTH-(MARGIN*2), PAGE_HEIGHT-(MARGIN*2))
    about_text.drawOn(c, MARGIN, PAGE_HEIGHT - about_text_height[1] - MARGIN)
    c.showPage()


def justify_text(c, text, x, y, width):
    words = text.split('|')
    total_length = sum(c.stringWidth(word, "Helvetica", 12) for word in words)
    spaces_needed = max(len(words) - 1, 1)  # Ensure at least one space needed

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
    title_style.fontSize = 62
    title_style.leading = 60
    cover_page = Paragraph(
        '''Downloads/<BR/>Downloads<BR/>.pdf''', title_style)
    cover_page_height = cover_page.wrapOn(
        c, PAGE_WIDTH-(MARGIN*2), PAGE_HEIGHT-(MARGIN*2))
    cover_page.drawOn(
        c, MARGIN, PAGE_HEIGHT - cover_page_height[1])
    c.showPage()


def generate_titles(c, title):
    title_style.fontSize = 62
    title_style.leading = 60
    c_text = Paragraph(f'{title}', title_style)
    c_text_height = c_text.wrapOn(
        c, PAGE_WIDTH - (MARGIN*2), PAGE_HEIGHT-(MARGIN*2))
    c_text.drawOn(c, MARGIN, PAGE_HEIGHT - c_text_height[1])


def empty_page(c):
    c.setPageSize(HALF_LETTER)
    c.showPage()


def pixelate_image(image_path, pixel_size, brightness_factor=1.2):
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
    empty_page(c)
    about_project_page(c, downloads_folder)
    for file in structured_files:
        c.setPageSize(HALF_LETTER)
        add_image(c, file)
        center_text = f'{file["date"]}|{
            file["extension"]}|{file["size"]}'
        justify_text(c, center_text, MARGIN,
                     PAGE_HEIGHT/2, PAGE_WIDTH-(MARGIN*2))
        title = shorten_text(file['title'], 50)
        generate_titles(c, title)
        page_number(c, structured_files.index(file) + 1)
        c.showPage()
    empty_page(c)
    c.save()


def randomly_pick_files(files, n):
    return random.sample(files, n)


def filter_files_no_folders(folder_path, files):
    return [file for file in files if os.path.isfile(os.path.join(folder_path, file))]


def filter_file_remove_types(files, types):
    return [file for file in files if file.split('.')[-1] not in types]


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
    filtered_files = filter_file_remove_types(filtered_files, [
        'DS_Store'])
    random_files = randomly_pick_files(filtered_files, NUMBER_OF_FILES)
    sorted_files = sort_files(random_files)
    structured_files = structure_files_to_dict(folder_path, sorted_files)
    generate_pdf(structured_files)
    print('PDF generated')


if __name__ == '__main__':
    # NAME = input("Please enter your name: ")
    print_files(downloads_folder)
