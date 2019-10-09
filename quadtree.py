import numpy as np
import random
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Point():
    def __init__(self, x, y):
        self.x = x
        self.y = y

#Klassi gia ton orismo twn oriwn
class Rect():
    def __init__(self, xL, yL, w, h):
        self.xL = xL
        self.yL = yL
        self.width = w
        self.height = h
    
    def contains(self, point):
        return (point.x >= self.xL and point.x <= self.xL + self.width and point.y >= self.yL and point.y <= self.yL + self.height)

    def intersects(self, distRec):
        return not (self.xL > distRec.xL + distRec.width or distRec.xL > self.xL + self.width or self.yL + self.height < distRec.yL or distRec.yL + distRec.height < self.yL)

class QuadTree():
    def __init__(self, boundary, k):
        self.boundary = boundary
        self.capacity = k
        self.points = []
        self.divided = False


    def subdivide(self):
        #Gia dieykolinsi
        x = self.boundary.xL
        y = self.boundary.yL
        w = self.boundary.width
        h = self.boundary.height

        #Dimioyrgia 4 perioxwn NE,NW,SE,Sw
        ne = Rect(x + w/2, y + h/2, w/2, h/2)
        self.northeast = QuadTree(ne, self.capacity)
        nw = Rect(x, y + h/2, w/2, h/2)
        self.northwest = QuadTree(nw, self.capacity)
        se = Rect(x + w/2, y, w/2, h/2)
        self.southeast = QuadTree(se, self.capacity)
        sw = Rect(x, y, w/2, h/2)
        self.southwest = QuadTree(sw, self.capacity)

        #Egine diairesi tis arxikis perioxis
        self.divided = True

        v = len(self.points)
        for u in range(v):
            self.insert(self.points.pop())
        
        
    #kanei update ta shmeia apo gonio se paidia i apo paidia se gonio
    def PopAndInsert(self, p):
        v = len(self.points)
        for u in range(v):
            p.append(self.points.pop())
        return p

    def insert(self, point):
        #An to point periexetai mesa sta oria
        if (not self.boundary.contains(point)):
            return False

        #An to sinolo ton points den exei 3eperasei to capacity KAI DN EXEI DIERETHEI TO QUADTREE POY BRISKESAI prosthese to
        if (len(self.points) < self.capacity and self.divided == False):
            self.points.append(point)
            return True
        else:
            if (not self.divided):
                self.subdivide()
            if (self.northeast.insert(point)):
                return True
            elif (self.northwest.insert(point)):
                return True
            elif (self.southeast.insert(point)):
               return True
            elif (self.southwest.insert(point)):
                return True
    
    def delete(self, point):
        if not self.divided:
            sum = 0
            for x in range(len(self.points)):
                if point.x == self.points[x].x :
                    self.points.pop(sum)
                    break
                sum = sum + 1
            sum = 0
        else:
            self.northwest.delete(point)
            self.northeast.delete(point)
            self.southeast.delete(point)
            self.southwest.delete(point)
        self.PatchFixer()
            
            
    def PatchFixer(self):
        if self.divided:
            n1 = self.northeast.PatchFixer()
            n2 = self.northwest.PatchFixer()
            n3 = self.southwest.PatchFixer()
            n4 = self.southeast.PatchFixer()
            
            sum = n1 + n2 + n3 + n4
            if sum == self.capacity:
                self.divided = False
                p = []
                k = self.northwest.PopAndInsert(p)
                if k: 
                    for x in range(len(k)): p.append(k.pop())
                k = self.northeast.PopAndInsert(p)
                if k: 
                    for x in range(len(k)): p.append(k.pop())
                k = self.southeast.PopAndInsert(p)
                if k: 
                    for x in range(len(k)): p.append(k.pop())
                k = self.southwest.PopAndInsert(p)
                if k: 
                    for x in range(len(k)): p.append(k.pop())
                for x in range(len(p)):
                    self.insert(p.pop())
            return sum
        else:
            return len(self.points)


    def query(self, distRec, found):
        if not found :
            found = []
        if not self.boundary.intersects(distRec) :
            return
        else :
            for p in self.points :
                if distRec.contains(p) :
                    found.append(p)
            if (self.divided) :
                k = self.northwest.query(distRec, found)
                if k: 
                    for x in range(len(k)): found.append(k.pop())
                k = self.northeast.query(distRec, found)
                if k: 
                    for x in range(len(k)): found.append(k.pop())
                k = self.southwest.query(distRec, found)
                if k: 
                    for x in range(len(k)): found.append(k.pop())
                k = self.southeast.query(distRec, found)
                if k: 
                    for x in range(len(k)): found.append(k.pop())
        return found


