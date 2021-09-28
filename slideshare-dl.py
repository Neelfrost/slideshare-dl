import argparse
from concurrent.futures import ThreadPoolExecutor
import glob
import os
import shutil
from sys import exit

from bs4 import BeautifulSoup
import img2pdf
import requests


SLIDES_FOLDER = os.path.join(os.getcwd(), "slides")


def create_parser():  # {{{
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

    # Return args namespace
    return parser.parse_args()  # }}}


def download_slide(idx, image_url, image_path):  # {{{
    # Print slide being downloaded
    print(f"Downloading slide: {idx}", end="\r", flush=True)
    # Download slide, save it in "slides" folder
    return os.system(f"curl.exe -s {image_url} -o {image_path}")  # }}}


def download_slides(url):  # {{{
    # Check if url if of slideshare
    # Exit if not
    if r"www.slideshare.net" not in url:
        exit("Invalid link...")

    # Scrape url for slide images
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    images = soup.find_all("img", class_="slide_image")
    no_of_images = len(images)

    # Make "slides" dir in cwd
    if not os.path.isdir(SLIDES_FOLDER):
        os.mkdir("slides")

    # Use highest slide resolution available
    # Exit if not found
    if images[0].has_attr("data-full"):
        res = "data-full"
    elif images[0].has_attr("data-normal"):
        res = "data-normal"
    else:
        exit("No slides were found...")

    # Parallelize slide downloading
    with ThreadPoolExecutor() as executor:
        for idx, image in enumerate(images, start=1):
            image_url = image.get(res).split("?")[0]
            # Format image name to include slide index (with leading zeros)
            image_name = (
                str(idx).zfill(len(str(no_of_images))) + "-" + image_url.split("/")[-1]
            )
            image_path = os.path.join("slides", image_name)
            if os.path.isfile(image_path):
                print(f"Slide: {idx} exists", end="\r", flush=True)
            else:
                executor.submit(download_slide, idx, image_url, image_path)  # }}}


def convert_to_pdf(pdf_name, no_pdf=False):  # {{{
    # Get all slides sorted by name
    files = glob.glob("slides/*")

    if not no_pdf:
        print("Generating pdf...", end="\r", flush=True)

        # Combine slides to a pdf using img2pdf
        with open(f"{pdf_name}.pdf", "wb") as pdf:
            pdf.write(img2pdf.convert(files))

        print(f"Generated: {pdf_name}.pdf")

        # Remove "slides" folder
        shutil.rmtree(SLIDES_FOLDER)  # }}}


if __name__ == "__main__":
    args = create_parser()
    download_slides(args.url)
    convert_to_pdf(args.url.split("/")[-1], no_pdf=args.nopdf)
