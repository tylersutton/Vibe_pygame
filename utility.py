class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

# function for line generation
# returns a list of directional movements make up the line
# between (x1,y1) and (x2,y2)
def line_directions(x1, y1, x2, y2):
    directions = []
    x = y = xe = ye = 0
    # calculate the line deltas
    dx = x2 - x1
    dy = y2 - y1
    # create positive copy of deltas
    dx1 = abs(dx)
    dy1 = abs(dy)
    # calculate error intervals for both axis
    px = 2*dy1 - dx1
    py = 2*dx1 - dy1

    #the line is X-axis dominant
    if dy1 <= dx1:
        # line is drawn left to right
        if dx1 >= 0:
            x = x1
            y = y1
            xe = x2
        else:
            x = x2
            y = y2
            xe = x1

        # rasterize the line
        i = 0
        while x < xe:
            x += 1
            # deal with octants
            dir_x = 1
            dir_y = 0
            if px < 0:
                px = px + 2*dy1
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    y += 1
                    dir_y = 1 
                else:
                    y -= 1
                    dir_y = -1
                px = px + 2 * (dy1 - dx1)
            # add point from line span at 
            # currently rasterized position
            directions.append((dir_x, dir_y))
            i += 1
    else: # line is Y-axis dominant
        if dy >= 0: # line is drawn bottom to top
            x = x1
            y = y1
            ye = y2
        else: # line is drawn top to bottom
            x = x2
            y = y2
            ye = y1

        # rasterize the line
        i = 0
        while y < ye:
            y += 1
            dir_y = 1
            dir_x = 0
            # deal with octants
            if py <= 0:
                py = py + 2 * dx1
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    x += 1
                    dir_x = 1
                else:
                    x -= 1
                    dir_x = -1
                py = py + 2 * (dx1 - dy1)
            # add point from line span at
            # currently rasterized position
            directions.append((dir_x, dir_y))
            i += 1
    return directions


# function for line generation
# returns a list of points that make up the line
# between (x1,y1) and (x2,y2)
def line(x1, y1, x2, y2):
    path = []
    x = y = xe = ye = 0
    # calculate the line deltas
    dx = x2 - x1
    dy = y2 - y1
    # create positive copy of deltas
    dx1 = abs(dx)
    dy1 = abs(dy)
    # calculate error intervals for both axis
    px = 2*dy1 - dx1
    py = 2*dx1 - dy1

    #the line is X-axis dominant
    if dy1 <= dx1:
        # line is drawn left to right
        if dx1 >= 0:
            x = x1
            y = y1
            xe = x2
        else:
            x = x2
            y = y2
            xe = x1
        # add first point
        path.append((x, y))
        # rasterize the line
        i = 0
        while x < xe:
            x += 1
            # deal with octants
            if px < 0:
                px = px + 2*dy1
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    y += 1
                else:
                    y -= 1
                px = px + 2 * (dy1 - dx1)
            # add point from line span at 
            # currently rasterized position
            path.append((x, y))
            i += 1
    else: # line is Y-axis dominant
        if dy >= 0: # line is drawn bottom to top
            x = x1
            y = y1
            ye = y2
        else: # line is drawn top to bottom
            x = x2
            y = y2
            ye = y1
        # add the first point
        path.append((x, y))
        # rasterize the line
        i = 0
        while y < ye:
            y += 1
            # deal with octants
            if py <= 0:
                py = py + 2 * dx1
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    x += 1
                else:
                    x -= 1
                py = py + 2 * (dx1 - dy1)
            # add point from line span at
            # currently rasterized position
            path.append((x, y))
            i += 1
    return path




"""
slightly modified from code by Nicolas Swift
https://medium.com/@nicholas.w.swift/easy-a-star-pathfinding-7e6689c7f7b2
"""
def astar(game_map, start, end):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1] # Return reversed path

        # Generate children
        children = []
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (game_map.width - 1) or node_position[0] < 0 or node_position[1] > (game_map.height -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if game_map.is_blocked(node_position[0], node_position[1]):
                continue
            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values
            child.g = current_node.g + 1
            child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)