# wxbrief
A small tool to download and print NOAA's uppair air analysis maps

## Installation
python3 -m pip install -r requirements.txt

## Usage
Sample invocation:

python3 wxbrief.py --print /usr/bin/lpr --levels 300,500,850

## Printing
The script calls the print command using `subprocess.run`. For example, on Linux
you can pass in /usr/bin/lpr to print using CUPS and the default settings on the
default printer.

Each map/pdf is printed on its own, single-sided. This makes annotating easier.

