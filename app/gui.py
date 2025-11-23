import sys
import threading
import tkinter as tk
from tkinter import ttk

from app import config, file_utils, pdf_utils


class DownloadsEditionsGUI:
    """GUI application for generating Downloads Editions PDF booklets."""

    ABOUT_TEXT = (
        "Developed by Alvin Ashiatey, this project aims to capture snapshots of our Download folders, "
        "the directory where the internet meets the local machine. I originally created this tool to "
        "reflect on my own digital consumption habits over time, but I soon realized it could be "
        "interesting to share with others. Together, we might create a larger snapshot of internet "
        "culture as seen through our Download folders.\n\n"
        "If you are reading this, you found the tool interesting enough to try. Feel free to share "
        "the generated PDF with me at mail@alvinashiatey.com."
    )

    def __init__(self, root):
        self.root = root
        self.root.title("Downloads Publication")
        self.button_width = 425
        self.button_height = 200
        self.padding = 30
        info_section_height = 160
        window_width = self.button_width + self.padding * 2
        window_height = self.button_height + self.padding * 2 + info_section_height
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(False, False)

        # Variables
        self.is_generating = False
        self.status_var = tk.StringVar(value=self.ABOUT_TEXT)

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Create and layout all UI elements."""
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Button section (top half) with padding
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=0, column=0, sticky="nsew",
                          pady=(self.padding, self.padding // 2))
        button_frame.grid_propagate(False)

        self.generate_btn = ttk.Button(
            button_frame,
            text="Generate PDF",
            command=self.generate_pdf,
            takefocus=False
        )
        self.generate_btn.pack(expand=True)

        # Separator
        separator = ttk.Separator(main_frame, orient='horizontal')
        separator.grid(row=1, column=0, sticky="ew", padx=self.padding)

        # Info/status section (bottom half)
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=2, column=0, sticky="nsew")
        info_frame.grid_propagate(False)

        info_label = ttk.Label(
            info_frame,
            textvariable=self.status_var,
            font=("Arial", 10),
            justify="left",
            anchor="w",
            wraplength=self.button_width
        )
        info_label.pack(expand=True, fill="both", padx=self.padding,
                        pady=(self.padding // 2, self.padding), anchor="w")

    def generate_pdf(self):
        """Generate PDF in a separate thread to prevent UI freezing."""
        if self.is_generating:
            return

        # Start generation in separate thread
        self.is_generating = True
        self.generate_btn.config(state='disabled', text="Generating...")
        self.status_var.set(
            "Generating your PDF...\n"
        )

        thread = threading.Thread(
            target=self._generate_pdf_thread, daemon=True)
        thread.start()

    def _generate_pdf_thread(self):
        """Worker thread for PDF generation."""
        try:
            # Use default settings
            folder = config.DOWNLOADS_FOLDER
            num_files = config.NUMBER_OF_FILES

            # Get sample files
            files = file_utils.get_sample_files(folder, num_files)

            if not files:
                self.root.after(0, self._generation_error,
                                "No files found in the Downloads folder")
                return

            # Create PDF
            pdf_utils.create_booklet_pdf(files)

            # Success
            self.root.after(0, self._generation_complete)

        except Exception as e:
            error_msg = str(e)
            self.root.after(0, self._generation_error, error_msg)

    def _generation_complete(self):
        """Called when PDF generation is complete (runs in main thread)."""
        self.is_generating = False
        self.generate_btn.config(state='normal', text="Generate PDF")
        self.status_var.set(
            f"{self.ABOUT_TEXT}"
        )

    def _generation_error(self, error_msg):
        """Called when PDF generation fails (runs in main thread)."""
        self.is_generating = False
        self.generate_btn.config(state='normal', text="Generate PDF")
        self.status_var.set(
            f"Failed to generate PDF:\n{error_msg}"
        )


def main():
    """Entry point for GUI application."""
    root = tk.Tk()

    # Set application icon if available (optional)
    try:
        if sys.platform == 'darwin':  # macOS
            root.createcommand('tk::mac::Quit', root.quit)
    except Exception:
        pass

    # Create and run app
    DownloadsEditionsGUI(root)
    root.mainloop()


if __name__ == '__main__':
    main()
