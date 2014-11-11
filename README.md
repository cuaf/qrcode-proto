# Prototype for live QR code recognition

Eventually we'll use the position of the QR code as error data for a control system that tries to centre the camera on the QR code.

## Install

On **OS X**, you should use [Homebrew](http://brew.sh). Do the following:

    $ brew tap homebrew/science
    $ brew install opencv
    $ brew install zbar

On **Ubuntu**, something similar such as `$ sudo apt-get install opencv zbar`
will probably work.

Run `$ python -c "import cv2" && echo "It works!"` to make sure it worked.

Install Python libraries:

    $ pip install pillow
    $ pip install git+https://github.com/npinchot/zbar
    
