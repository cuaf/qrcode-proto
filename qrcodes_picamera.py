import io
import numpy
import PIL.Image
import picamera
import picamera.array
import time
import zbar

# init zbar, enable qrcodes only
scanner = zbar.ImageScanner()
scanner.parse_config('enable')
# scanner.set_config(zbar.Symbol.NONE, zbar.Config.ENABLE, 0)
# scanner.set_config(zbar.Symbol.QRCODE, zbar.Config.ENABLE, 1)

# width, height = 2592, 1944

size = width, height = 640, 480

with picamera.PiCamera() as camera:
    #with picamera.array.PiYUVArray(camera, size=size) as stream:
    camera.resolution = width, height

    camera.start_preview()
    time.sleep(2)
    while True:
        stream = io.BytesIO()
        print 'capture'
        camera.capture(stream, 'yuv', use_video_port=True)
        print 'reading'
        stream.seek(0)
        fwidth = (width + 31) // 32 * 32
        fheight = (height + 15) // 16 * 16;

        Y = numpy.frombuffer(stream.getvalue(), dtype=numpy.uint8,
                count=fwidth*fheight).reshape((fheight, fwidth))

        # foo = stream.array.tostring()[:width * height]

        # print 'stream.array.shape', stream.array.shape
        print 'making zbar image'
        #print len(stream.array.tostring())
        zbar_image = zbar.Image(width, height, 'Y800', Y.tostring())
        #
        #pil_image = PIL.Image.fromstring("L", size, foo)
        #pil_image.save("capture.jpg")

        #zbar_image = zbar.Image(width, height, 'I420', stream)
        # zbar_image = zbar.Image(width, height, 'Y800', stream.array.tostring())

        print 'scanning'
        results = scanner.scan(zbar_image)

        print 'decoding results'
        if results:
            for symbol in zbar_image:
               print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
        #time.sleep(4)

