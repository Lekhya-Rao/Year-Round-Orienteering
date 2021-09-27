import math
import sys
import numpy as np
from PIL import Image

# stores speed according to terrain
# open land
terrain_speeds = {(248, 148, 18): 100}
# rough meadow
terrain_speeds[(255, 192, 0)] = 50
# easy movement forest
terrain_speeds[(255, 255, 255)] = 90
# slow run forest
terrain_speeds[(2, 208, 60)] = 70
# walk forest
terrain_speeds[(2, 136, 40)] = 60
# impassible vegetation
terrain_speeds[(5, 73, 24)] = 0.01
# lake swamp marsh
terrain_speeds[(0, 0, 255)] = 0.1
# paved road
terrain_speeds[(71, 51, 3)] = 70
# footpath
terrain_speeds[(0, 0, 0)] = 80
# out of bounds
terrain_speeds[(205, 0, 101)] = 0.001

# stores the elevation of each pixel
elevations = []
# stores the RGV value of each pixel
pixels = []
# stores the path from source to destination.
path = []
# stores water pixels
water = []
# stores pixels to color
colorpath = []
color = None


def processElevationFile(elevation_file):
    """
    this method pocesses the elevation file given.
    :param elevation_file: elevation file name
    :return: list of elevations mapped to pixel coordinates.
    """
    # contains elevations as a two dimensional list
    elevation = [[]] * 500
    with open(elevation_file) as f:
        i = j = 0
        for line in f:
            str_elevations = line.strip().split()
            elevation[i] = str_elevations[0:len(str_elevations) - 5]
            for j in range(0, len(str_elevations) - 5):
                elevation[i][j] = float(elevation[i][j])
            i = i + 1
    return elevation


def processPathFile(path_file):
    """
    this method processes the path file given.
    :param path_file: name of path file
    :return: list containing points to be visited in order.
    """
    # contains path as a two dimensional list
    paths = []
    with open(path_file) as f:
        i = j = 0
        for line in f:
            str_paths = line.strip().split()
            paths.append(str_paths)
            for j in range(0, len(str_paths)):
                paths[i][j] = int(paths[i][j])
            i = i + 1
    return paths


def loadImage(image_file):
    """
    this method process the image file given.
    :param image_file: image file name
    :return: reference to the input image and a list
                containing RGB values of each pixel in the image.
    """
    # load the image
    image = Image.open(image_file)
    image = image.convert("RGB")
    # convert image to numpy array
    image_data = np.asarray(image)
    # stores pixel color
    pixels = []
    for i in range(500):
        pixels.append([])
        for j in range(395):
            pixels[i].append(image.getpixel((j, i)))
    return image, pixels


class node:
    """
    Here node represents a pixel in the image with the properties:
        x coordinate
        y coordinate
        speed of terrain in which pixel is located
        total distance travelled
        pixel elevation
        heuristic value
        pathcost calculated as time+heuristic
        list of possible neighbors
        parent pixel
        destination
        time taken to travel till current pixel

    """
    __slots__ = 'x', 'y', 'speed', 'distance', 'elevation', \
                'heuristic', 'pathCost', 'action', 'parent', \
                'goal', 'topath'

    def __init__(self, x, y, goal=None, parent=None, pathCost=0):
        self.x = x
        self.y = y
        self.goal = goal
        self.speed = terrain_speeds[pixels[x][y]]
        self.parent = parent
        self.elevation = elevations[self.x][self.y]
        self.distance = self.calcDistance()
        self.heuristic = 0
        self.topath = 0
        self.pathCost = pathCost
        self.heuristic = (self.calcHeuristic())
        if parent is not None:
            self.topath = self.parent.topath + self.calcDistance() / self.speed
            self.pathCost = self.topath + self.heuristic
            self.distance = self.distance + self.parent.distance

        self.action = []
        self.action = self.possibleActions()

    def possibleActions(self):
        """
        This method returns a list of all possible neighbors to a pixel

        :return: list of all possible neighbors
        """
        moves = []
        if self.x != 0:
            moves.append([self.x - 1, self.y, self])
            if self.y != 0:
                moves.append([self.x - 1, self.y - 1, self])
            if self.y != 394:
                moves.append([self.x - 1, self.y + 1, self])
        if self.x != 499:
            moves.append([self.x + 1, self.y, self])
            if self.y != 0:
                moves.append([self.x + 1, self.y - 1, self])
            if self.y != 394:
                moves.append([self.x + 1, self.y + 1, self])
        if self.y != 0:
            moves.append([self.x, self.y - 1, self])
        if self.y != 394:
            moves.append([self.x, self.y + 1, self])
        # stores out of bounds elements in moves
        counter = []
        # creates a list of out of bounds elements in moves
        for i in moves:
            if terrain_speeds[pixels[i[0]][i[1]]] < 1:
                counter.append(i)
        # removes all out of bounds elements from moves
        for i in counter:
            moves.remove(i)
        return moves

    def calcDistance(self):
        """
        calculates distance travelled from previous pixel to current pixel
        :return: distance
        """
        if self.parent is None:
            return 0
        x = abs(self.parent.x - self.x) * 7.55
        y = abs(self.parent.y - self.y) * 10.29
        # z = abs(self.parent.elevation - self.elevation)
        return math.sqrt(x ** 2 + y ** 2)

    def calcHeuristic(self):
        """
        calculates heuristic as euclidean distance between current pixel and destination
        :return: heuristic value
        """
        x = abs(self.x - self.goal[0])
        y = abs(self.y - self.goal[1])
        z = abs(self.elevation - elevations[self.goal[0]][self.goal[1]])
        return math.sqrt(x ** 2 + y ** 2 + z ** 2)


