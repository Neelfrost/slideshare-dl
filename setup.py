from setuptools import setup


def read_contents(fname):
    with open(fname, encoding="utf-8") as f:
        return f.read()


setup(
    name="slideshare-dl",
    version="1.0",
    description="A simple, multi-threaded, CLI slideshare presentation downloader.",
    author="Neel Basak",
    author_email="neelfrost@gmail.com",
    license=read_contents("LICENSE"),
    packages=["slideshare_dl"],
    install_requires=read_contents("requirements.txt").splitlines(),
    entry_points={"console_scripts": ["slideshare-dl = slideshare_dl.__main__:main"]},
    classifiers=[
        "Environment :: Console",
        "License :: MIT",
        "Operating System :: OS Independent",
    ],
)
