import argparse
import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from sys import exit

import img2pdf
import requests
from bs4 import BeautifulSoup

SLIDES_FOLDER = os.path.join(os.getcwd(), "slides")


def create_parser():
    """Create CLI parser using argparse

    Returns:
            args namespace
    """

    # Init parser
    parser = argparse.ArgumentParser(
        description="Download a slideshare presentation.",
    )

    # Add args
    parser.add_argument(
        "url",
        type=str,
        help="Slideshare presentation url.",
    )
    parser.add_argument(
        "--nopdf",
        default=False,
        help='Do not combine slides into a pdf. (Individual slides are saved in "slides" folder)',
        action="store_true",
    )

    return parser.parse_args()


def download_slide(idx, image_url, image_path):
    """Use requests module to download a slide (image)

    Args:
        idx (string): index of slide
        image_url (string): url of slide
        image_path (string): save path of slide
    """

    # Print slide being downloaded
    print("\x1b[1K\r" + f"Downloading slide: {idx}", end="")
    # Download slide, save it in "slides" folder
    with open(image_path, "wb") as image:
        image.write(requests.get(image_url).content)


def download_presentation(url):
    """Download a slideshare presentation

    Args:
        url (string): url of slideshare presentation
    """

    # Exit if url does not belong to slideshare
    if r"www.slideshare.net" not in url:
        exit("Invalid link...")

    # Scrape url for slide images
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    images = soup.find_all("img", class_="slide-image")
    no_of_images = len(images)

    # Exit if presentation not found
    if not images:
        exit("No slides were found...")
    print(f"Number of slides to be downloaded: {len(images)}")

    # Make "slides" dir in cwd
    if not os.path.isdir(SLIDES_FOLDER):
        os.mkdir("slides")

    # Parallelize slide downloading
    with ThreadPoolExecutor() as executor:
        for idx, image in enumerate(images, start=1):
            # Get image url from srcset attribute (csv of image urls, with last value being the highest res)
            image_url = image.get("srcset").split(",")[-1].split("?")[0]

            # Format image name to include slide index (with leading zeros)
            image_name = (
                f"{str(idx).zfill(len(str(no_of_images)))}-{image_url.split('/')[-1]}"
            )
            # Save path of image (cwd/slides/image_name)
            image_path = os.path.join("slides", image_name)

            # Check if slide is already downloaded
            if os.path.isfile(image_path):
                print("\x1b[1K\r" + f"Slide: {idx} exists", end="")
            else:
                executor.submit(download_slide, idx, image_url, image_path)

    # "\x1b[1K" clear to end of line
    print("\x1b[1K\r" + "Slides downloaded")


def convert_to_pdf(pdf_name, no_pdf=False):
    """Combine set of images within 'slides' folder into a pdf using img2pdf

    Args:
        pdf_name (string): name of the final pdf
        no_pdf (bool): True to generate a pdf, False to skip generation
    """

    if no_pdf:
        return

    # Get all slides sorted by name
    slides = [os.path.join(SLIDES_FOLDER, slide) for slide in os.listdir(SLIDES_FOLDER)]

    print("\x1b[1K\r" + "Generating pdf...", end="")

    # Combine slides into a pdf using img2pdf
    with open(f"{pdf_name}.pdf", "wb") as pdf:
        pdf.write(img2pdf.convert(slides))

    print("\x1b[1K\r" + f"Generated: {pdf_name}.pdf")

    # Remove "slides" folder
    shutil.rmtree(SLIDES_FOLDER)


if __name__ == "__main__":
    args = create_parser()
    download_presentation(args.url)
    convert_to_pdf(args.url.split("/")[-1], no_pdf=args.nopdf)