def solution(node):
    """
    Given a node, this function traces the parent chain of this node.
    :param node: the node to be traced
    :return: list containing the parent trace
    """
    sol = []
    dist = node.distance
    while node is not None:
        sol.append([node.x, node.y])
        node = node.parent
    sol = sol[::-1]
    return sol, dist


def comparePathcost(el):
    """
    given an element, it returns the property of element to be
    considered for sorting.
    :param el: element
    :return: property to be considered for sorting
    """
    return el.pathCost


def modifySearch(initial_sate, goalState):
    """
    performs A* search to ind best path between 2 given points
    :param initial_sate: source
    :param goalState: destination
    :return: best path between source and destination
    """
    # stores the list of nodes to be explored.
    frontier = []
    # stores list of explored nodes
    explored = []
    goal = goalState[::-1]

    def frontierCheck(child, listt):
        """
        given a node and a list, it determines it the node's
        coordinates already exist in the list.
        :param child: node
        :param listt: list
        :return: index at which coordinatees are found
                    else -1
        """
        for i in range(len(listt)):
            if listt[i].x == child.x and listt[i].y == child.y:
                return i
        return -1

    # creates a node for source
    initialState = node(initial_sate[1], initial_sate[0], goal)
    # source is appended to frontier
    frontier.append(initialState)
    while frontier:
        # element with least path cost is popped
        frontier.sort(key=comparePathcost)
        currentNode = frontier.pop(0)
        # if current element is destination, return path
        if currentNode.x == goal[0] and currentNode.y == goal[1]:
            return solution(currentNode)
        # else add to explored list
        explored.append(currentNode)
        for move in currentNode.action:
            # for each neighbor of current node
            child = node(move[0], move[1], goal, currentNode)
            exists = frontierCheck(child, frontier)
            if frontierCheck(child, explored) == -1:
                if exists == -1:
                    # if neighbor has not been encountered before add to frontier
                    frontier.append(child)
                elif exists != -1 and frontier[exists].pathCost > child.pathCost:
                    # if neighbor was encountered and pathcost of current neighbor is
                    # less than that of visited neighbor, replace the old neighbor
                    # with current neighbor
                    frontier.pop(exists)
                    frontier.append(child)
    # if path not found return false
    return False


def imageOutput(source, destinaton, path, colorpath=None, colour=None):
    """
    displays the terrain with path drawn
    :param source: image file
    :param destinaton: name of image to be diaplayed
    :param path: path travelled
    :param distance: distance travelled

    """

    image = Image.open(source)
    image = image.convert("RGB")
    colour = colour
    color = (243, 9, 9)
    # for i in path:
    #     for j in i:
    #         image.putpixel((j[1], j[0]), color)
    if len(colorpath) != 0:
        for i in colorpath:
            for j in i:
                image.putpixel((j[1], j[0]), colour)
    for i in path:
        for j in i:
            image.putpixel((j[1], j[0]), color)

    image.save(destinaton + '.png')
    image.show()



