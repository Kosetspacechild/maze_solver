"""
This is a stub for the comp16321 midterm.
Do not edit or delete any lines given in this file that are marked with a "(s)".
(you can move them to different lines as long as you do not change the overall structure)

Place your code below the comments marked "#Your code here".

Each method is documented to explain what work is to be placed within it.
"""


def read_mazes():#(s)
    """
        Read in the text file and save the mazes into a python list

        :return: A list of strings denoting each maze
    """

    # Your code here

    with open("mazes.txt", "r") as f:
        contents= f.read()
        maze_strings= [i for i in contents.split("\n") if i != ""]

    #using with to open the file we avoid having to close it.
    #after opening the file we read into it using .read()
    #we use list comprehension to get rid of all blank spaces and split the mazes

    return (maze_strings)#(s)

def validate_mazes(maze_strings):#(s)
    """
        Validate if the input from the text file is correct based on the rules defined

        :param: list maze_strings: The list of strings denoting each maze
        :return: A list of string values in order denoting if the input
            is invalid as defined in the specification
    """

    # Your code here

    char_list= ["0","1","S","E"]
    maze_validation= maze_strings.copy()    #copies maze_strings into maze_validation

    for i in range(len(maze_strings)):  #for loop for each maze
                                        #range() so that it counts for all the items in the list. 
                                        # len() so that it knows how many items
        string_items= maze_strings[i].split(",")      #[i] so that it does it in every item
        for item in string_items:                       #reiterate through every line in maze
            validation= all(char in char_list for char in item)     #validate letters in every item
            if validation == False:
                maze_validation[i]= "invalid"
                break

    return (maze_validation)#(s)


def transform_input(maze_strings, maze_validation):#(s)
    """
        Transform the valid mazes into a 2d array and combine the list with the maze validation
        list as defined in the specification

        :param: list maze_strings: The list of strings denoting each maze
        :param: list maze_strings: The list of string values in order denoting if the input
            is incorrect based on the described rules
        :return: A list of 2d arrays and string values in order denoting mazes and invalid inputs as
            defined in the specification
    """

    # Your code here

    transformed_maze_validation= maze_validation.copy()

    for i in range(len(maze_strings)):
        if maze_validation[i]== "invalid":
            continue        #if invalid, keep it that way and continue
        
        maze= []
        maze_rows= maze_strings[i].split(",")        #.split() to get the rows
        for row in maze_rows:
            chars= [*row]                           #split them further into chracters
            for j in range(len(chars)):
                if chars[j] == "1" or chars[j] == "0":
                    chars[j]= int(chars[j])         #makes 0 and 1 into intergers
            maze.append(chars)                      #.append() to make 2d array
        transformed_maze_validation[i]= maze        #entering this into the list to make array

    return (transformed_maze_validation)#(s)


def solve_mazes(transformed_maze_validation):#(s)
    """
        Determine if each valid maze is solvable and then solve them by providing the coordinates
        in the order required to traverse the maze from start to end

        :param: The list of 2d arrays and string values in order denoting mazes and invalid inputs
        :return: A list of coordinate lists and string values in order denoting solutions, invalid inputs
            and unsolvable mazes as defined in the specification

    """

    # Your code here

    #using depth-first search: https://www.educative.io/answers/how-to-implement-depth-first-search-in-python

    solved_transformed_maze_validation= transformed_maze_validation.copy()

    for i in range(len(transformed_maze_validation)):
        if transformed_maze_validation[i]== "invalid":
            continue
        maze= transformed_maze_validation[i]

        #finding starting point and end if there is

        starting_point= "S" in maze[0] or "S" in maze[-1] or "S" in [row[0] for row in maze] or "S" in [row[-1] for row in maze]
        ending_point= "E" in maze[0] or "E" in maze[-1] or "E" in [row[0] for row in maze] or "E" in [row[-1] for row in maze]

        if starting_point == False or ending_point == False:
            solved_transformed_maze_validation[i]= "Unsolvable"
            #if there is no start or end on the edges, the maze us unsovable
            continue

        #actually solving the solvable mazes:

        for j in range(len(maze)):
            for k in range(len(maze[0])):
                if maze[j][k] == "S":
                    starting_point= (j,k)   #starting_point coordinates saved
                elif maze[j][k] == "E":
                    ending_point= (j,k)     #ending_point coordinates saved

        routes= []
        path= []
        travel_maze(maze, starting_point, routes, ending_point, path)
        if len(routes) == 0:
            solved_transformed_maze_validation[i]= "Unsolvable"

        else:
            routes.sort(key= len)   #key is what .sort() sorts by
            shortest_path = [list(coord) for coord in routes[0]]
            solved_transformed_maze_validation[i]= shortest_path   #first route which is the shortest one

    return (solved_transformed_maze_validation)#(s)

#function that gets a list of the neighbour items to a coordinate
#adds to a list called path that stores all neighbouring paths possible in the form of coordinates

def get_neighbours(maze, coord):
    y= coord[0]
    x= coord[1]
    paths= []
    if y > 0 and maze[y - 1][x] != 1:
        paths.append((y - 1, x))
    if x > 0 and maze[y][x - 1] != 1:
        paths.append((y, x - 1))
    if y < len(maze) - 1  and maze[y + 1][x] != 1:
        paths.append((y + 1, x))
    if x < len(maze[0]) -1  and maze[y][x + 1] != 1:
        paths.append((y, x + 1))

    return (paths)

#recursive function for the depth-first search:

def travel_maze(maze, coord, routes, ending_point, paths):
    paths.append(coord)
    if coord == ending_point:
        routes.append(paths.copy())
        #print(routes)
        paths.pop()
        return

    #visit the possible neighbours you haven't been to before
    
    neighbours= get_neighbours(maze, coord)

    #for loop for each viable neighbour to repeat function till you reach ending_point

    for neighbour in neighbours:
        if neighbour not in paths:
            travel_maze(maze, neighbour, routes, ending_point, paths)

    paths.pop()
    return

if __name__ == '__main__':
    # You can place any ad-hoc testing here
    # i.e mazes = read_mazes()
    # i.e print(mazes)

    #test= read_mazes()
    #print(test)
    #test1= validate_mazes(test)
    #print(test1)
    #test2= transform_input(test, test1)
    #print(test2)
    #test3= solve_mazes(test2)
    #print(test3)
    pass
