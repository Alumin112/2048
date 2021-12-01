import pygame
import random
from constants import COLORS
pygame.init()

class Block:
    def __init__(self, x, y, w, h, pad, val):
        self.value = val
        self.ox = x
        self.oy = y 
        self.oh = h
        self.ow = w
        self.x = x + pad
        self.y = y + pad 
        self.h = h-(2*pad)
        self.w = w-(2*pad)
        if self.value == 0:self.state = False
        else: self.state = True
    
    def add(self):
        self.value *= 2
        if self.value>0:
            self.state = True

    def assign(self, val):
        self.value = val
        if self.value>0:
            self.state = True
    
    def draw(self, screen):
        color = COLORS[self.value]
        rect = pygame.Rect(self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, color, rect)


class Grid:
    def __init__(self, size, pad, width, height, screen, end_score=2048, block_val=0):
        self.screen = screen
        self.size = size
        self.pad = pad
        self.val = block_val
        self.end_score = end_score
        block_w = width/self.size
        block_h = height/self.size
        self.grid = [[Block(block_w*col, block_h*row, block_w, block_h, pad, block_val) for col in range(self.size)] for row in range(self.size)]

    def draw(self):
        for row in self.grid:
            for block in row:
                block.draw(self.screen)
    
    def move(self):
        high = 0
        filled = True
        for row in self.grid:
            for block in row:
                if self.end_score != None and block.value >= self.end_score:return self.end(True),high
                if block.value > high: high = block.value
                if not block.state:
                    filled = False  
                    new = block
        if filled:return self.end(False),high
        new.assign(random.choice([2,2,2,2,2,2,2,2,2,2,4]))
        return False,high

    def end(self, win):
        if win: text = "YOU WON!"
        else: text = "YOU LOST"
        WINNER = pygame.font.SysFont("comicsans",100)
        drawt = WINNER.render(text,1,(255,255,255))
        self.screen.blit(drawt,(self.screen.get_width()//2-drawt.get_width()//2,self.screen.get_height()//2-drawt.get_height()//2))
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()
        return True

    def left(self):
        self.cover_up()
        self.merge()
        self.cover_up()

    def right(self):
        self.reverse()
        self.cover_up()
        self.merge()
        self.cover_up()
        self.reverse()

    def up(self):
        self.transpose()
        self.cover_up()
        self.merge()
        self.cover_up()
        self.transpose()

    def down(self):
        self.transpose()
        self.reverse()
        self.cover_up()
        self.merge()
        self.cover_up()
        self.reverse()
        self.transpose()

    def transpose(self):
        self.grid =  [[self.grid[j][i] for j in range(len(self.grid))] for i in range(len(self.grid[0]))]

    def reverse(self):
        self.grid =  [[self.grid[i][len(self.grid[0])-j-1] for j in range(len(self.grid[0]))] for i in range(len(self.grid))]
        
    def cover_up(self):
        new = [[Block(self.grid[i][j].ox,self.grid[i][j].oy,self.grid[i][j].ow,self.grid[i][j].oh,self.pad,self.val) for j in range(self.size)] for i in range(self.size)]
        for i in range(self.size):
            count = 0
            for j in range(self.size):
                if self.grid[i][j].state:
                    new[i][count].assign(self.grid[i][j].value)
                    count += 1
        self.grid = new


    def merge(self):
        for i in range(self.size):
            for j in range(self.size-1):
                if self.grid[i][j].value == self.grid[i][j+1].value and self.grid[i][j].state:
                    self.grid[i][j].add()
                    self.grid[i][j+1].assign(0)

