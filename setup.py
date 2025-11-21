from setuptools import find_packages, setup

setup(
    name="downloads-editions",
    version="0.1.0",
    description="A tool to create a booklet PDF from your Downloads folder.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Alvin Ashiatey",
    author_email="mail@alvinashiatey.com",
    url="https://github.com/alvinashiatey/downloads_editions",
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "reportlab",
    ],
    entry_points={
        "console_scripts": [
            "downloads-editions=app.main:main",
            "downloads-editions-gui=app.gui:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
