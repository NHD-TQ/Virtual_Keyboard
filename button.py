import cv2

class Button:
    def __init__(self, pos, text, size = [80, 80]):
        self.pos = pos
        self.text = text
        self.size = size