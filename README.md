MangaLoader - A free manga downloader
=====================================

DESCRIPTION
-----------
MangaLoader retrives mangas from free online manga reading site (e.g. MangaReader.net)


LICENSE
-------
MangaLoader is released under the GNU General Public License v2 or newer


USAGE
-----

Usage from command line:
```
  ./MangaLoader.py [options]
```

Options:
```
  -h, --help         show this help message and exit
  --version          show version information
  -m, --MangaReader  use MangaReader module
  -z                 create cbz files
  -n NAME            name of the manga
  -r FROM TO         load a range of chapters
  -i CHAPTER IMAGE   load a single image (chapterNo, imageNo)
  -o DEST_DIR        destination directory
```

Usage for GUI:
```
  ./MangaLoaderGUI.py
```

REQUIREMENTS
------------
MangaLoader requires at least Python 3.3. Further Python dependencies are
listed in the requirements file.

Before installing the Python library dryscrape, install its dependencies:

    apt-get install qt5-default libqt5webkit5-dev build-essential python-lxml python-pip xvfb
