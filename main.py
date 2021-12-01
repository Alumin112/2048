import pygame
import json
from pygame.constants import K_LEFT,K_RIGHT,K_UP,K_DOWN
from classes import *
from constants import *

SCREEN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Game")
CLOCK = pygame.time.Clock()
GRID = Grid(SIZE,10,WIDTH,HEIGHT,SCREEN,ENDSCORE,BLOCKVALUE)
GRID.move()

def draw():
    SCREEN.fill(BACKGROUND)
    GRID.draw()
    pygame.display.update()

def close(move,score,time):
    s = load()
    s.append([score,move,time])
    with open("score.json","w") as f:
        json.dump(s,f,indent=4)
    quit()

def load():
    try:
        with open("score.json","r") as f:
            score = json.load(f)
    except FileNotFoundError:
        f = open("score.json","w")
        f.close()
        score = []
    except json.decoder.JSONDecodeError:
        score = []
    finally:
        return score

def main():
    move = 0
    score = 0
    time = 0
    m = False
    while True:
        CLOCK.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                close(move,score,time)
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()
                if keys[K_LEFT]:
                    GRID.left()
                    m = True
                elif keys[K_RIGHT]:
                    GRID.right()
                    m = True
                elif keys[K_UP]:
                    GRID.up()
                    m = True
                elif keys[K_DOWN]:
                    GRID.down()
                    m = True
        draw()
        time += 1
        if m:
            move += 1
            m = False
            a, score = GRID.move()
            if a:
                close(move,score,time)


if __name__ == "__main__":
    main()