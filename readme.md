# OAK D Deploy notes

## First steps
```bash
sudo apt install python3.11-venv
python3 -m venv venv
pip install -r requirements.txt
python3 -m depthai_viewer
```

## Making device available
```bash
# Create this new udev rule
sudo nano /etc/udev/rules.d/80-luxonis.rules
# Paste this code on it
SUBSYSTEM=="usb", ATTR{idVendor}=="03e7", MODE="0666"

# Reload udev rules
sudo udevadm control --reload-rules
sudo udevadm trigger
# Then reconect the camera and try
# python3 -m depthai_viewer
# The camera should be listed
```