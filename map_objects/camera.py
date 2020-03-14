class Camera:
    def __init__(self, game_map, player, width, height):
        self.game_map = game_map
        self.player = player
        self.width = width
        self.height = height
        self.x, self.y = self.clamp(self.player.x, self.player.y)
        

    def update(self):
        self.x, self.y = self.clamp(self.player.x - (self.width//2), self.player.y - (self.height//2))
        
    
    def clamp(self, x, y):
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        if x + self.width >= self.game_map.width:
            x = max(0,self.game_map.width - self.width)
        if y + self.height >= self.game_map.height:
            y = max(0,self.game_map.height - self.height)
        return x, y