import os
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from app import config, image_utils, file_utils
from typing import List, Dict, Any

# Define a type alias for clarity
FileInfo = Dict[str, Any]
PageInfo = Dict[str, Any]


styles = getSampleStyleSheet()
title_style = styles["Normal"]
title_style.paddingLeft = 0

oldest_added_file, recent_added_file = file_utils.analyze_files_by_creation_date(
    config.DOWNLOADS_FOLDER)


def justify_text(c: canvas.Canvas, text: str, x: float, y: float, width: float) -> None:
    """
    Justifies the given text within the specified width on the canvas.

    Args:
        c (canvas.Canvas): The canvas to draw on.
        text (str): The text to justify.
        x (float): The x-coordinate to start drawing the text.
        y (float): The y-coordinate to start drawing the text.
        width (float): The width within which to justify the text.

    Returns:
        None
    """
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


def draw_image(c: canvas.Canvas, file_info: FileInfo) -> None:
    """
    Draws a pixelated image on the canvas if the file is an image.

    This function applies a blend mode, pixelates the image, calculates
    its aspect ratio, and then draws it onto the canvas.

    Args:
        c (Canvas): The ReportLab canvas to draw on.
        file_info (FileInfo): Dictionary containing file details.
            Expected keys: 'path', 'extension'
    """
    # Only process supported image extensions
    image_extensions = ['jpg', 'jpeg', 'png', 'gif', 'bmp']
    if file_info['extension'].lower() not in image_extensions:
        return

    # Set up blend mode if not already defined
    if not hasattr(c._doc, "ExtGState"):
        c._doc.ExtGState = {}
    ext_gs_name = "GS1"
    blend_mode = "multiply"
    gs_dict_code = f"<< /Type /ExtGState /BM /{blend_mode} >>"
    c._doc.ExtGState[ext_gs_name] = gs_dict_code

    # Apply the blend state
    c.saveState()
    c._code.append(f"/{ext_gs_name} gs")

    # Process and pixelate the image
    image_utils.pixelate_image(file_info['path'])
    image = ImageReader(config.TEMP_PIXELATED_PATH)

    # Get original dimensions and compute new dimensions to fit the half-page
    img_width, img_height = image.getSize()
    aspect_ratio = img_width / img_height
    new_width = config.HALF_WIDTH - 2 * config.MARGIN
    new_height = new_width / aspect_ratio

    # Draw the image
    c.drawImage(
        image,
        config.MARGIN,
        config.HALF_HEIGHT - new_height - config.MARGIN,
        width=new_width,
        height=new_height
    )
    c.restoreState()

    # Clean up the temporary pixelated image file
    os.remove(config.TEMP_PIXELATED_PATH)


def draw_title(c: canvas.Canvas, file_info: FileInfo) -> None:
    """
    Draws the title on the canvas.

    The title is extracted from the file's basename and shortened if necessary.

    Args:
        c (Canvas): The ReportLab canvas to draw on.
        file_info (FileInfo): Dictionary containing file details.
            Expected key: 'path'
    """
    # Set title style parameters
    title_style.fontSize = 60
    title_style.leading = 60

    # Extract and shorten the file name for the title
    title = os.path.basename(file_info['path'])
    title = shorten_text(title, config.TITLE_TEXT_LENGTH)

    # Create and draw the title paragraph
    c_text = Paragraph(title, title_style)
    c_text.wrapOn(c, config.HALF_WIDTH - 2 * config.MARGIN,
                  config.HALF_HEIGHT - 2 * config.MARGIN)
    # Adjust vertical position based on the paragraph height and margin
    c_text.drawOn(c, config.MARGIN, config.HALF_HEIGHT -
                  (c_text.height - (2 * config.MARGIN) * 2))


def draw_centered_text(c: canvas.Canvas, file_info: FileInfo) -> None:
    """
    Draws centered text on the canvas containing file metadata.

    The text includes the file's date, extension, and size.

    Args:
        c (Canvas): The ReportLab canvas to draw on.
        file_info (FileInfo): Dictionary containing file details.
            Expected keys: 'date', 'extension', 'size'
    """
    center_text = f'{file_info["date"]} | {
        file_info["extension"]} | {file_info["size"]} bytes'
    justify_text(
        c,
        center_text,
        config.MARGIN,
        config.HALF_HEIGHT / 2,
        config.HALF_WIDTH - 2 * config.MARGIN
    )


def draw_page_number(c: canvas.Canvas, page_num: int) -> None:
    """
    Draws the page number on the canvas.

    Args:
        c (Canvas): The ReportLab canvas to draw on.
        page_num (int): The page number to display.
    """
    c.drawString(
        config.HALF_WIDTH - config.MARGIN,
        config.MARGIN,
        str(page_num),
        direction='LTR'
    )