def searchPatch(qtree, ax):
    ax.add_patch(patches.Rectangle((qtree.boundary.xL, qtree.boundary.yL), qtree.boundary.width, qtree.boundary.height, fill=False))
    if qtree.divided :
        searchPatch(qtree.northeast, ax)
        searchPatch(qtree.northwest, ax)
        searchPatch(qtree.southeast, ax)
        searchPatch(qtree.southwest, ax)


def ploting(option, root, rect):

    fig = plt.figure(figsize=(12, 8))
    plt.title("Quadtree")
    plt.axis([0, val, 0, val])
    ax = fig.add_subplot(111)
    searchPatch(root, ax)
    if option == 2: ax.add_patch(patches.Rectangle((rect.xL, rect.yL), rect.width, rect.height, fill=False, edgecolor = 'g')) 
    plt.plot(xList, yList, 'ro')
    plt.show()

val = int(input("Prosdioriste to megethos NxN toy kamba: "))
firstRec = Rect(0, 0, val, val)
k = int(input("Prosdioriste to orio shmeiwn se ena tetragwno: "))
root = QuadTree(firstRec, k)
option =  int(input("MENU\nDie3agwgi peiramatos me:\n1)Tyxaia stoixeia\n2)Sygkekrimena stoixeia\n"))
xList = []
yList = []
if option == 1:
    num = int(input("Arithmos shmeiwn peiramatos: "))
    start = time.time()
    for x in range(num):
        p = Point(round(random.uniform(0, val), 2), round(random.uniform(0, val), 2)) #shmeia apo to 0 ws to val(max diastash)
        xList.append(p.x)
        yList.append(p.y)
        root.insert(p)
    ploting(0, root, 0)
else:
    pass


while True:
    distRec = 0
    option1 =  int(input("MENU\nEnergeies:\n1)Eisagwgh stoixeioy\n2)Anazhthsh stoixeiwn apo ena allo se mia sigkekrimenh apostash\n3)Diagrafi stoixioy\n4)EXIT\n"))
    if option1 == 1:
        point_x = float(input("Dwste thn sintetagmeni X toy stoixeioy "))
        point_y = float(input("Dwste thn sintetagmeni Y toy stoixeioy "))
        p = Point(point_x, point_y)
        xList.append(p.x)
        yList.append(p.y)
        root.insert(p)
    elif option1 == 2:
        for x in range(len(xList)):
            print('{})[{},{}] '.format(x, xList[x], yList[x]))
        
        choose = int(input("Diale3e to shmeio apo to opoio the na breis apostasteis se alla: "))
        p = Point(xList[choose], yList[choose])

        dist = int(input("Posoi apostasth apo to shmeio? "))
        distRec = Rect(xList[choose] - dist, yList[choose] - dist, 2 * dist, 2 * dist)
        fpoints = []
        dpoints = root.query(distRec, fpoints)
        for p in range(len(dpoints)):
            print("[{},{}]".format(dpoints[p].x, dpoints[p].y))

    elif option1 == 3:
        for x in range(len(xList)):
            print('{})[{},{}] '.format(x, xList[x], yList[x]))
        
        choose = int(input("Diale3e to shmeio poy tha diagrafei: "))
        p = Point(xList[choose], yList[choose])
        
        root.delete(p)
        xList.pop(choose)
        yList.pop(choose)
    else:
        break
    ploting(option1, root, distRec)



