import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import matplotlib.cm as cm
import scipy.signal as sp



class Life:
    
    """
    Class Life - A Game Of Life implementation.
    There are several parameters that can be modified when the instance is initialised.
    
    rows: number of rows in the grid
    cols: number of columns in the grid
    steps: number of steps in the simulation
    seedType: select from various grid initial states
    refreshInterval: animation refresh rate (in miliseconds)
    colourmap: choice of matplotlib colourmaps
    
    """
    
    def __init__(self, **kwargs):

        self.rows = kwargs['rows']
        self.cols = kwargs['cols']
        self.steps = kwargs['steps']
        
        self.seedType = kwargs.get('seedType')
        self.refreshInterval = kwargs.get('refreshInterval') # in miliseconds
        self.colourmap = kwargs.get('colourmap')
        
        # keep track of steps
        self.counter = 0
        
        # set default animation interval if value is not set by user
        if not self.refreshInterval:
            self.refreshInterval = 500 # miliseconds
        
        # set default colourmap if value is not set by user
        if not self.colourmap:
            self.colourmap = 'binary'
        
        # pattern dictionary, for class use
        # the mixed pattern is not included
        self._dcPatterns = {
            1: 'random',
            2: 'glider',
            3: 'acorn',
            4: 'B-heptomino',
            5: 'Gosper glider gun'
        }
        
        

        # Initialise grid
        if self.seedType:
            
            self.grid = self.generatePattern(self.seedType[0], self.seedType[1])
                
        else:
            self.initGrid_default()
        
        
        # close any open plots
        plt.close()


    def updateLife(self):
        
        # The rules of the Game Of Life
        
        # step 1 is initial state
        if self.counter > 1:

            # Mask used for 2D convolution
            mask = np.array([ [1,1,1],[1,0,1],[1,1,1] ], dtype=int)
        
            neighbours = sp.convolve2d(self.grid,mask,mode='same')
        
            # Apply the Game Of Life rules
            self.grid_prev = self.grid
            self.grid = ((self.grid[:,:] == 0) * (neighbours[:,:] == 3)) + ((self.grid[:,:] == 1) * (neighbours[:,:] == 2)) + \
                ((self.grid[:,:] == 1) * (neighbours[:,:] == 3))
        
            # results are now in boolean, convert back to int
            self.grid = self.grid.astype(int)
        
        # update step counter
        self.counter += 1


    def generatePattern(self, PatternType, PatternArgs):
        
        # used for internal pattern generation
        if type(PatternType) == int:
            selectedPattern = self._dcPatterns[PatternType]
            print(selectedPattern)
        else:
            selectedPattern = PatternType
        
        
        if selectedPattern == 'random':
            localGrid = self.initGrid_random(*PatternArgs)

        elif selectedPattern == 'glider':
            localGrid = self.initGrid_glider(*PatternArgs)
        
        elif selectedPattern == 'acorn':
            localGrid = self.initGrid_acorn(*PatternArgs)
        
        elif selectedPattern == 'B-heptomino':
            localGrid = self.initGrid_bhepto(*PatternArgs)
        
        elif selectedPattern == 'Gosper glider gun':
            localGrid = self.initGrid_gosperglidergun(*PatternArgs)
            
        elif selectedPattern == 'Mixed Pattern':
            localGrid = self.initGrid_mixedpatterns(*PatternArgs)
        
        else:
            localGrid = self.initGrid_default()
        
        return localGrid
    
    
    def initGrid_random(self, *args):
        
        # 'random': randomly generate live cells
        # self.seedType = ('random', numLiveCells)
        
        
        if len(args) < 1:
            iTotalCells = self.rows * self.cols
            iNumLiveCells = np.random.random_integers(iTotalCells/16, iTotalCells/8)
        else:
            iNumLiveCells = args[0]
        
        x_vals = np.random.random_integers(0, self.rows-1, iNumLiveCells)
        y_vals = np.random.random_integers(0, self.rows-1, iNumLiveCells)
        localGrid = np.zeros( (self.rows, self.cols), dtype=int)
        localGrid[x_vals,y_vals] = 1
        
        return localGrid
    
    
    def initGrid_mixedpatterns(self, *args):
        
        # 'Mixed Pattern: populate the grid using a mixture of patterns
        # self.seedType('Mixed Pattern', NumPatterns)
        
        # create blank grid
        localGrid = np.zeros( (self.rows, self.cols), dtype=int)
        
        # generate random patterns
        iNumPatterns = args[0]
        lsPatterns = np.random.random_integers(1,len(self._dcPatterns), iNumPatterns)
        
        for iPatNum in lsPatterns:
            # numpy.int64 -> int
            intPat = int(iPatNum)
            tempGrid = self.generatePattern(intPat, [])
            localGrid = ( (localGrid == 1) + (tempGrid == 1) ).astype(int)
        
        return localGrid
    
        
    def initGrid_glider(self, *args):
        
        # 'glider': generate a glider at a specified location
        # self.seedType = ('glider', (xLoc, yLoc))
        
        if len(args) < 2:
            xLoc = np.random.random_integers(2, (self.rows-1)*2/3 )
            yLoc = np.random.random_integers(0, (self.cols-1)*2/3 )
        else:
            xLoc, yLoc = args
            
                    
        localGrid = np.zeros( (self.rows, self.cols), dtype=int)
        # xLoc, yLoc = self.seedType[1]
        localGrid[xLoc, yLoc] = 1
        localGrid[xLoc, yLoc + 1] = 1
        localGrid[xLoc, yLoc + 2] = 1
        localGrid[xLoc - 1, yLoc + 2] = 1
        localGrid[xLoc - 2, yLoc + 1] = 1
        
        return localGrid
    
        
    def initGrid_acorn(self, *args):
        
        # 'acorn': generate an acorn pattern at a specified location
        # self.seedType = ('acorn', (xLoc, yLoc))
        
        if len(args) < 2:
            xLoc = np.random.random_integers(2, (self.rows-1)*2/3 )
            yLoc = np.random.random_integers(0, (self.cols-1)*2/3 )
        else:
            xLoc, yLoc = args
        
        localGrid = np.zeros( (self.rows, self.cols), dtype=int)
        # xLoc, yLoc = self.seedType[1]
        localGrid[xLoc, yLoc] = 1
        localGrid[xLoc, yLoc + 1] = 1
        localGrid[xLoc, yLoc + 4] = 1
        localGrid[xLoc, yLoc + 5] = 1
        localGrid[xLoc, yLoc + 6] = 1
        localGrid[xLoc - 1, yLoc + 3] = 1
        localGrid[xLoc - 2, yLoc + 1] = 1
        
        return localGrid
    
        
    def initGrid_bhepto(self, *args):
        
        # 'B-heptomino': generate a B-heptomino pattern at a specified location
        # self.seedType = ('B-heptomino', (xLoc, yLoc))
        
        if len(args) < 2:
            xLoc = np.random.random_integers(2, (self.rows-1)*2/3 )
            yLoc = np.random.random_integers(0, (self.cols-1)*2/3 )
        else:
            xLoc, yLoc = args
        
        localGrid = np.zeros( (self.rows, self.cols), dtype=int)

        localGrid[xLoc, yLoc] = 1
        localGrid[xLoc, yLoc + 2] = 1
        localGrid[xLoc, yLoc + 3] = 1
        localGrid[xLoc + 1, yLoc] = 1
        localGrid[xLoc + 1, yLoc + 1] = 1
        localGrid[xLoc + 1, yLoc + 2] = 1
        localGrid[xLoc + 2, yLoc + 1] = 1
        
        return localGrid
    
    
    def initGrid_gosperglidergun(self, *args):
        
        # 'Gosper glider gun': generate a Gosper Glider Gun pattern at a specified location
        # self.seedType = ('Gosper glider gun', (xLoc, yLoc))
        
        if len(args) < 2:
            xLoc = np.random.random_integers(5, (self.rows-1)*2/3 )
            yLoc = np.random.random_integers(0, (self.cols-1)/2 )
        else:
            xLoc, yLoc = args
        
        localGrid = np.zeros( (self.rows, self.cols), dtype=int)

        # start from Block pattern
        localGrid[xLoc, yLoc] = 1
        localGrid[xLoc, yLoc + 1] = 1
        localGrid[xLoc+ 1, yLoc] = 1
        localGrid[xLoc + 1, yLoc + 1] = 1
        
        localGrid[xLoc, yLoc + 10] = 1
        localGrid[xLoc + 1, yLoc + 10] = 1
        localGrid[xLoc + 2, yLoc + 10] = 1
        
        localGrid[xLoc - 1, yLoc + 11] = 1
        localGrid[xLoc + 3, yLoc + 11] = 1
        
        localGrid[xLoc - 2, yLoc + 12] = 1
        localGrid[xLoc - 2, yLoc + 13] = 1
        localGrid[xLoc + 4, yLoc + 12] = 1
        localGrid[xLoc + 4, yLoc + 13] = 1
        
        localGrid[xLoc + 1 , yLoc + 14] = 1
        
        localGrid[xLoc - 1, yLoc + 15] = 1
        localGrid[xLoc + 3, yLoc + 15] = 1

        localGrid[xLoc, yLoc + 16] = 1
        localGrid[xLoc + 1, yLoc + 16] = 1
        localGrid[xLoc + 2, yLoc + 16] = 1
        
        localGrid[xLoc + 1, yLoc + 17] = 1
        
        localGrid[xLoc, yLoc + 20] = 1
        localGrid[xLoc, yLoc + 21] = 1
        localGrid[xLoc - 1, yLoc + 20] = 1
        localGrid[xLoc - 1, yLoc + 21] = 1
        localGrid[xLoc - 2, yLoc + 20] = 1
        localGrid[xLoc - 2, yLoc + 21] = 1
        
        localGrid[xLoc - 3, yLoc + 22] = 1
        localGrid[xLoc + 1, yLoc + 22] = 1
        
        localGrid[xLoc - 3, yLoc + 24] = 1
        localGrid[xLoc - 4, yLoc + 24] = 1
        localGrid[xLoc + 1, yLoc + 24] = 1
        localGrid[xLoc + 2, yLoc + 24] = 1
        
        localGrid[xLoc - 1, yLoc + 34] = 1
        localGrid[xLoc - 1, yLoc + 35] = 1
        localGrid[xLoc - 2, yLoc + 34] = 1
        localGrid[xLoc - 2, yLoc + 35] = 1
        
        return localGrid

        
    
    def initGrid_default(self):
        
        # populate the grid with 0s and 1s. The ratio is not controlled.
        return np.random.random_integers(0,1, (self.rows, self.cols))
    
    
    

    def gridUpdate(self, iStepNum):
        # Update the grid based on the Game Of Life rules
        self.updateLife()
        
        # print('Step ' + str(iStepNum))
        
        # update the plot
        temp = self.mat1.set_data(self.grid)
        plt.title('Step ' + str(iStepNum))
                
        return temp
    
    
    def run(self):
        
        # intialise figure
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_xticklabels([])
        self.ax1.set_yticklabels([])
        self.ax1.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off')
        
        # intialise matshow
        self.mat1 = self.ax1.matshow(self.grid, cmap = plt.get_cmap(self.colourmap))
        
        # create animation
        self.anim = animation.FuncAnimation(self.fig1, self.gridUpdate, frames = range(0,self.steps), 
                    interval=self.refreshInterval, repeat=False)
        
        # show plot
        plt.show()
            