def draw_page_content(c: canvas.Canvas, file_info: FileInfo, page_num: int) -> None:
    """
    Draws the content of a page, including an image (if applicable),
    the title, centered metadata text, and the page number.

    Args:
        c (Canvas): The ReportLab canvas to draw on.
        file_info (FileInfo): Dictionary containing file details.
        page_num (int): The page number to display.
    """
    # Draw the image if the file is of an image type
    draw_image(c, file_info)

    # Draw the file title
    draw_title(c, file_info)

    # Draw the centered file metadata text
    draw_centered_text(c, file_info)

    # Draw the page number at the bottom-right
    draw_page_number(c, page_num)


def shorten_text(text: str, max_length: int) -> str:
    """
    Shortens the text to a specified maximum length, adding ellipsis if truncated.

    Args:
        text (str): The text to shorten.
        max_length (int): The maximum allowed length of the text.

    Returns:
        str: The shortened text with ellipsis if it exceeds the maximum length.
    """
    return text if len(text) <= max_length else text[:max_length] + '...'


def prepare_file_infos(files: List[str]) -> List[FileInfo]:
    """
    Prepare file information for each file.

    Args:
        files (List[str]): List of file paths.

    Returns:
        List[FileInfo]: A list of dictionaries containing file details.
    """
    file_infos: List[FileInfo] = []
    for f in files:
        file_infos.append({
            'path': f,
            'title': os.path.splitext(os.path.basename(f))[0],
            'date': datetime.fromtimestamp(os.path.getmtime(f)).strftime('%m.%d.%Y'),
            'extension': os.path.splitext(f)[1][1:],
            'size': os.path.getsize(f)
        })
    return file_infos


def build_pages(file_infos: List[FileInfo]) -> List[PageInfo]:
    """
    Build the initial list of pages for the booklet.

    Args:
        file_infos (List[FileInfo]): A list of file information dictionaries.

    Returns:
        List[PageInfo]: A list of page dictionaries.
    """
    pages: List[PageInfo] = []

    # Cover page
    pages.append({'type': 'cover'})

    # Empty page
    pages.append({'type': 'empty'})

    # Content pages for each file info
    for idx, file_info in enumerate(file_infos):
        pages.append({
            'type': 'content',
            'file_info': file_info,
            'page_num': idx + 1
        })

    # Additional empty page and about page
    pages.append({'type': 'empty'})
    pages.append({'type': 'about'})

    return pages


def pad_pages_to_multiple_of_four(pages: List[PageInfo]) -> List[PageInfo]:
    """
    Pads the pages list with empty pages until its total count is a multiple of 4.

    Args:
        pages (List[PageInfo]): The current list of pages.

    Returns:
        List[PageInfo]: The padded list of pages.
    """
    total_pages = len(pages)
    if total_pages % 4 != 0:
        padding_needed = 4 - (total_pages % 4)
        for _ in range(padding_needed):
            pages.append({'type': 'empty'})
    return pages


def rearrange_pages_for_booklet(pages: List[PageInfo]) -> List[PageInfo]:
    """
    Rearranges the pages into booklet order for printing.

    Args:
        pages (List[PageInfo]): The list of pages (must be a multiple of 4).

    Returns:
        List[PageInfo]: A new list with pages in booklet order.
    """
    num_sheets = len(pages) // 4
    booklet_order: List[PageInfo] = []
    for sheet in range(num_sheets):
        # Front side: last page of the sheet and first page of the sheet
        booklet_order.append(pages[-(2 * sheet + 1)])
        booklet_order.append(pages[2 * sheet])
        # Back side: second page of the sheet and second-to-last page of the sheet
        booklet_order.append(pages[2 * sheet + 1])
        booklet_order.append(pages[-(2 * sheet + 2)])
    return booklet_order


def generate_booklet_pdf(booklet_order: List[PageInfo]) -> None:
    """
    Generates the PDF for the booklet using the given page order.

    Args:
        booklet_order (List[PageInfo]): List of pages in booklet order.

    Returns:
        None
    """
    c = canvas.Canvas(config.BOOKLET_PDF_PATH,
                      pagesize=(config.LANDSCAPE_WIDTH, config.LANDSCAPE_HEIGHT))

    # Draw two pages per LANDSCAPE sheet
    for i in range(0, len(booklet_order), 2):
        c.setPageSize((config.LANDSCAPE_WIDTH, config.LANDSCAPE_HEIGHT))

        # Left half
        c.saveState()
        c.translate(0, 0)
        draw_half_page(c, booklet_order[i])
        c.restoreState()

        # Right half
        c.saveState()
        c.translate(config.LANDSCAPE_WIDTH / 2, 0)
        draw_half_page(c, booklet_order[i + 1])
        c.restoreState()

        c.showPage()

    c.save()
    print(f'Booklet PDF generated: {config.BOOKLET_PDF_PATH}')
    file_utils.open_file_in_default_app(config.BOOKLET_PDF_PATH)


