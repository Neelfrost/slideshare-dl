<p align="center">
    <img src="https://raw.githubusercontent.com/Neelfrost/github-assets/main/slideshare/logo.png" alt="slideshare-dl logo" width="192">
</p>

<h1 align="center">slideshare-dl</h1>

<p align="center">
  <b>A simple, multi-threaded, CLI slideshare presentation downloader 🚀</b>
  <br>
  <b>No login required!</b>
</p>

<img src="https://raw.githubusercontent.com/Neelfrost/github-assets/main/slideshare/demo.gif" width="100%">

## Installation

Clone repo:

```powershell
git clone https://github.com/Neelfrost/slideshare-dl.git; cd .\slideshare-dl
```

Install using pip:

```powershell
pip install .
```

## Usage

```powershell
slideshare-dl.exe --help
```

```powershell
usage: slideshare-dl.py [-h] [--nopdf] url

Download a slideshare presentation.

positional arguments:
  url         Slideshare presentation url.

optional arguments:
  -h, --help  show this help message and exit
  --nopdf     Do not combine slides into a pdf. (Individual slides are saved in "slides" folder)
```

## Todo

-   [x] Speed up download using multi-threading
-   [ ] Implement OCR