def findWater():
    """
    creates a list of all water pixels in the image
    :return: list of water pixels
    """

    water = []
    for i in range(500):
        for j in range(395):
            if pixels[i][j] == (0, 0, 255):
                water.append([i, j])
    return water


def waterNeighboers(el):
    """
    creates a list of neighbors upto 7 pixels for current pixel
    :param el: current pixel
    :return: list of neighbors
    """
    x = el[0]
    y = el[1]
    moves = []
    for i in range(1, 8):
        if x - i > 0:
            moves.append([x - i, y])
            if y - i > 0:
                moves.append([x - i, y - i])
            if y + i < 394:
                moves.append([x - i, y + i])
        if x + i < 499:
            moves.append([x + i, y, ])
            if y - i > 0:
                moves.append([x + i, y - i])
            if y + i < 394:
                moves.append([x + i, y + i])
        if y - i > 0:
            moves.append([x, y - i])
        if y + i < 394:
            moves.append([x, y + i])
    counter = []
    for i in moves:
        if terrain_speeds[pixels[i[0]][i[1]]] < 0.1:
            counter.append(i)
    for i in counter:
        moves.remove(i)
    return moves


def bfs(source, water_list):
    """
    performs BFS to create a list of all water pixels
    within 7 pixels from a land pixel.
    :param source: source node
    :param water_list: list of water pixels
    :return: list of pixels to be colored in winter
    """
    # stores list of pixels to be colored
    color_pixel = []
    # stores the list of nodes to be explored.
    frontier = []
    # stored the list of words explored.
    explored = []
    # goal is water
    goal = (0, 0, 255)
    initialState = source
    frontier.append(initialState)
    while len(frontier) != 0:
        currentNode = frontier.pop(0)
        # current element being considered is removed from water pixels list
        water_list.remove(currentNode)
        # current element being considered is added to explored
        explored.append(currentNode)
        # neighbors of current pixel are generated
        neighbors = waterNeighboers(currentNode)
        for move in neighbors:
            if pixels[move[0]][move[1]] != goal and currentNode not in color_pixel:
                # if neighbor is non water pixel and current node not already in
                # color_pixel, add to color_pixel
                color_pixel.append(currentNode)
            elif pixels[move[0]][move[1]] == goal and move not in frontier and move not in explored:
                # if neighbor is water pixel and has not been visited yet
                # append to frontier
                frontier.append(move)
    return color_pixel


if __name__ == '__main__':
    # stores input image filename
    image_file = sys.argv[1]
    # stores elevation path filename
    elevation_file = sys.argv[2]
    # stores path filename
    path_file = sys.argv[3]
    # stores season
    season = sys.argv[4]
    # stores name of output image
    output_file = sys.argv[5]
    elevations = processElevationFile(elevation_file)
    path = processPathFile(path_file)
    image, pixels = loadImage(image_file)
    # stores total distance travelled
    total_distance = 0
    # stores total path travelled
    total_path = []

    if season == 'fall':
        # if season is fall, speed of easy movement forest is updated.
        terrain_speeds[(255, 255, 255)] = 70

    elif season == 'winter':
        # if season is winter, updating speed for ice
        terrain_speeds[(190, 250, 255)] = 90
        # update color of snow pixels
        color = (190, 250, 255)
        # list of water pixels
        water = findWater()
        l = water
        colorpath = []
        # implementing bfs to find ice pixels
        while l:
            colorpath.append(bfs(l[0], l))
        colorpath = colorpath
        # updating color of ice pixels in pixels list
        for i in colorpath:
            for j in i:
                pixels[j[0]][j[1]] = (190, 250, 255)

        for i in range(len(path) - 1):
            # parsing through path file and find best path between
            # 2 consecutive points given in path file.
            curr_path, curr_dist = modifySearch(path[i], path[i + 1])
            total_distance = total_distance + curr_dist
            total_path.append(curr_path)
        imageOutput(image_file, output_file, total_path, colorpath, color)
        print(total_distance)
    else:
        for i in range(len(path) - 1):
            # parsing through path file and find best path between
            # 2 consecutive points given in path file.
            curr_path, curr_dist = modifySearch(path[i], path[i + 1])
            total_distance = total_distance + curr_dist
            total_path.append(curr_path)
        imageOutput(image_file, output_file, total_path, [])
        print(total_distance)
