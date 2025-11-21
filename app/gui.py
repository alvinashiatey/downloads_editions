import sys
import threading
import tkinter as tk
import tkinter.font as tkfont

from app import config, file_utils, pdf_utils


class HyperlinkButton(tk.Label):
    """Label behaving like a hyperlink with hover/disabled states."""

    def __init__(self, master, text, command, font=("Arial", 20, "underline"),
                 normal_color="#1f6fe7", hover_color="#1859b9", disabled_color="#8aa6d6"):
        super().__init__(
            master,
            text=text,
            fg=normal_color,
            bg=master["bg"],
            cursor="hand2",
            font=font,
            anchor="w",
            padx=0,
            pady=0
        )
        self.command = command
        self.normal_color = normal_color
        self.hover_color = hover_color
        self.disabled_color = disabled_color
        self.state = "normal"
        self.display_text = text
        self.hover_text = "/Generate PDF"

        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", lambda e: self._on_hover(True))
        self.bind("<Leave>", lambda e: self._on_hover(False))

    def _on_click(self, _event):
        if self.state == "normal" and self.command:
            self.command()

    def _on_hover(self, entering):
        if self.state != "normal":
            return
        text = self.hover_text if entering else self.display_text
        color = self.hover_color if entering else self.normal_color
        self.config(text=text, fg=color)

    def set_state(self, state: str):
        self.state = state
        if state == "disabled":
            self.config(fg=self.disabled_color, cursor="")
        else:
            self.config(fg=self.normal_color, cursor="hand2")

    def set_text(self, text: str):
        self.display_text = text
        self.config(text=text)


class DownloadsEditionsGUI:
    """GUI application for generating Downloads Editions PDF booklets."""

    def __init__(self, root):
        self.root = root
        self.bkCG = "#fefefe"
        self.root.title("Downloads Publication")
        self.button_width = 425
        self.button_height = 200
        self.body_font = ("Arial", 12)
        self.bold_email_font = tkfont.Font(
            family="Arial", size=12, weight="bold")
        self.email = "mail@alvinashiatey.com"
        padding = 30
        info_section_height = 160
        window_width = self.button_width + padding * 2
        window_height = self.button_height + padding * 2 + info_section_height
        self.root.geometry(f"{window_width}x{window_height}")
        self.root.resizable(False, False)
        # Hide title bar/borders for a floating feel
        self.root.overrideredirect(True)
        self.root.configure(bg=self.bkCG)
        try:
            # Make the black background transparent where supported (Windows Linux Tk 8.6+)
            self.root.wm_attributes("-transparentcolor", self.bkCG)
        except Exception:
            pass

        # Variables
        self.is_generating = False
        self.status_var = tk.StringVar(
            value="Developed by Alvin Ashiatey, this project aims to capture snapshots of our Download folders, the directory where the internet meets the local machine. I originally created this tool to reflect on my own digital consumption habits over time, but I soon realized it could be interesting to share with others. Together, we might create a larger snapshot of internet culture as seen through our Download folders.\nIf you are reading this, you found the tool interesting enough to try. Feel free to share the generated PDF with me at mail@alvinashiatey.com."
        )

        # Setup UI
        self.setup_ui()

    def setup_ui(self):
        """Create and layout all UI elements."""
        main_frame = tk.Frame(self.root, bg=self.bkCG)
        main_frame.pack(fill="both", expand=True)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.columnconfigure(0, weight=1)

        # Button section (top half) with padding
        button_frame = tk.Frame(main_frame, bg=self.bkCG)
        button_frame.grid(row=0, column=0, sticky="nsew", pady=(30, 30))
        button_frame.grid_propagate(False)

        self.generate_btn = HyperlinkButton(
            button_frame,
            text="/Download PDF",
            command=self.generate_pdf,
            font=("Arial", 28, "underline"),
            normal_color="#1f6fe7",
            hover_color="#1859b9",
            disabled_color="#8aa6d6"
        )
        self.generate_btn.pack(anchor="w", padx=30, pady=(0, 10))

        # Info/status section (bottom half)
        info_frame = tk.Frame(main_frame, bg=self.bkCG)
        info_frame.grid(row=1, column=0, sticky="nsew")
        info_frame.grid_propagate(False)

        info_label = tk.Label(
            info_frame,
            textvariable=self.status_var,
            bg=self.bkCG,
            fg="#181818",
            font=("Arial", 12),
            justify="left",
            anchor="w",
            wraplength=self.button_width
        )
        info_label.pack(expand=True, fill="both", padx=30,
                        pady=(10, 30), anchor="w")

    def generate_pdf(self):
        """Generate PDF in a separate thread to prevent UI freezing."""
        if self.is_generating:
            return

        # Start generation in separate thread
        self.is_generating = True
        self.generate_btn.set_state('disabled')
        self.generate_btn.set_text("Generating...")
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
        self.generate_btn.set_state('normal')
        self.generate_btn.set_text("/Download PDF")
        self.status_var.set(
            f"PDF created at:\n{config.BOOKLET_PDF_PATH}\n\nDeveloped by Alvin Ashiatey, this project aims to capture snapshots of our Download folders, the directory where the internet meets the local machine. I originally created this tool to reflect on my own digital consumption habits over time, but I soon realized it could be interesting to share with others. Together, we might create a larger snapshot of internet culture as seen through our Download folders.\nIf you are reading this, you found the tool interesting enough to try. Feel free to share the generated PDF with me at mail@alvinashiatey.com."
        )

    def _generation_error(self, error_msg):
        """Called when PDF generation fails (runs in main thread)."""
        self.is_generating = False
        self.generate_btn.set_state('normal')
        self.generate_btn.set_text("/Download PDF")
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
