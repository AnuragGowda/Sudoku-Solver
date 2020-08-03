import pygame as pg

class Box(pg.sprite.Sprite):
    val_dict = {
        pg.K_1:'1',
        pg.K_2:'2',
        pg.K_3:'3',
        pg.K_4:'4',
        pg.K_5:'5',
        pg.K_6:'6',
        pg.K_7:'7',
        pg.K_8:'8',
        pg.K_9:'9'
    }
    all_boxes = []
    unsolved = []
    horizontals = [[] for _ in range(9)]
    verticals = [[] for _ in range(9)]
    home_groups = [[] for _ in range(9)]
    current_solve = None

    def __init__(self, pos, game, val=None):
        self.game = game
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.size = game.block_size
        self.image = pg.transform.scale(pg.image.load('block.png').convert(), (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = [i*game.block_size for i in pos]
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

    def clicked(self):

        # Setup the initial numbers on the grid
        if not self.game.setup:
            return 
        if pg.mouse.get_pressed()[0] and self.rect.collidepoint(pg.mouse.get_pos()):
            key_wait = True
            while key_wait:
                for event in pg.event.get():
                    if event.type == pg.KEYDOWN:
                        if event.key in Box.val_dict:
                            self.val = Box.val_dict[event.key]
                            self.final = True
                            return 
                        elif event.key == pg.K_ESCAPE:
                            return
    
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
                #print('Parent')
                Box.current_solve = self.parent
                #print(Box.current_solve.x, Box.current_solve.y)
                Box.current_solve.increase()
            else:
                print('No sol')
                pg.quit()
        elif not self.val:
            self.val = 1
        else:
            self.val += 1

    @classmethod
    def debug_show(cls):
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

class Game:

    def __init__(self):
        pg.init()
        self.block_size = 60
        self.running = True
        self.size = self.block_size*9
        self.screen = pg.display.set_mode((self.size, self.size))
        self.clock = pg.time.Clock()
        self.run_solver = False
    
    def new(self):

        self.setup = True
        self.box_init = False
        self.solved = False
        self.all_sprites = pg.sprite.Group()

        # Draw grid
        Box.all_boxes = []

        # Default
        for y in range(9):
            for x in range(9):
                Box([x, y], self)
        
        '''# Specific
        x = y = 0
        with open('1.txt', 'r') as f:
            for line in f:
                for char in line.strip():
                    if char.isdigit():
                        Box([x,y], self, int(char))
                    else:
                        Box([x,y], self)
                    x+=1
                y+=1
                x=0'''

        self.run()
    
    def run(self):
        while self.running:
            self.clock.tick(120)
            self.events()
            if self.run_solver and not self.solved:
                self.update()
            self.draw()

    def events(self):

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
            elif event.type == pg.KEYDOWN:
                key = pg.key.get_pressed()
                if event.key == pg.K_r:
                    self.new()
                elif event.key == pg.K_s:
                    self.start_time = pg.time.get_ticks()
                    print('Solving')
                    self.setup = False
                    self.run_solver = True
                    self.box_init = True
        
        # Check if a box is clicked
        if self.setup:
            for box in Box.all_boxes:
                box.clicked()
        
        if self.box_init:
            Box.generate()
            self.box_init = False

    def update(self):
        if Box.current_solve.valid:
            if not Box.current_solve.child and Box.current_solve.valid:
                self.solved = True
            else:
                #print('Child')
                Box.current_solve = Box.current_solve.child
        else:
            #print(Box.current_solve.x, Box.current_solve.y)
            Box.current_solve.increase()   
    
    def draw(self):
        self.all_sprites.draw(self.screen)

        # Loop through boxes, and if val draw      
        for box in Box.all_boxes:
            if box.val and box.final: 
                self.draw_text(str(box.val), int(self.block_size), (0,0,0), box.rect.x+box.size/2, box.rect.y+box.size/4)
            elif box.val: 
                self.draw_text(str(box.val), int(self.block_size), (255,0,0), box.rect.x+box.size/2, box.rect.y+box.size/4)
        
        if self.solved:
            print(str((pg.time.get_ticks()-self.start_time)/60000)+' minutes to solve')
            self.draw_text('Solved', int(self.block_size/3), (0,255,0), int(self.block_size/3)+4, 3)
        
        pg.display.flip()

    def draw_text(self, text, size, color, x, y, font_name = ''):
        font = pg.font.Font(pg.font.match_font(font_name), size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        self.screen.blit(text_surface, text_rect)
            
g = Game()
g.new()
pg.quit()
