import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from app import config, image_utils, file_utils

styles = getSampleStyleSheet()
title_style = styles["Normal"]
title_style.paddingLeft = 0

oldest_added_file, recent_added_file = file_utils.analyze_files_by_creation_date(
    config.DOWNLOADS_FOLDER)


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


def draw_page_content(c, file_info, page_num):
    # Image
    if file_info['extension'].lower() in ['jpg', 'jpeg', 'png', 'gif', 'bmp']:
        if not hasattr(c._doc, "ExtGState"):
            c._doc.ExtGState = {}
        ext_gs_name = "GS1"
        blend_mode = "multiply"
        gs_dict_code = f"<< /Type /ExtGState /BM /{blend_mode} >>"
        c._doc.ExtGState[ext_gs_name] = gs_dict_code
        c.saveState()
        c._code.append(f"/{ext_gs_name} gs")
        image_utils.pixelate_image(file_info['path'])
        image = ImageReader(config.TEMP_PIXELATED_PATH)
        img_width, img_height = image.getSize()
        aspect_ratio = img_width / img_height
        new_width = config.HALF_WIDTH - 2 * config.MARGIN
        new_height = new_width / aspect_ratio
        c.drawImage(image, config.MARGIN, config.HALF_HEIGHT - new_height - config.MARGIN,
                    width=new_width, height=new_height)
        c.restoreState()
        os.remove(config.TEMP_PIXELATED_PATH)

    # Title
    title_style.fontSize = 60
    title_style.leading = 60
    title = os.path.basename(file_info['path'])
    title = shorten_text(title, config.TITLE_TEXT_LENGTH)
    c_text = Paragraph(f'{title}', title_style)
    c_text.wrapOn(c, config.HALF_WIDTH - (2 * config.MARGIN),
                  config.HALF_HEIGHT - (2 * config.MARGIN))
    c_text.drawOn(c, config.MARGIN, config.HALF_HEIGHT -
                  (c_text.height - (2 * config.MARGIN) * 2))

    # Centered Text
    center_text = f'{file_info["date"]} | {
        file_info["extension"]} | {file_info["size"]} bytes'
    justify_text(c, center_text, config.MARGIN, config.HALF_HEIGHT /
                 2, config.HALF_WIDTH - 2 * config.MARGIN)
    # Page Number
    c.drawRightString(config.HALF_WIDTH - config.MARGIN,
                      config.MARGIN, str(page_num))


def shorten_text(text, max_length):
    return text if len(text) <= max_length else text[:max_length] + '...'


def create_booklet_pdf(files):
    # Prepare file information
    file_infos = []
    for f in files:
        file_infos.append({
            'path': f,
            'title': os.path.splitext(os.path.basename(f))[0],
            'date': datetime.fromtimestamp(os.path.getmtime(f)).strftime('%m.%d.%Y'),
            'extension': os.path.splitext(f)[1][1:],
            'size': os.path.getsize(f)
        })

    # Create content pages
    pages = []

    # Cover Page
    pages.append({'type': 'cover'})

    # Empty Page
    pages.append({'type': 'empty'})

    # Content Pages
    for idx, file_info in enumerate(file_infos):
        pages.append(
            {'type': 'content', 'file_info': file_info, 'page_num': idx + 1})

    # Empty Page
    pages.append({'type': 'empty'})

    # About Page
    pages.append({'type': 'about'})

    # Ensure total pages is a multiple of 4
    total_pages = len(pages)
    if total_pages % 4 != 0:
        for _ in range(4 - (total_pages % 4)):
            pages.append({'type': 'empty'})

    # Rearrange pages for booklet printing
    num_sheets = len(pages) // 4
    booklet_order = []
    for sheet in range(num_sheets):
        # Front side
        booklet_order.append(pages[-(2 * sheet + 1)])
        booklet_order.append(pages[2 * sheet])
        # Back side
        booklet_order.append(pages[2 * sheet + 1])
        booklet_order.append(pages[-(2 * sheet + 2)])

    # Create the booklet PDF
    c = canvas.Canvas(config.BOOKLET_PDF_PATH, pagesize=(
        config.LANDSCAPE_WIDTH, config.LANDSCAPE_HEIGHT))
    for i in range(0, len(booklet_order), 2):
        # New LANDSCAPE page
        c.setPageSize((config.LANDSCAPE_WIDTH, config.LANDSCAPE_HEIGHT))

        # Left Half
        c.saveState()
        c.translate(0, 0)
        draw_half_page(c, booklet_order[i])
        c.restoreState()

        # Right Half
        c.saveState()
        c.translate(config.LANDSCAPE_WIDTH / 2, 0)
        draw_half_page(c, booklet_order[i + 1])
        c.restoreState()

        c.showPage()
    c.save()
    print(f'Booklet PDF generated: {config.BOOKLET_PDF_PATH}')
    file_utils.open_file_in_default_app(config.BOOKLET_PDF_PATH)


def draw_half_page(c, page_info):
    if page_info['type'] == 'cover':
        # Draw Cover Page
        title_style.fontSize = 62
        title_style.leading = 60
        cover_page = Paragraph(
            '''Downloads/<br/>Downloads<br/>.pdf''', title_style)
        cover_page.wrapOn(c, config.HALF_WIDTH - 2 *
                          config.MARGIN, config.HALF_HEIGHT - 2 * config.MARGIN)
        cover_page.drawOn(c, config.MARGIN, config.HALF_HEIGHT -
                          (cover_page.height - (2 * config.MARGIN) * 2))
    elif page_info['type'] == 'about':
        # Draw About Page
        about_style = styles["Normal"]
        about_style.fontSize = 12
        about_style.leading = 12 * 1.2
        about_text = f'''This edition examines the Downloads folder of {config.USER_NAME.capitalize()} as of {datetime.now().strftime("%m.%d.%Y")}. It reflects on the quiet buildup of digital clutter and unveils the untold stories hidden in our downloads. Files are randomly selected, with pixelated images ensuring privacy. As part of this ongoing project exploring the overlooked archives of our digital lives, your most recent download is {
            recent_added_file[0]} (added on {recent_added_file[1].strftime("%m.%d.%Y")}), and the earliest download is {oldest_added_file[0]} (added on {oldest_added_file[1].strftime("%m.%d.%Y")}).'''
        about_text = about_text.replace('\n', '<br/>')
        about_page = Paragraph(about_text, about_style)
        about_page.wrapOn(c, config.HALF_WIDTH - 2 *
                          config.MARGIN, config.HALF_HEIGHT - 2 * config.MARGIN)
        about_page.drawOn(c, config.MARGIN, config.HALF_HEIGHT -
                          (about_page.height - (2 * config.MARGIN)))
    elif page_info['type'] == 'content':
        draw_page_content(c, page_info['file_info'], page_info['page_num'])
    else:
        # Empty Page
        pass  # Do nothing for empty pages
