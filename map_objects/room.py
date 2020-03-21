class Room:
    def __init__(self, rect):
        self.x1 = rect.x
        self.y1 = rect.y
        self.x2 = rect.x + rect.width
        self.y2 = rect.y + rect.height
    
    def center(self):
        center_x = int((self.x1 + self.x2) / 2)
        center_y = int((self.y1 + self.y2) / 2)
        return center_x, center_y