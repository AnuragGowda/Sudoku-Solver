from time import time

class Box:
    all_boxes = []
    unsolved = []
    horizontals = [[] for _ in range(9)]
    verticals = [[] for _ in range(9)]
    home_groups = [[] for _ in range(9)]
    current_solve = None

    def __init__(self, pos, val=None):
        self.x, self.y = pos
        self.val = val
        self.final = True if val else False
        self.home = None
        self.parent = None
        self.child = None
        self.setup()
        Box.all_boxes.append(self)
    
    @classmethod
    def generate(cls):

        # Get unsolved list
        for box in Box.all_boxes:
            if not box.val:
                cls.unsolved.append(box)
        
        # Parents and children for each box
        for boxNum in range(len(cls.unsolved[1:])):
            if boxNum - 1 > -1:
                cls.unsolved[boxNum].parent = cls.unsolved[boxNum-1]
            if boxNum + 1 < len(cls.unsolved):
                cls.unsolved[boxNum].child = cls.unsolved[boxNum+1]
        
        # Get first box
        cls.current_solve = cls.unsolved[0]

    @property
    def valid(self):
        if not self.val:
            return False
        
        # Check the digit already exists
        for box in Box.horizontals[self.y]+Box.verticals[self.x]+Box.home_groups[self.home]:
            if box.val == self.val and box != self:
                return False
        return True
    
    def setup(self):

        # Sets up info about the rows and columns
        hg = [
                [0,1,2],
                [3,4,5],
                [6,7,8]
            ]
        self.home = hg[self.y//3][self.x//3]
        Box.horizontals[self.y].append(self)
        Box.verticals[self.x].append(self)
        Box.home_groups[self.home].append(self)
    
    def increase(self):
        if self.val == 9:
            self.val = None
            if self.parent:
                Box.current_solve = self.parent
                Box.current_solve.increase()
            else:
                print('No sol')
                pg.quit()
        elif not self.val:
            self.val = 1
        else:
            self.val += 1

    @classmethod
    def show(cls):
        i = 0
        s = ''
        for box in cls.all_boxes:
            if box.val:
                s+=str(box.val)
            else:
                s+='-'
            i+=1
            if i == 9:
                print(s)
                i = 0
                s = ''

def main():

    # Draw grid
    Box.all_boxes = []
    
    x = y = 0
    with open('problems\\2.txt', 'r') as f:
        for line in f:
            for char in line.strip():
                if char.isdigit():
                    Box([x,y], int(char))
                else:
                    Box([x,y])
                x+=1
            y+=1
            x=0

    Box.generate()

    global solve
    solve = True

def update():

    if Box.current_solve.valid:
        if not Box.current_solve.child and Box.current_solve.valid:
            global solve
            solve = False
        else:
            Box.current_solve = Box.current_solve.child
    else:
        Box.current_solve.increase()   

start = time()
main()
while solve:
    update()
Box.show()
print('Solved in: ' + str(round(time()-start,3)) + ' seconds')
