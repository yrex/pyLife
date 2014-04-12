import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
# import matplotlib.cm as cm
import scipy.signal as sp
import os



class Life:

    """
    Class Life - A Game Of Life implementation.
    There are several parameters that can be modified when the instance is initialised.
    
    rows: number of rows in the grid
    cols: number of columns in the grid
    steps: number of steps in the simulation
    seedType: select from various grid initial states
    refreshInterval: animation refresh rate (in milliseconds)
    colourmap: choice of matplotlib colourmaps
    
    """

    def __init__(self, **kwargs):

        self.rows = kwargs['rows']
        self.cols = kwargs['cols']
        self.steps = kwargs['steps']

        self.seedType = kwargs.get('seedType')
        self.refreshInterval = kwargs.get('refreshInterval') # in milliseconds
        self.colourmap = kwargs.get('colourmap')

        # keep track of steps
        self.counter = 0

        # set default animation interval if value is not set by user
        if not self.refreshInterval:
            self.refreshInterval = 500 # milliseconds

        # set default colourmap if value is not set by user
        if not self.colourmap:
            self.colourmap = 'binary'

        # Set directory for patterns
        self._sPatDir = 'patterns'
        self._sModuleDir = os.path.dirname(__file__)
        self._sPatDirPath = os.path.join(self._sModuleDir, self._sPatDir)

        # create a list of available pattern names
        self.patterns = dict()
        self.getPatterns()

        # Initialise grid
        if self.seedType:

            self.grid = self.generatePattern(self.seedType[0], self.seedType[1])

        else:
            self.grid = self.initGrid_random()

        # close any open plots
        plt.close()


    def updateLife(self):

        """
        The rules of the Game Of Life!
        Update the grid based on the rules

        """

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

    def getPatterns(self):

        """
        This method traverses the self._sPathDirPath directory and
        will return a list of tuples containing the name and path
        of available patterns

        """

        for (root, dirs, patFiles) in os.walk(self._sPatDirPath):

            # Traverse pattern directory and list all patterns
            for patFile in patFiles:
                # ignore hidden files
                if patFile[0] != '.':
                    PatternFilePath = os.path.join(root,patFile)
                    patternName = self.readPatternName(PatternFilePath).upper()
                    self.patterns[patternName] = PatternFilePath

        print(self.patterns)


    @staticmethod
    def readPatternName(PatFilename):

        """
        Read pattern name
        The first line contains the patter name in the form:
        !NAME: patternName

        """

        with open(PatFilename, 'r') as f:
            sPatternName = f.readline().split(':')[1].strip()

        return sPatternName


    @staticmethod
    def readPatternDef(PatFilename):

        """
        Read the pattern definition and return a numpy array

        """

        def mapTextToInt(s):
            # '.' -> 0
            # 'O' -> 1

            deadcell = '.'
            livingcell = 'O'

            if s == deadcell:
                output = 0
            elif s == livingcell:
                output = 1
            else:
                output = 0

            return output

        # extract the definition
        PatDef = list()
        with open(PatFilename, 'r') as f:
            for line in f:
                if line[0] != '!':
                    # convert text to 0s and 1s
                    currLine = [ mapTextToInt(w) for w in line.strip()]
                    PatDef.append(currLine)

        # pad all list items so that they are of equal size
        # get longest column in the definition
        max_cols = max([len(l) for l in PatDef])
        for l in PatDef:
            l += [0]* (max_cols - len(l))


        # convert definition from 2D list to numpy array
        PatDefArr = np.array(PatDef, dtype=int)

        return PatDefArr

    def generatePattern(self, PatternType, *PatternArgs):

        """
        Generate a pattern on the grid.

        PatternType of 'RANDOM' and 'MIXED PATTERN' are special to the class.
        Other patterns are read from the pattern files in the patters/ directory.

        PatternArgs contains parameters related to the chosen PatternType

        """

        print(PatternType)

        if PatternType.upper() == 'RANDOM':
            localGrid = self.initGrid_random(*PatternArgs)

        elif PatternType.upper() == 'MIXED PATTERN':
            localGrid = self.initGrid_mixedpatterns(*PatternArgs)

        else:
            localGrid = self.initGrid_fromPatternFile(PatternType, *PatternArgs)

        return localGrid


    def initGrid_random(self, *args):

        """
        'random': randomly generate live cells
        self.seedType = ('random', numLiveCells)

        """

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

        """
        'Mixed Pattern: populate the grid using a mixture of patterns
        self.seedType('Mixed Pattern', NumPatterns)

        """

        # create blank grid
        localGrid = np.zeros( (self.rows, self.cols), dtype=int)

        # generate random patterns
        iNumPatterns = args[0][0]
        # lsPatterns = np.random.random_integers(1,len(self._dcPatterns), iNumPatterns)
        lsPatterns = np.random.choice(list(self.patterns.keys()), iNumPatterns)

        for iPatName in lsPatterns:
            # numpy.int64 -> int
            # intPat = int(iPatName)
            tempGrid = self.generatePattern(iPatName)
            localGrid = ( (localGrid == 1) + (tempGrid == 1) ).astype(int)

        return localGrid

    def initGrid_fromPatternFile(self,PatternType, *args):

        """
        Update the grid using a definition stored in a pattern file

        """

        if len(args) < 1:
            xLoc = np.random.random_integers(2, (self.rows-1)*2/3 )
            yLoc = np.random.random_integers(0, (self.cols-1)*2/3 )
        else:
            xLoc, yLoc = args[0]

        # create blank grid
        localGrid = np.zeros( (self.rows, self.cols), dtype=int)

        # get pattern definition if PatternType exists
        if self.patterns.get(PatternType.upper()):

            PatDefArr = self.readPatternDef(self.patterns[PatternType.upper()])
            patRows, patCols = PatDefArr.shape
            localGrid[xLoc:xLoc + patRows, yLoc:yLoc + patCols] = PatDefArr

        else:
            print("Pattern doesn't exist")

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

        # initialise figure
        self.fig1, self.ax1 = plt.subplots()
        self.ax1.set_xticklabels([])
        self.ax1.set_yticklabels([])
        self.ax1.tick_params(axis='both', which='both', bottom='off', top='off', left='off', right='off')

        # initialise matshow
        self.mat1 = self.ax1.matshow(self.grid, cmap = plt.get_cmap(self.colourmap))

        # create animation
        self.anim = animation.FuncAnimation(self.fig1, self.gridUpdate, frames = range(0,self.steps),
                    interval=self.refreshInterval, repeat=False)

        # show plot
        plt.show()