def create_booklet_pdf(files: List[str]) -> None:
    """
    Creates a booklet PDF from a list of file paths.

    This function prepares file information, builds page data,
    pads the pages to a multiple of four, rearranges the pages
    for booklet printing, and then generates the PDF.

    Args:
        files (List[str]): List of file paths to include in the booklet.

    Returns:
        None
    """
    # Prepare file info
    file_infos = prepare_file_infos(files)

    # Build and pad pages
    pages = build_pages(file_infos)
    pages = pad_pages_to_multiple_of_four(pages)

    # Rearrange pages for booklet printing
    booklet_order = rearrange_pages_for_booklet(pages)

    # Generate the PDF
    generate_booklet_pdf(booklet_order)


def draw_cover_page(c: canvas.Canvas) -> None:
    """
    Draws the cover page on the given canvas.

    Args:
        c (Canvas): The ReportLab canvas to draw on.
    """
    title_style.fontSize = 62
    title_style.leading = 60

    cover_page = Paragraph(
        '''/Downloads<br/>/Downloads<br/>.pdf''',
        title_style
    )
    cover_page.wrapOn(c, config.HALF_WIDTH - 2 * config.MARGIN,
                      config.HALF_HEIGHT - 2 * config.MARGIN)
    cover_page.drawOn(c, config.MARGIN,
                      config.HALF_HEIGHT - (cover_page.height - (2 * config.MARGIN) * 2))


def draw_about_page(c: canvas.Canvas) -> None:
    """
    Draws the about page on the given canvas.

    Args:
        c (Canvas): The ReportLab canvas to draw on.
    """
    # Create a local style based on the default "Normal" style
    about_style = styles["Normal"]
    about_style.fontSize = 12
    about_style.leading = 12 * 1.2

    about_text = (
        f"This edition examines the Downloads folder of {
            config.USER_NAME.capitalize()} "
        f"as of {datetime.now().strftime('%m.%d.%Y')
                 }. It reflects on the quiet buildup of digital "
        f"clutter and unveils the untold stories hidden in our downloads. Files are randomly selected, "
        f"with pixelated images ensuring privacy. As part of this ongoing project exploring the overlooked "
        f"archives of our digital lives, your most recent download is {
            recent_added_file[0]} "
        f"(added on {recent_added_file[1].strftime(
            '%m.%d.%Y')}), and the earliest download is "
        f"{oldest_added_file[0]} (added on {
            oldest_added_file[1].strftime('%m.%d.%Y')})."
        f"\n"
        f"Developed by Alvin Ashiatey, this Python package is a zine in itself—a space where design intersects with code, and each run brings new life to its content."
    )
    # Replace any newline with <br/> if needed
    about_text = about_text.replace('\n', '<br/>')
    about_page = Paragraph(about_text, about_style)

    about_page.wrapOn(c, config.HALF_WIDTH - 2 * config.MARGIN,
                      config.HALF_HEIGHT - 2 * config.MARGIN)
    about_page.drawOn(c, config.MARGIN,
                      config.HALF_HEIGHT - (about_page.height - (2 * config.MARGIN)))


def draw_content_page(c: canvas.Canvas, file_info: Dict[str, Any], page_num: int) -> None:
    """
    Draws a content page on the canvas using the provided file information.

    Args:
        c (Canvas): The ReportLab canvas to draw on.
        file_info (Dict[str, Any]): Dictionary containing information about the file.
        page_num (int): The page number to be displayed.
    """
    draw_page_content(c, file_info, page_num)


def draw_empty_page(c: canvas.Canvas) -> None:
    """
    Handles drawing an empty page (currently does nothing).

    Args:
        c (Canvas): The ReportLab canvas to draw on.
    """
    # Empty page: no drawing required.
    pass


def draw_half_page(c: canvas.Canvas, page_info: PageInfo) -> None:
    """
    Draws the appropriate content on half a page based on the page type.

    Args:
        c (Canvas): The ReportLab canvas to draw on.
        page_info (PageInfo): Dictionary containing page details.
            Expected keys:
              - 'type': One of 'cover', 'about', 'content', or 'empty'.
              - For 'content', also expects 'file_info' and 'page_num'.
    """
    page_type = page_info.get('type')

    if page_type == 'cover':
        draw_cover_page(c)
    elif page_type == 'about':
        draw_about_page(c)
    elif page_type == 'content':
        draw_content_page(c, page_info['file_info'], page_info['page_num'])
    else:
        draw_empty_page(c)
