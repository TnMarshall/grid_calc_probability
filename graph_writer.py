import numpy as np
import sys
import math
import pandas as pd

class MyCar:
    def __init__(self, prob, px, py, dir=1,probT=1, probB=1, probL=1, probR=1, probS=1):
        # All probs are from the perspective of the car
        self.dir = dir # dir 1 = up, 2 = right, 3 = down, 4 = left, any other number = you messed up
        self.prob = prob #car's prob
        self.probL = probL # left
        self.probR = probR # right
        self.probT = probT # top
        self.probB = probB # bottom
        self.probS = probS # stay
        self.px = px
        self.py = py

class MyGrid:
    def __init__(self, gridSize=1, maskPS=1, maskPT=1, maskPR=1, maskPB=1, maskPL=1):
        self.grid1 = np.zeros(shape=(gridSize,gridSize), dtype=float)
        self.grid2 = np.zeros(shape=(gridSize,gridSize), dtype=float)
        self.curGrid = 1
        self.carArray1 = []
        self.carArray2 = []
        self.maskPS = maskPS
        self.maskPT = maskPT
        self.maskPR = maskPR
        self.maskPB = maskPB
        self.maskPL = maskPL


    def print(self):
        if (self.curGrid == 1):
            print(self.grid1)
        elif (self.curGrid == 2):
            print(self.grid2)
        else:
            raise Exception("An error has occured and the grid number is not right")

    def addCar(self, prob, px, py, dir=1):
        probT=self.maskPT
        probR=self.maskPR
        probB=self.maskPB
        probL=self.maskPL
        probS=self.maskPS
        newCar = MyCar(prob, px, py, dir, probT=probT,probB=probB,probR=probR,probL=probL,probS=probS)
        if (self.curGrid == 1):
            self.carArray1.append(newCar)
            self.grid1[newCar.py,newCar.px] = self.grid1[newCar.py,newCar.px] + prob

        elif (self.curGrid == 2):
            self.carArray2.append(newCar)
            self.grid2[newCar.py,newCar.px] = self.grid2[newCar.py,newCar.px] + prob

        else:
            raise Exception("An error has occured and this grid is not valid")

    def cycle(self):
        if (self.curGrid == 1):
            oldCarArr  = self.carArray1
        elif (self.curGrid == 2):
            oldCarArr  = self.carArray2
        else:
            raise Exception("An error has occured and this grid is not valid")
        
        newGrid = np.zeros(self.grid1.shape, dtype=float)
        newCarArr = []

        for i in oldCarArr:
            if (i.dir == 1):
                # follows order Stay, Top, Right, Bottom, Left
                probs = [i.prob*i.probS, i.prob*i.probT, i.prob*i.probR, i.prob*i.probB, i.prob*i.probL]
            elif (i.dir == 2):
                probs = [i.prob*i.probS, i.prob*i.probL, i.prob*i.probT, i.prob*i.probR, i.prob*i.probB]
            elif (i.dir == 3):
                probs = [i.prob*i.probS, i.prob*i.probB, i.prob*i.probL, i.prob*i.probT, i.prob*i.probR]
            elif (i.dir == 4):
                probs = [i.prob*i.probS, i.prob*i.probR, i.prob*i.probB, i.prob*i.probL, i.prob*i.probT]
            # if (i.dir == 1):
            #     # follows order Stay, Top, Right, Bottom, Left
            #     probs = [i.prob*i.probS, self.maskPT, self.maskPR, self.maskPB, self.maskPL]
            # elif (i.dir == 2):
            #     probs = [i.prob*i.probS, self.maskPL, self.maskPT, self.maskPR, self.maskPB]
            # elif (i.dir == 3):
            #     probs = [i.prob*i.probS, self.maskPB, self.maskPL, self.maskPT, self.maskPR]
            # elif (i.dir == 4):
            #     probs = [i.prob*i.probS, self.maskPR, self.maskPB, self.maskPL, self.maskPT]
            else:
                raise Exception("Improper direction")
            
            if (probs[0] != 0.0):
                newCarS = MyCar(probs[0], px=i.px, py=i.py, dir=i.dir, probT=self.maskPT, probB=self.maskPB, probL=self.maskPL, probR=self.maskPR, probS=self.maskPS)
                newCarArr.append(newCarS)
            if (probs[1] != 0.0):
                newCarT = MyCar(probs[1], px=i.px, py=i.py-1, dir=1, probT=self.maskPT, probB=self.maskPB, probL=self.maskPL, probR=self.maskPR, probS=self.maskPS)
                newCarArr.append(newCarT)
            if (probs[2] != 0.0):
                newCarR = MyCar(probs[2], px=i.px+1, py=i.py, dir=2, probT=self.maskPT, probB=self.maskPB, probL=self.maskPL, probR=self.maskPR, probS=self.maskPS)
                newCarArr.append(newCarR)
            if (probs[3] != 0.0):
                newCarB = MyCar(probs[3], px=i.px, py=i.py+1, dir=3, probT=self.maskPT, probB=self.maskPB, probL=self.maskPL, probR=self.maskPR, probS=self.maskPS)
                newCarArr.append(newCarB)
            if (probs[4] != 0.0):
                newCarL = MyCar(probs[4], px=i.px-1, py=i.py, dir=4, probT=self.maskPT, probB=self.maskPB, probL=self.maskPL, probR=self.maskPR, probS=self.maskPS)
                newCarArr.append(newCarL)

        for car in newCarArr:
            newGrid[car.py,car.px] = newGrid[car.py,car.px] + car.prob

        if (self.curGrid == 1):
            self.curGrid = 2
            self.carArray2 = newCarArr
            self.grid2 = newGrid
        elif (self.curGrid == 2):
            self.curGrid = 1
            self.carArray1 = newCarArr
            self.grid1 = newGrid

    def get_cur_grid(self):
        if (self.curGrid == 1):
            gridOut = self.grid1
        elif (self.curGrid == 2):
            gridOut = self.grid2
        else:
            raise Exception("An error has occured and this grid is not valid")
        return gridOut
        

