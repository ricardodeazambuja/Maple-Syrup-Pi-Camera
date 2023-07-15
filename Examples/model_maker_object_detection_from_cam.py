import io
import time
import argparse
import numpy as np
from picamera import PiCamera


from PIL import Image
from PIL import ImageDraw

from pycoral.adapters import common
from pycoral.adapters import detect
from pycoral.utils.dataset import read_label_file
from pycoral.utils.edgetpu import make_interpreter


colors = {0: (128, 255, 102), 1: (102, 255, 255)}

    
def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-m', '--model', required=True,
                        help='File path of .tflite file.')
    parser.add_argument('-l', '--labels',
                        help='File path of labels file.')
    parser.add_argument('-t', '--threshold', type=float, default=0.0,
                        help='Classification score threshold')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='Saves the last image to last_image_obj_detec_from_cam.jpg')
    args = parser.parse_args()

    print(f"Initializing EdgeTPU... {args.model} and {args.labels}")
    labels = read_label_file(args.labels) if args.labels else {}
    interpreter = make_interpreter(*args.model.split('@'))
    interpreter.allocate_tensors()
    size = common.input_size(interpreter)
    interpreter.invoke()  # warmup
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()
    print(f"Model input details:\n{input_details}")
    print(f"Model output details:\n{output_details}")

    
    def process_img(image):
        interpreter.set_tensor(input_details[0]['index'], image)
        interpreter.invoke()
        scores = interpreter.get_tensor(output_details[0]['index'])[0]
        boxes = interpreter.get_tensor(output_details[1]['index'])[0]
        num_detections = interpreter.get_tensor(output_details[2]['index'])[0]
        classes = interpreter.get_tensor(output_details[3]['index'])[0]

        return boxes, classes, scores, num_detections

    print("Initializing picamera...")
    # See https://picamera.readthedocs.io/en/release-1.13/api_camera.html
    # for details about the parameters:

    print("Starting...")
    # Start the video process
    stream = io.BytesIO()    
    time.sleep(2)
    try:
        with PiCamera() as camera:
            camera.resolution = (320, 320)
            camera.framerate = 60
            # camera.contrast = contrast
            camera.video_stabilization = True
            camera.video_denoise = True
            #camera.rotation = 180

            start = time.perf_counter()
            for _ in camera.capture_continuous(stream, format='rgb'):
                print(f'Running at {(1/(time.perf_counter() - start)):.2f} fps')
                start = time.perf_counter()
                stream.truncate()
                stream.seek(0)
                image = Image.fromarray(np.frombuffer(stream.getvalue(), dtype=np.uint8).reshape((320,320,3))).convert('RGB').resize(size, Image.ANTIALIAS)
                if image:
                    np_image = np.asarray(image)
                    input_tensor = np.expand_dims(np_image, axis=0)
                    boxes, classes, scores, num_detections = process_img(input_tensor)
                    for i in range(int(num_detections)):
                        if scores[i] >= args.threshold:
                            ymin = int(max(1, (boxes[i][0] * size[1])))
                            xmin = int(max(1, (boxes[i][1] * size[0])))
                            ymax = int(min(size[1], (boxes[i][2] * size[1])))
                            xmax = int(min(size[0], (boxes[i][3] * size[0])))
                    # for obji,obj in enumerate(objs):
                            print(f"Obj #{i} (Confidence {int(100*scores[i])}%): {labels.get(int(classes[i]))} - {(xmin,ymin),(xmax,ymax)}\n")
    except KeyboardInterrupt:
        pass
    finally:
        if args.debug and image:
            dimage = ImageDraw.Draw(image)
            if len(boxes):
                for i in range(int(num_detections)):
                    if scores[i] >= args.threshold:
                        ymin = int(max(1, (boxes[i][0] * size[1])))
                        xmin = int(max(1, (boxes[i][1] * size[0])))
                        ymax = int(min(size[1], (boxes[i][2] * size[1])))
                        xmax = int(min(size[0], (boxes[i][3] * size[0])))
                        dimage.rectangle((xmin, ymin, xmax, ymax), width=7,
                                        outline=colors[int(classes[i])])
                        dimage.rectangle((xmin, ymin, xmax, ymin-10),
                                        fill=colors[int(classes[i])])
                        try:
                            label = labels[int(classes[i])]
                        except KeyError:
                            label = "None"
                        text = label + ' ' + str(scores[i]*100) + '%'
                        dimage.text((xmin+2, ymin-10), text, fill=(0, 0, 0), width=5)

            image.save("last_image_obj_detec_from_cam.jpg")
            print("last_image_obj_detec_from_cam.jpg saved!")
        
        print("Done!")

if __name__ == '__main__':
    main()
