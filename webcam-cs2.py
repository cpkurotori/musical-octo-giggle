"""
Simply display the contents of the webcam with optional mirroring using OpenCV
via the new Pythonic cv2 interface.  Press <esc> to quit.
"""
import os
import io

import cv2
from google.cloud import vision
from google.cloud.vision import types

def show_webcam(mirror=False):
    client = vision.ImageAnnotatorClient()
    cam = cv2.VideoCapture(0)
    while True:
        ret_val, img = cam.read()
        if mirror:
            img2 = cv2.flip(img, 1)
        cv2.imshow('my webcam', img2)
        c = cv2.waitKey(1)
        if  c == 27:
            break  # esc to quit
        if c == 99:
            cv2.imwrite("resources/img.jpg", img)
            # The name of the image file to annotate
            file_name = os.path.join(
                os.path.dirname(__file__),
                'resources/img.jpg')

            # Loads the image into memory
            with io.open(file_name, 'rb') as image_file:
                content = image_file.read()

            image = types.Image(content=content)
            response = client.label_detection(image=image)
            labels = response.label_annotations
            response = client.logo_detection(image=image)
            logos = response.logo_annotations
            print('Logos:')

            for logo in logos:
                print(logo.description)

            print('Labels:')
            for label in labels:
                print(label.description)
            # response = client.image_properties(image=image)
            # props = response.image_properties_annotation
            # print('Properties:')
            # print(props)
            # for color in props.dominant_colors.colors:
            #     print('frac: {}'.format(color.pixel_fraction))
            #     print('\tr: {}'.format(color.color.red))
            #     print('\tg: {}'.format(color.color.green))
            #     print('\tb: {}'.format(color.color.blue))
            #     print('\ta: {}'.format(color.color.alpha))
    cv2.destroyAllWindows()


def main():
    show_webcam(mirror=True)


if __name__ == '__main__':
    main()
