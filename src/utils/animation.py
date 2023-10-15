from typing import List


class Animation:
    def __init__(self, images: List, image_duration: float, loop: bool = True) -> None:
        self.images = images
        self.image_duration = image_duration
        self.loop = loop
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(images=self.images, image_duration=self.image_duration, loop=self.loop)

    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.image_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.image_duration * len(self.images) - 1)
            if self.frame >= self.image_duration * len(self.images) - 1:
                self.done = True

    def get_current_image(self):
        return self.images[int(self.frame / self.image_duration)]
