import pygame
from random import randint

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((240, 260))
    pygame.display.set_caption("Ping-Pong")

    x_racket = 0 # 0 bis 8 = 9 Felder
    x_ball = 1
    y_ball = 1
    vx_ball = 1
    vy_ball = 1
    clock = pygame.time.Clock()
    continueGame = True
    score = 0
    while continueGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continueGame = False

        font = pygame.font.SysFont("arial", 20)
        text = font.render("score:" + str(score), True, (255, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = screen.get_rect().centerx
        screen.fill((0, 0, 0))

        screen.blit(text, textrect)
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x_racket * 20, 250, 80, 10))
        pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(x_ball * 20, y_ball * 20, 20, 20))

        x_ball = x_ball + vx_ball
        y_ball = y_ball + vy_ball

        if x_ball > 10 or x_ball < 1:
            vx_ball *= -1
        if y_ball > 11 or y_ball < 1:
            vy_ball *= -1

        reward = 0
        if y_ball == 12:
            if (x_ball >= x_racket and x_ball <= x_racket + 4):
                score = score + 1
                reward = +1
            else:
                score = score - 1
                reward = -1

        pygame.display.flip()
        clock.tick(60)  # Refresh-Zeiten festlegen 60 FPS