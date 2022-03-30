# coding=utf8

class Parser:
    cells = [0]
    sequenceIndex = 0
    cellIndex = 0
    loopLevel = 0
    sequence = None
    
    actions = {
        '👉': 'nextCell',
        '👈': 'previousCell',
        '👆': 'increase',
        '👇': 'decrease',
        '🤜': 'startLoop',
        '🤛': 'endLoop',
        '👊': 'display'
    }
    
    def __init__(self, sequence):
        self.sequence = sequence
    
    @property
    def cell(self):
        return self.cells[self.cellIndex]
    
    @cell.setter
    def cell(self, value):
        self.cells[self.cellIndex] = value
    
    def nextCell(self):
        if self.cellIndex == len(self.cells) - 1:
            self.cells.append(0)
        self.cellIndex += 1
    
    def previousCell(self):
        self.cellIndex -= 1
    
    def increase(self):
        self.cell = (self.cell + 1) if self.cell != 255 else 0
    
    def decrease(self):
        self.cell = (self.cell - 1) if self.cell != 0 else 255
    
    def display(self):
        print(chr(self.cell), end='', flush=True)
        
    def startLoop(self):
        self.loopLevel += 1
        if self.cell == 0:
            self._moveToCurrentLoopEnd()
            self.loopLevel -= 1
    
    def endLoop(self):
        if self.cell != 0:
            self._moveToCurrentLoopStart()
        
    def _moveToCurrentLoopEnd(self):
        self._moveToSameLevelLoopLimit('🤜', '🤛', 1)
    
    def _moveToCurrentLoopStart(self):
        self._moveToSameLevelLoopLimit('🤛', '🤜', -1)
    
    def _moveToSameLevelLoopLimit(self, startSymbol, endSymbol, step):
        i = self.sequenceIndex
        currentLevel = self.loopLevel
        
        while (True):
            i += step
            if self.sequence[i] == endSymbol:
                if self.loopLevel == currentLevel:
                    break
                currentLevel -= 1
            elif self.sequence[i] == startSymbol:
                currentLevel += 1
        
        self.sequenceIndex = i
        
    def run(self):
        while self.sequenceIndex < len(self.sequence):
            action = getattr(self, self.actions[self.sequence[self.sequenceIndex]])
            action()
            self.sequenceIndex += 1
    

if __name__ == '__main__':
    parser = Parser('👉👆👆👆👆👆👆👆👆🤜👇👈👆👆👆👆👆👆👆👆👆👉🤛👈👊👉👉👆👉👇🤜👆🤛👆👆👉👆👆👉👆👆👆🤜👉🤜👇👉👆👆👆👈👈👆👆👆👉🤛👈👈🤛👉👇👇👇👇👇👊👉👇👉👆👆👆👊👊👆👆👆👊👉👇👊👈👈👆🤜👉🤜👆👉👆🤛👉👉🤛👈👇👇👇👇👇👇👇👇👇👇👇👇👇👇👊👉👉👊👆👆👆👊👇👇👇👇👇👇👊👇👇👇👇👇👇👇👇👊👉👆👊👉👆👊')
    parser.run()
