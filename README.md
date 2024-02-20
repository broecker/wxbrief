# wxbrief
A small tool to download and print NOAA's uppair air analysis maps

## Installation
python3 -m pip install -r requirements.txt

## Usage
Sample invocation:

python3 wxbrief.py --print /usr/bin/lpr --levels 300,500,850

## Printing
The script calls the print command using `subprocess.run`. For example, on Linux
you can pass in `/usr/bin/lpr` or `/user/bin/lp` to print using CUPS and the
default settings on the default printer.

Each map/pdf is printed on its own, single-sided. This makes annotating easier.


## Raspberry PI installation

The interesting application of this small script comes when run daily. For
example, I'm running this script on my Raspberry Pi. Systemd timers are used to
trigger this script every morning.

### Install

```
# Clone the github repo into a new folder in /opt: 
sudo mkdir /opt/wxbrief
sudo chmod 777 /opt/wxbrief
cd /opt/wxbrief
git clone https://github.com/broecker/wxbrief.git .
python3 -m pip install -r requirements.txt 
```

### Raspberry Pi and CUPS Setup

See the
[official Raspberry Pi article](https://www.raspberrypi.com/news/printing-at-home-from-your-raspberry-pi/)
and the [CUPS documentation](https://www.cups.org/documentation.html) on how to
set up printing on a Raspi.

```
sudo apt-get install cups

# Show all printers
lpstat -p -d

# Set the default printer, if not already set:
lpoptions -d <PRINTER_NAME>

# Get a sample upper-air analysis and print it to test the connection.
wget https://www.spc.noaa.gov/obswx/maps/sfc_12.pdf
lp sfc_12.pdf
```

### Setting up a Systemd service

Edit the wxbrief.timer file and make sure that the running timer is set to a
correct time; i.e. the --zulu flag should be /before/ your time when the script
is running.

```
# Install timer and service.
sudo cp -r wxbrief.service wxbrief.timer /etc/systemd/system
sudo systemctl enable wxbrief.timer
sudo systemctl enable wxbrief.service
sudo systemctl start wxbrief.timer

# Check that a new timer invocation is scheduled:
systemctl status wxbrief.timer
```

