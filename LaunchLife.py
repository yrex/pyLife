import life



if __name__ == '__main__':
    
    iNumRows = 100
    iNumCols = 100
    iNumSteps = 500
    
    # colourmap -> spring, summer, Set2, Set3, Accent, Blues, BrBG, BuGn, PuOr, PuRd, OrRd, Pastel1, Pastel2, Purples, bone, binary
    
    dcParams = {
        'rows': iNumRows,
        'cols': iNumCols,
        'steps': iNumSteps,
        'seedType': ('acorn', (20, 40)),
        'refreshInterval': 50,
        'colourmap': 'Set3'
    }
    
    # Create Game Of Life instance and run
    GoL = life.Life(**dcParams)
    GoL.run()