if __name__ == "__main__":
    # if (len(sys.argv) == 3):
    #     gridSize = int(sys.argv[1])
    #     numCycles = int(sys.argv[2])
    # else:
    #     gridSize = 9
    gridSize = 9
    myGrid = MyGrid(gridSize=gridSize, maskPB=0, maskPL=0.1, maskPR=0.3, maskPS=0.4, maskPT=0.2)

    myGrid.addCar(prob=1,px=math.ceil(float(gridSize)/2.0)-1,py= math.ceil(float(gridSize)/2.0)-1,dir=1)
    # for i in range(numCycles):
    #     myGrid.cycle()


    ## Testing

    gridc0 = np.zeros((9,9),dtype=float)
    gridc0[4,4] = 1

    print("\n\n")
    if (np.array_equal(myGrid.grid1, gridc0)):
        print("Grid matches after C0")
    else:
        print("Grid does not match after C0")

    myGrid.cycle()

    gridc1 = np.zeros((9,9),dtype=float)
    gridc1[4,4] = 0.4
    gridc1[3,4] = 0.2
    gridc1[4,3] = 0.1
    gridc1[5,4] = 0.0
    gridc1[4,5] = 0.3

    if (np.array_equal(myGrid.grid2, gridc1)):
        print("Grid matches after C1")
    else:
        print("Grid does not match after C1")

    myGrid.print()

    myGrid.cycle()

    gridc2 = np.zeros((9,9),dtype=float)
    gridc2[4,4] = 0.4 * 0.4
    gridc2[3,4] = 0.2*0.4 + 0.4*0.2
    gridc2[4,3] = 0.1*0.4 + 0.4*0.1
    gridc2[5,4] = 0.0 + 0.0*4.0
    gridc2[4,5] = 0.3*0.4 + 0.3*0.4
    
    gridc2[3,3] = 0.1*0.3 + 0.2*0.1
    gridc2[5,3] = 0.1*0.1
    gridc2[5,5] = 0.0 + 0.3*0.3
    gridc2[2,4] = 0.2*0.2
    gridc2[4,2] = 0.1*0.2
    gridc2[4,6] = 0.3*0.2
    gridc2[3,5] = 0.2*0.3 + 0.3*0.1

    if (np.array_equal(myGrid.grid1, gridc2)):
        print("Grid matches after C2")
    else:
        print("Grid does not match after C2")

    myGrid.print()
    print(gridc2)
    print("SUM: " + str(np.sum(np.sum(myGrid.grid1))))

    ## Output theoretical correct graph
    gridSize=21
    finalGraph = MyGrid(gridSize=gridSize, maskPB=0, maskPL=0.1, maskPR=0.3, maskPS=0.4, maskPT=0.2)
    finalGraph.addCar(prob=1,px=math.ceil(float(gridSize)/2.0)-1,py= math.ceil(float(gridSize)/2.0)-1,dir=1)
    numCycles = 10
    for i in range(numCycles):
        finalGraph.cycle()

    print("\n\n")
    print(finalGraph.get_cur_grid())
    print("FINAL SUM: " + str(np.sum(np.sum(finalGraph.get_cur_grid()))))

    # convert array into dataframe
    DF = pd.DataFrame(finalGraph.get_cur_grid())
 
# save the dataframe as a csv file
    DF.to_csv("graph_" + str(numCycles) + "_cycles.csv")