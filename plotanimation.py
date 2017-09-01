''' 
@author: Rory Andrews
@adapted by: Marco de Lannoy Kobayashi
'''
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Example usage:
# $ python plotanimation.py weightset.txt exampleset.txt ouputfilename.mp4
# weightset.txt is generated from perceptron.py using the same exampleset.txt
# outputfilename.mp4 will be the name of the video of the animation. it must end with .mp4

def get_limits(point_data):
    lim = [point_data[0],point_data[0]]
    for i in point_data:
        if i < lim[0] + 1:
            lim[0] = i - 1
        if i > lim[1] - 1:
            lim[1] = i + 1
    return lim

def get_points(weights, xlim, ylim):
    bias = weights[0]
    weight1 = weights[1]
    weight2 = weights[2]
    pt1 = [0,0]
    pt2 = [0,0]
    if weight1 == 0 and weight2 == 0:
        pass
    elif weight1 == 0: # Horizontal line
        pt1[1] = -bias / weight2
        pt2[1] = pt1[1]
        pt1[0] = xlim[0]
        pt2[0] = xlim[1]
    elif weight2 == 0: # Vertical line
        pt1[0] = -bias / weight1
        pt2[0] = pt1[0]
        pt1[1] = ylim[0]
        pt2[1] = ylim[1]
    else: # y=mx+b
        slope = -weight1 / weight2
        inter = -bias / weight2
        x = (ylim[0] - bias) / weight1
        y = -bias / weight2
        pt1 = [xlim[0], xlim[0]*slope + inter]
        pt2 = [xlim[1], xlim[1]*slope + inter]

    return [pt1,pt2,'k']

def update_line(line_data, line):
    line.set_ydata([line_data[0][1], line_data[1][1]])
    line.set_xdata([line_data[0][0], line_data[1][0]])
    line.set_color(line_data[2])
    sys.stdout.write('#')
    sys.stdout.flush()

    return line

def animate(weight_data,point_data,outputfile):
    # Parse point data
    point_data1 = [[],[]]
    point_data2 = [[],[]]
    for row in point_data:
        #row = row.split(',')
        if float(row[2]) <= 0:
            point_data1[0].append(float(row[0]))
            point_data1[1].append(float(row[1]))
        else:
            point_data2[0].append(float(row[0]))
            point_data2[1].append(float(row[1]))

    # Get xlim and ylim (1 greater or lesser than the smallest and largest value)
    xlim = get_limits(point_data1[0] + point_data2[0])
    ylim = get_limits(point_data1[1] + point_data2[1])
    #print("Limits:") #TODO create verbose mode and show this
    #print(xlim)
    #print(ylim)

    # Get line_data to draw lines.
    line_data = []
    for row in weight_data:
        line_data.append(get_points(row, xlim, ylim))
    if len(line_data) > 0:
        last = line_data[-1]
        last[2] = 'r'
        last2 = list(last)
        last2[2] = 'y'
        for i in range(4):
            line_data.append(last)
            line_data.append(last2)

    #for row in line_data: #TODO create verbose mode and show this
        #print(row)
        
    fig, ax = plt.subplots()

    # Get figure, set limits, get line.
    ax.axis([xlim[0],xlim[1],ylim[0],ylim[1]])
    line, = ax.plot(0,0,'k')


    # Plot the example points.
    ax.plot(point_data1[0], point_data1[1], 'b.')
    ax.plot(point_data2[0], point_data2[1], 'r.')


    line_ani = animation.FuncAnimation(fig, update_line, line_data,
                                       fargs=(line,), interval=300)
    line_ani.save(outputfile)
    print(' . . . [animation complete]')

if __name__ == '__main__':
    # Get Weight Data
    if len(sys.argv) > 1:
        wfile = sys.argv[1]
    with open(wfile) as weight_file:
        data = weight_file.read()
    rows = data.strip().split('\n')
    weight_data = []
    for row in rows:
        row = row.split(',')
        weight_data.append([float(row[0]), float(row[1]), float(row[2])])

    # Get Point Data
    if len(sys.argv) > 2:
        dfile = sys.argv[2]
    with open(dfile) as data_file:
        point_data = [[col for col in row.split(',')]
                      for row in data_file.read().strip().split('\n')]
        #rows = point_data.strip().split('\n')

    # Get output filename
    if len(sys.argv) > 3:
        outputfile = sys.argv[3]
    else:
        outputfile = "graph.mp4"  
  
    animate(weight_data,point_data,outputfile)
