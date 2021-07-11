import pygame


def initialize():
    pygame.init()
    win = pygame.display.set_mode((400,400))

def getKey(keyName):
    ans = False
    for eve in pygame.event.get(): pass
    keyInput = pygame.key.get_pressed()
    myKey = getattr(pygame,'K_{}'.format(keyName))
    if keyInput[myKey]:
        ans = True
    pygame.display.update()

    return ans

def main():
    if getKey('w'):
        print("Forward")
    elif getKey('s'):
        print("Backward")

if __name__ == "__main__":
    initialize()
    while True:
        main()
