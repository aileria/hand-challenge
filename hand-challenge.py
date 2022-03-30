# coding=utf8

class Parser:
    cells = [0]
    cellIndex = 0
    sequence = None
    sequenceIndex = 0
    loopStartByEnd = dict()
    loopEndByStart = dict()
    
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
        self._createLoopLookups()
    
    @property
    def cell(self):
        return self.cells[self.cellIndex]
    
    @cell.setter
    def cell(self, value):
        self.cells[self.cellIndex] = value
    
    def _createLoopLookups(self):
        loopStartIndexes = list()
        for i in range(0, len(self.sequence)):
            if self.sequence[i] == '🤜':
                loopStartIndexes.append(i)
            elif self.sequence[i] == '🤛':
                self.loopStartByEnd[i] = loopStartIndexes.pop()
                self.loopEndByStart[self.loopStartByEnd[i]] = i
                
        
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
        if self.cell == 0:
            self.sequenceIndex = self.loopEndByStart[self.sequenceIndex]
    
    def endLoop(self):
        if self.cell != 0:
            self.sequenceIndex = self.loopStartByEnd[self.sequenceIndex]  
        
    def run(self):
        while self.sequenceIndex < len(self.sequence):
            action = getattr(self, self.actions[self.sequence[self.sequenceIndex]])
            action()
            self.sequenceIndex += 1
    

if __name__ == '__main__':
    with open('input.hand', 'r') as f:
        Parser(f.read()).run()
