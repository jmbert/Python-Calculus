
# Imports
import turtle
import math


# Set up turtle so it will go instantly and invisible
turtle.speed(0)
turtle.tracer(0, 0)
turtle.ht()

# Define our own curried power function
def power(a) :
    f = lambda b : pow(a, b)
    return f

# Define add function (curried)
def add(a) :
    f = lambda b : a + b
    return f

# Curried Multiply function
def multiply(a) :
    f = lambda b : a * b
    return f

# Declare turtle window
s = turtle.Screen()

# Define our grid function
def DrawGrid(screen, xOffset, yOffset) :
    turtle.tracer(0, 0)
    turtle.speed(0)
    turtle.ht()
    width, height = screen.window_width(), screen.window_height()
    turtle.penup()
    turtle.goto(-width, yOffset)
    turtle.pendown()
    turtle.goto(width, yOffset)
    turtle.penup()
    turtle.goto(xOffset, height)
    turtle.pendown()
    turtle.goto(xOffset, -height)

# Operation class
class operation :
    # Function field
    f = None;
    # Input 1
    base = None
    # Input 2
    secondary = None

    # Init
    def __init__(self, f, base = None, secondary = None) :
        
        self.f = f
        self.base = base
        self.secondary = secondary

    # Performs the operation
    def Perform(self, x) :
        # Check if this is a curried function
        if (callable(self.f(x))) :

            # Checks if the base is an operations itself
            if (isinstance(self.base, operation)) :
                # Sets y to the base's Perform (only recursive while the base is an operation) on x, then run the secondary through that
                y = self.f(self.base.Perform(x))(self.secondary)
            else :
                # Plug x into f, then run the base through that
                y = self.f(x)(self.base)
        else :
            # Checks if the base is an operations itself
            if (isinstance(self.base, operation)) :
                # Sets y to the base's Perform (only recursive while the base is an operation) on x, then run the secondary through that
                y = self.f(self.base.Perform(x))
            else :
                # Plug x into f, then run the base through that
                y = self.f(x)
            
        # Return y
        return y


# Full Function Class
class function :
    # The operation
    term = None
    # Pen to be used
    pen = turtle.Turtle()
    # Pen to be used for the derivative
    dPen = turtle.Turtle()
    # Graph Limit
    graphLim = 0
    # Detail to be graphed
    detail = 0.0

    # Init
    def __init__(self, term, graphLim, pen, detail, dPen) :

        self.term = term
        self.graphLim = graphLim
        self.pen = pen
        self.detail = detail
        self.dPen = dPen

    # Calculate the function at a given point
    def Calculate(self, base) :
        term = self.term
        y = self.term.Perform(base)
        return y
    
    # Calculate all points, of interval self.detail, from -graphlim, to graphlim
    def Graph(self) :
        # Setting x to -graphLim (so we start in the negatives)
        x = -self.graphLim
        # Declaring empty graph
        graph = []

        # Loop over all points up to graphlim
        while x < self.graphLim :
            # Append the y value at this point
            graph.append(self.Calculate(x))

            # Increment x by detail
            x = x + self.detail

        # Return the full Array
        return graph

    # Display the graph
    def DisplayGraph(self, graph, zoom, pen, yOffset, xOffset) :
        turtle.tracer(0, 0)
        pen.speed(0)
        # Hide pen
        pen.ht()
        # Lift pen
        pen.penup()
        # Setting x to -graphLim (so we start in the negatives)
        x = -graphLim
        # Setting i to 0
        i = 0
        # move to the first point (pen still up)
        pen.goto((x * zoom) + xOffset, (graph[0] * zoom) + yOffset)
        # Put pen down
        pen.pendown()
        # Loop over all fields in the graph
        while i < len(graph):
            # Move to the value at that point
            pen.goto((x * zoom) + yOffset, (graph[i] * zoom) + xOffset)
            # Increment x and i
            i = i + 1
            x = x + self.detail
    
    # Differentiate function
    def Differentiate(self, dx) :
        # Declare empty derivative array (a graph)
        derivative = []
        # Setting x to -graphLim (so we start in the negatives)
        x = -self.graphLim
        # Looping over all points up to graphlim (as before in function.Graph())
        while x < graphLim + 1:
            # Instead of calculating at point x only, we cheat on derivatives and just find the gradient between point x and point x + dx, where dx is some small amount
            derivative.append(-(self.Calculate(x) - self.Calculate(x + dx)) / dx)
            # Increment x by detail
            x = x + self.detail

        # Return the graph of the derivative
        return derivative

# Getting input
zoom = s.numinput("Zoom", "How zoomed in should the graph be", 1, minval=1, maxval=1000)
graphLim = s.numinput("Graph Limit", "How far should the graph go", 100, minval=10, maxval=1000)
dx = s.numinput("Difference in X", "Both the detail fo the graph and the detail to which the derivative is found", 0.01, minval=0, maxval=1)


# Getting pens to draw with
pen = turtle.Turtle()
pen.color("blue")
pen.speed(0)
pen.ht()

dPen = turtle.Turtle()
dPen.color("red")
dPen.speed(0)
dPen.ht()



# Instantiating function with an operation, the graph Limit, the pen, and detail
func = function(operation(power, 2), graphLim, pen, dx, dPen)

# Calculate, then display Graph
func.DisplayGraph(func.Graph(), zoom, func.pen, 0, 0)
# Calculate, then display the derivative
func.DisplayGraph(func.Differentiate(dx), zoom, func.dPen, 0, 0)

# X and Y
x = 0
y = 0


# Loop for input
while (True) :
    x = s.numinput("X", "", x, minval=-math.inf, maxval=math.inf)
    y = s.numinput("Y", "", y, minval=-math.inf, maxval=math.inf)

    # Modify Zoom
    zoom = s.numinput("Zoom", "", zoom, minval=1, maxval=math.inf)

    # Clear previous screen
    s.clearscreen()

    # Drawing our grid
    DrawGrid(s, x, y)

    # Calculate, then display Graph
    func.DisplayGraph(func.Graph(), zoom, func.pen, x, y)
    # Calculate, then display the derivative
    func.DisplayGraph(func.Differentiate(dx), zoom, func.dPen, x, y)

    # Update Screen
    turtle.update()