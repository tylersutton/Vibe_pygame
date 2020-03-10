import pygame

def load_tile_table(filename, width, height):
    image = pygame.image.load(filename).convert()
    image_width, image_height = image.get_size()
    tile_table = []
    for tile_x in range(0, image_width//width):
        line = []
        tile_table.append(line)
        for tile_y in range(0, image_height//height):
            rect = (tile_x*width, tile_y*height, width, height)
            line.append(image.subsurface(rect))
    return tile_table

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    table = load_tile_table("assets/overworld_tileset_grass.png", 16, 16)
    print('we made it')
    while 1:
        # 5 - clear the screen before drawing it again
        screen.fill(0)
        # 6 - draw the screen elements
        for x, row in enumerate(table):
            for y, tile in enumerate(row):
                screen.blit(tile, (x*24, y*24))
        # 7 - update the screen
        pygame.display.flip()
        # 8 - loop through the events
        for event in pygame.event.get():
            # check if the event is the X button
            if event.type==pygame.QUIT:
                # if it is quit the game
                pygame.quit()
                exit(0)

if __name__=='__main__':
    main()