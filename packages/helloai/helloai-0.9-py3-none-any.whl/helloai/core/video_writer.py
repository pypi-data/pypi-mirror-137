import os
import cv2
import uuid
from helloai.core.image import Image 

__all__ = ['VideoWriter']

class VideoWriter:
    def __init__(self, path, capture):
        self.__options = capture.options
        print('options : ', self.__options)

        self.__width = int(self.__options['width'])
        self.__height = int(self.__options['height'])
        self.__fps = self.__options['fps']
        self.__name = str(uuid.uuid4()).split('-')[0]
        
        self.__fcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        self.__out = cv2.VideoWriter(os.path.join(path, f'{self.__name}.mp4'), self.__fcc, self.__fps, (self.__width, self.__height))
        self.__writable = False
        self.__frame_count = 0
        # avi
        # self.__fcc = cv2.VideoWriter_fourcc(*'XVID')
        # self.__out = cv2.VideoWriter(os.path.join(path, f'{name}.avi'), self.__fcc, self.__fps, (self.__width, self.__height))
        # print('recorder name :', os.path.join(path, f'{name}.avi'))
        
        # mp4
        # self.__fcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        # self.__out = cv2.VideoWriter(os.path.join(path, f'{name}.mp4'), self.__fcc, self.__fps, (self.__width, self.__height))
        # print('recorder name :', os.path.join(path, f'{name}.mp4'))

    @property
    def frame_count(self):
        return self.__frame_count

    def write(self, img):
        if not isinstance(img, Image):
            return
        if self.__out:
            self.__frame_count += 1
            self.__out.write(img.frame)

    def release(self):
        if self.__out is not None:
            self.__out.release()
            self.__out = None

    def __del__(self):
        if self.__out is not None:
            self.__out.release()


