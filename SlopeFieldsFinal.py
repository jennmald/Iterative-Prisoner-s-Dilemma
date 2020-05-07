import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import numpy
from numpy import sqrt, sin, cos
import pylab as P

# use numpy.linspace(start, end, numPoints)


# dx/dt = f(x,y)
def dx(x,y):
    return -y

# dy/dt = g(x,y)
def dy(x,y):
    return x

# function for Euler's Method
# dx/dt = f(x,y)
# dy/dt = g(x,y)
# starting point on graph: (x0, y0)
# returns [ (x0,y0), (x1,y1), ... ]
#         [ (x0,x1,...), (y0,y1,...) ]
def eulersMethod(f, g, x0, y0, deltaT, numSteps):
    xValues = [x0]
    yValues = [y0]
    xCurrent = x0
    yCurrent = y0
    for i in range (0,numSteps):
        deltaX = f(xCurrent,yCurrent) * deltaT
        deltaY = g(xCurrent,yCurrent) * deltaT
        xNext = xCurrent + deltaX
        yNext = yCurrent + deltaY
        xValues.append( xCurrent )
        yValues.append( yCurrent )
        xCurrent = xNext
        yCurrent = yNext
    return [ xValues, yValues ]


xValues, yValues = eulersMethod( dx,dy, 1,0, 0.01, 630 )

plt.plot( xValues, yValues, c="gray" )

## slope field code
xMin = -2
xMax = 2
xDivisions = 20
xRange = numpy.linspace( xMin, xMax, xDivisions )

yMin = -2
yMax = 2
yDivisions = 20
yRange = numpy.linspace( yMin, yMax, yDivisions )

# note: choose good value based on x and y ranges
epsilon = 0.05

# point-slope equation of a line
def line(m, x0, y0):
    return lambda x : m * (x - x0) + y0

# finding vectors from points
# normalizing them on some scale
# returning the new vector point
def normalizeVectors(x0,y0,x,y):
    lengthScale = 1/xDivisions # hopefully change this to a function
    vx = x - x0
    vy = y - y0
    lengthV = sqrt(vx*vx + vy*vy)
    vx = vx / lengthV * lengthScale
    vy = vy / lengthV * lengthScale
    x = x0 + vx
    y = y0 + vy
    return [x,y]

for xCurrent in xRange:
    for yCurrent in yRange:
        deltaX = dx( xCurrent, yCurrent ) * epsilon
        deltaY = dy( xCurrent, yCurrent ) * epsilon
        xNext = xCurrent + deltaX
        yNext = yCurrent + deltaY
        xNext, yNext = normalizeVectors(xCurrent,yCurrent, xNext,yNext)

        #plt.plot( [xCurrent, xNext], [yCurrent, yNext])
        plt.arrow( xCurrent, yCurrent, deltaX, deltaY, fc="k", ec="k", head_width=0.05, head_length=0.05 )
        plt.xlim(-2,2)
        plt.ylim(-2,2)
        plt.title('Slope Field')
        plt.xlabel('x')
        plt.ylabel('y')


##tValues = numpy.arange( -6.28, 6.28, 0.01 )
##xValues = x(tValues)
##yValues = y(tValues)
##
##plt.plot( xValues, yValues, c="orange" )
##
##
###P.subplot(111)
### P.arrow( x, y, dx, dy, **kwargs )
##
##P.show()


plt.show()

        
