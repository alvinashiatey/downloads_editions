# setup.py
from setuptools import setup, find_packages

setup(
    name="downloads-editions",
    version="0.1.0",
    description="A tool to create a booklet PDF from your Downloads folder.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/alvinashiatey/downloads_editions",
    packages=find_packages(),           # Automatically discover your packages.
    install_requires=[
        "Pillow",
        "reportlab",
        # Add any other runtime dependencies here.
    ],
    entry_points={
        "console_scripts": [
            "downloads-editions=app.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license.
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
