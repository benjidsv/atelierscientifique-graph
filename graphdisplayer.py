import turtle
import time

# TODO: Optimiser

def DrawGraph(G, path=0, scale=100, animationspeed=0, linethickness=5, nodesize=10, bgcolor="black", graphcolor="white", pathcolor="red", startcolor="cyan", finishcolor="lime"):
    # paramétrage de l'écran
    wn = turtle.Screen()  
    wn.bgcolor(bgcolor)

    # paramétrage du turtle
    t = turtle.Turtle()
    t.hideturtle()
    t.pencolor(graphcolor)
    t.pensize(linethickness)
    t.fillcolor(graphcolor)
    t.speed(0)


    # traçage du graphe et dessin des noeuds
    i = 0
    nodecount = len(G)
    start = time.time()
    tracedlines = []
    for node in G:
        percentage = round(i / nodecount * 100, 2)
        nodesleft = nodecount - i
        print(f"Status: {percentage} % completed. There is {nodesleft} nodes left to draw.")

        scalednode = (node[0] * scale, node[1] * scale)

        t.penup()
        TraceCircle(t, scalednode, nodesize, graphcolor)
        t.goto(scalednode)
        t.pendown()


        for neighbor in G[node]:
            if (node, neighbor) not in tracedlines and (neighbor, node) not in tracedlines:
                scaledneighbor = (neighbor[0] * scale, neighbor[1] * scale)
            
                t.goto(scaledneighbor) 
                t.goto(scalednode)

                tracedlines.append((node, neighbor))
        
        i+=1

    t.penup()

    end = time.time()
    s = end - start
    print(f"Status: 100%. Task completed successfully. It took {round(s // 60)}mn{round(s % 60)}s to complete the graph.")

    # traçage du chemin, du départ et de l'arrivée si un chemin est donné en paramètres
    if path != 0:
        start = (path[0][0] * scale, path[0][1] * scale)
        finish = (path[-1][0] * scale, path[-1][1] * scale) # path[-1] est le dernier élement de path (-1 le 1er en partant de la fin, -2 le deuxième, etc.)

        TraceCircle(t, start, nodesize, startcolor)

        t.color(pathcolor)
        t.goto(path[0][0] * scale, path[0][1] * scale)
        t.pendown()
        
        t.speed(animationspeed)
        for node in path:
            t.goto(node[0] * scale, node[1] * scale)
        t.penup()

        TraceCircle(t, finish, nodesize, finishcolor)
    
    wn.mainloop()   


def TraceCircle(t, pos, radius, color):
    t.speed(0)
    t.color(color)
    t.goto(pos[0], pos[1] - radius)
    t.begin_fill()
    t.circle(radius)
    t.end_fill()