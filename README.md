Camera
======

Prototype code for live QR code recognition.

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
    

## Camera

Here are the things we'd like the camera to do:

### Raw Capture

capture raw video, discard all but latest frame.

- What would be a zbar-friendly format? Have a look at <https://github.com/ZBar/ZBar/blob/854a5d97059e395807091ac4d80c53f7968abb8f/zbar/convert.c> and <https://github.com/mattvenn/qr-music-player/blob/master/picam_qr.py>.

    => Gabi worked out ZBar will only scan grayscale images ("Y800"). We can get grayscale using the Y channel of the Pi's raw YUV image.

- shared memory? This would be nice for zero-copying things between processes, so different things can do stuff with the camera stream. This looks useful: <http://stackoverflow.com/questions/5549190/is-shared-readonly-data-copied-to-different-processes-for-python-multiprocessing/5550156#5550156>

Have to use `use_video_port=True` so the field of view doesn't change while
grabbing frames.

### Still capture

periodically capture still images to jpeg

For aerial photography.

- consistency might be important? <http://picamera.readthedocs.org/en/release-1.8/recipes1.html#capturing-consistent-images>

### Live stream

capture h.264 video, resized to be smaller (eg. using `resize=(1024, 768)`)

For streaming live video over wifi.

- How can we stream this using UDP?

    python gstreamer-rtsp?

    `raspivid -t 0 -h 480 -w 640 -fps 25 -hf -b 1000000 -o - | gst-launch-1.0 -v fdsrc ! h264parse ! rtph264pay config-interval=1 pt=96 ! udpsink host=127.0.0.1 port=1234`

    <http://www.jonobacon.org/2006/08/28/getting-started-with-gstreamer-with-python/>


    <http://stackoverflow.com/questions/7669240/webcam-streaming-using-gstreamer-over-udp>

