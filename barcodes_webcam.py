from io import BytesIO
import signal
import sys
import threading
import time

import cv2
import IPython.display
import numpy
import PIL.Image
import PIL.ImageDraw
import PIL.ImageFont
import zbar



def numpy2pil(image_array):
    try:
        # Convert BGR to RGB
        rgb_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2RGB)
    except:
        # Uh... maybe it was grayscale?
        rgb_array = cv2.cvtColor(image_array, cv2.COLOR_GRAY2RGB)

    # Convert to PIL image
    return PIL.Image.fromarray(rgb_array)

def pil2numpy(pil_image):
    pil_image = pil_image.convert("RGB")
    rgb_array = numpy.array(pil_image)
    return cv2.cvtColor(rgb_array, cv2.COLOR_RGB2BGR)



# zbar
scanner = zbar.ImageScanner()
scanner.parse_config('enable')

latest_frame = None
latest_output = None

font = PIL.ImageFont.truetype("Arial Black.ttf", 16)


class Recogniser(threading.Thread):
    running = True

    DISAPPEAR = 0.1

    def run(self):
        global latest_output
        latest_output_time = 0
        while self.running:
            time.sleep(0.05)

            if time.time() - latest_output_time > self.DISAPPEAR:
                latest_output = None

            if not latest_frame:
                continue

            pil_image = latest_frame.copy()
            width, height = pil_image.size

            gray = pil_image.convert('L')
            raw_image = gray.tostring()
            zbar_image = zbar.Image(width, height, 'Y800', raw_image)
            results = scanner.scan(zbar_image)
            if not results:
                continue

            foo = PIL.Image.new("RGBA", pil_image.size, (0,0,0,0))
            draw = PIL.ImageDraw.Draw(foo)
            draw.setink((255, 0, 0, 255))
            for symbol in zbar_image:
                # So we get some numbers out, not really sure what they are.
                # Might as well draw some lines and see what happens.
                # I think the longest line should be our "best" match...
                # but why can't it give us a bounding box or something! Nuts.
                print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data

                pairs = len(symbol.location)
                pointNumber = 0
                for x in range(pairs):
                    pointNumber+=1
                    print x
                    draw.text(symbol.location[x],str(pointNumber),(255,255,255),font=font)
                    draw.line([symbol.location[x], symbol.location[x-1]])

            latest_output = foo
            latest_output_time = time.time()

        print "Stopped"

    def stop(self):
        self.running = False
        self.join()


r = Recogniser()
r.daemon = True
r.start()

def cleanup():
    cv2.destroyWindow("preview")
    r.stop()

def sigint_handler(signal, frame):
    signal.pause()
    cleanup()
    sys.exit(0)

window = cv2.namedWindow("preview")
video = cv2.VideoCapture(0)
if video.isOpened():
    while True:
        rval, frame = video.read()
        if not rval:
            break

        pil_image = numpy2pil(frame)
        latest_frame = pil_image.copy()
        if latest_output:
            pil_image.paste(latest_output, mask=latest_output.split()[3])
        display = pil2numpy(pil_image)

        display = cv2.flip(display, 1)
        cv2.imshow("preview", display)

        key = cv2.waitKey(2)
        if key == 27: # exit on ESC
            break

cleanup()

