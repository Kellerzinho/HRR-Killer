from time import sleep, time
import os
import cv2 as cv
from estado import Estado
from hardware import Hardware
import constantes as c

from abc import ABC, abstractmethod
from constantes import WIDTH, HEIGHT, FRAMERATE, WARMUP_TIME, CONTRAST


class Camera(Hardware, ABC):
    '''
    Classe abstrata que envolve operações a nível hardware da câmera como a captura de imagens.
    '''
    CONTRAST = CONTRAST
    WIDTH, HEIGHT = WIDTH, HEIGHT
    FRAMERATE = FRAMERATE
    WARMUP_TIME = WARMUP_TIME

    @abstractmethod
    def take_photo(self, name: str | None):
        pass

    @abstractmethod
    def stop(self):
        pass


class RaspCamera(Camera):
    '''
    Implementação da classe Camera que utiliza a câmera do Raspberry Pi para capturar imagens.
    '''

    def __init__(self, dir: str = "images"):
        import picamera2 as picamera
        self.counter = 0
        self.path = os.path.join(os.getcwd(), dir)
        self.cam = picamera.PiCamera(resolution=(
            c.WIDTH, c.HEIGHT), framerate=c.FRAMERATE, contrast=c.CONTRAST)
        sleep(c.WARMUP_TIME)

    def take_photo(self, name: str | None = None):
        """
        Tira uma foto e salva no diretório "images"
        """
        if name is None:
            name = "image" + str(self.counter) + ".jpg"
            self.counter += 1

        path = os.path.join(self.path, name)
        try:
            self.cam.capture(path)
            return path
        except KeyboardInterrupt:
            self.cam.stop_preview()

    def next_state(self):
        pass


# import numpy as np

# import sys

# #sys.path.append('./hrr/data/images/fotos/')

# class RaspCamera(__Camera):
#     def __init__(self):
#         # print("Entra no _init_ da Classe_camera")
#         cam = picamera.PiCamera(resolution=(
#             c.WIDTH, c.HEIGHT), framerate=c.FRAMERATE, contrast=c.CONTRAST)
#         self.cam = cam
#         sleep(c.WARMUP_TIME)

#     def capture(self):
#         return self.capture_opencv()

#     def capture_opencv(self):
#         image = np.empty((c.HEIGHT * c.WIDTH * 3,), dtype=np.uint8)
#         self.cam.capture(image, 'bgr')
#         image = image.reshape((c.HEIGHT, c.WIDTH, 3))
#         return image

#     def capture_sequence(self, frames):
# #        cam.start_preview()
#         # Give the camera some warm-up time
#  #       time.sleep(2)
#         start = time()
#         self.cam.capture_sequence([
#             '../data/images/sequence/image%02d.jpg' % i
#             for i in range(frames)
#             ], use_video_port=True)
#         finish = time()
#         print('Captured %d frames at %.2ffps' % (
#         frames,
#         frames / (finish - start)))
