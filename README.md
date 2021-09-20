## Usage

Clone repo:

```powershell
git clone https://github.com/Neelfrost/slideshare-dl.git; cd .\slideshare-dl
```

Install dependencies:

```powershell
pip install -I -r requirements.txt
```

Run script:

```powershell
py .\slideshare-dl.py -h
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
