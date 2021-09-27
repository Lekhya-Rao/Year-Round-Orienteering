# Year-Round-Orienteering
LAB-1:YEAR-ROUND
ORIENTEERING
LEKHYA RAO MUMMAREDDY
The solution to the given problem uses the following methods:
1.Functions to process the input files:
These functions take as input the filename and create a list containg the
information in the file.
 For the elevation path, a list elevations is created which reads the file and
stores the elevations as float values according to the coordinates of each
pixel.
 For the image file, a reference to the image is created, which is then used to
perform any required operations on the image, like save(),show() etc.For
this, the Python Image Library is used. After processing the image, a list
pixels is created consisting of the RGB values of pixels in the image
according to their coordinates.
 For the path file, a list path is created, which consists of all the controls to
be visited in their respective order.
2.Speed:
Inorder to take into consideration the ability to be able to traverse through
different terrains, a dictionary terrain_speeds is created, which maps the different
terrains with an appropriate speed.
The speeds are assigned in the following order:
Open Land (100) > Easy movement forest (90) > Footpath (80) > Slow run forest,
Paved road (70) > Walk forest (60) > Rough Meadow (50) > Lake, swamp or
marsh (0.1) > Impassible vegetation (0.01) > Out of bounds (0.001)
3.Pixel representation:
In order to efficiently represent the pixels and their respective information, a class
node is used. The members of the node are:
x - x coordinate
y - y coordinate
speed - speed of terrain in which pixel is located
distance - total distance travelled
elevation - pixel elevation
heuristic - heuristic value ( The heuristic value is calculated as euclidean distance
between the current pixel and the destination pixel in 3 dimenstions i.e
x,y,elevation)
pathCost - pathcost calculated as time(i.e topath)+heuristic
action - list of possible neighbors
parent - parent pixel
goal - destination
topath - time taken to travel till current pixel (calculated as time taken till parent
node+(distance tavelled from parent to current pixel)/speed of current pixel)
The class node also contains the functions:
i. a constructor init() to initialize the values of node members.
ii. possibleActions: which creates a list of possible neighbor coordinates from
current pixels by eliminating any out of bouns pixels.
iii. calcDistance: which returns the euclidean distance travelled between
parent pixel and current pixel. In order to consider real time distance, the
difference between corresponding x and y coordinates are multiplied by a
factor od 10.29 and 7.55 respectively.
iv. calcHueristic: which calclulates the euclidean distance between the current
pixel and the destination pixel in 3 dimenstions i.e x,y,elevation.
In order to ensure that the heuristic is admissible, the euclidean distance is taken
which is always less than or equal to the actual distance, hence the heuristic value
never over estimates the actual value. The cost fuction here is the sum of the time
taken to travel till current node and the euclidean distance between the current
node and the destination which also takes elevation into consideration. If feel that
this cost function is effective because the heuristic fuction is admissible, improving
the performance of the A* algorithm and also by considering time taken to travel,
we use the information about the different terrains and the possible speed in
them. Which helps us choose the best optimal path between two points.
3. A* Search Algorithm:
Given two points the A* algorithm find the best possible path between them by
choosing an efficient cost for each possible step.
The algorithm is implemented in the following manner:
- The algorithm consists of two lists:
frontier: stores list of pixels to be explored.
explored: stores list of pixels already explored.
- While frontier is not empty, frontier is sorted according to the pathcost.
- The pixel node with least pathcost is popped from frontier and this becomes the
current node.
- It is checked whether the current node is the destination pixel, if yes, its path is
traced and returned. Else we continue.
- The current node is then added to the explored list.
- For each neighbor of current node it is checked whether the node exists in
explored and frontier.
- If it exists in frontier and the pathcost of existing node is greater than that of
current neighbor, the existing node is replaced with the current neighbor in
frontier.
- If the neighbor does not exist in both frontier and explored, it means the
neighbor has not been visited yet. It is then added to the frontier .
4. Solution:
In order to trace the path of a given node, this method traverses through the
node's coordinates to the root parent's coordinated and returns the list of
coordinates from parent to child.
This method also returns the distance of the given node, which represents the
total distance travelled till current node.
5.Output Image:
Once all the points in the the path file are travered through, the trace of path
between every two consecutive points in path file is stored in a list which is given
as input along with the input image filename and output image filename to the
function imageOutput . This method goes through the trace of path travelled and
changes the color of every pixel in the path in the image file and stores it in the
output filename provided and displays this image.
The total distance travelled is also reflected on the terminal.
6.Seasons:
i. Summer: the images provided are taken in summer, hence the algorithm
remains accurate for summer without any changes.
ii. Fall: in this season, the leaves fall and the paths through the woods become
covered making it a little harder to travel through such paths. To reflect this,
the speed for easy movement forest in fall has been decreased to account
for increased time taken to travel such paths.
iii. Winter: in this season, the water pixels within 7 pixels of non-water pixels
freezes and is safe to walk on. Such pixels are found by implementing BFS in
the following manner:
- first a list of all water pixels is created using findWater
- the function waterNeighbors is used to create a list of all neighbors
within 7 pixels of a given pixel, any neighbors that are out of bounds are
removed from the list.
- the terrain_speed of ice is added to the dictionary, so the frozen path is
considered by A*.
- The BFS algorithm consists of 2 lists,
frontier: stores list of water pixels to be explored.
explored: stores list of water pixels already explored.
colour_pixel: stores list of pixels to be colored.
-While there are elements in waterpixels, the bfs algorithm is
implemented for the first element in the list.
- The first element is added into frontier.
- For each iteration of the algorithm, the first element of frontier is
popped, this becomes our current pixel.
-The current pixel is also removed from water pixels and added to
explored.
- For each neighbor of current pixel, if the neighbor is a non water pixel
and current pixel is not in color_pixel, current pixel is added into list of pixels
to be colored, as one of its neighbors within 7 pixels is a non-water pixel.
- If the neighbor is a water pixel and it is not already in frontier or
explored, i.e it has not been visited yet, then it is added to frontier.
-This is repeated till all water pixels are considered.
- The BFS then returns the list of pixels to be coloured.
- First we update the color of pixels in pixels list, implement A*
search.
- In outputImage we update the color of path pixels as well as the frozen
pixels to be colored.
