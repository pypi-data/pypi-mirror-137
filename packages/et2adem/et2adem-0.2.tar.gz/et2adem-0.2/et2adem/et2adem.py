from tqdm import tqdm
from playsound import playsound
import threading
import os

_ROOT = os.path.abspath(os.path.dirname(__file__))
class et2adem(tqdm):
    def __init__(self, loop_data, sound=True):
        self.sound = sound
        tqdm.__init__(self, loop_data,
                      bar_format='{l_bar}{bar}{r_bar}',
                      ascii='\U0001f4a8\U0001f3c3',
                      ncols=50)

    def __iter__(self):
        if self.sound:
            stop_threads = False
            threading.Thread(target=self.play_song, args=(lambda: stop_threads,), daemon=True).start()
        yield from super().__iter__()
        stop_threads = True
        return

    @staticmethod
    def play_song(stop):
        path = 'et2dm.wav'
        while True:
            playsound(os.path.join(_ROOT, 'data', path))
            if stop():
                break