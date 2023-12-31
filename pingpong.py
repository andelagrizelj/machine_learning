import pygame
from random import uniform
import numpy as np

""" 
Setup for ping-pong game taken from Prof. Dr. Jörn Fischer:
https://services.informatik.hs-mannheim.de/~fischer/lectures/MLE_Files/PingPong.py 
"""

class QLearningPingPong:
    def __init__(self, space_x, space_y, actions_num, learning_rate, discount_factor, exploration_prob):
        self.space_x = space_x
        self.space_y = space_y
        self.state_space_size = space_x * space_y * 2 * 2 * 9
        self.action_space_size = actions_num
        self.learning_rate = learning_rate # alpha
        self.discount_factor = discount_factor # gamma
        self.exploration_prob = exploration_prob # epsilon

        self.q_values = np.array([[uniform(-0.1, 0.1) for _ in range(self.action_space_size)] for _ in range(self.state_space_size)])

    def select_action(self, state):
        """
        Nächste Action mit Epsilon Greedy auswählen
        :param state: Aktueller Zustand
        :return: Index der nächsten action
        """
        # Wenn random Zahl (0-1) kleiner als Epsilon ist, dann wähle eine random action aus
        # wenn nicht, dann wähle eine action mit der maximalen W-keit aus
        e_prob = np.random.rand()
        if e_prob < self.exploration_prob:
            return np.random.choice(self.action_space_size)
        else:
            #Greedy case
            return np.argmax(self.q_values[state, :])

    def update_q_values(self, state, action, reward, next_state):
        """
        Aktualisierung der Q-Values Matrix
        :param state: Aktueller Zustand
        :param action: Ausgewählte action, die durchgeführt wurde
        :param reward: Belohnung für die action (0, -1 oder 1)
        :param next_state: Nächster Zustand, nach der action
        """
        # Q-value mit Bellmansches Optimalitätsprinzip
        self.q_values[int(state), action] += self.learning_rate * (reward + self.discount_factor * np.max(self.q_values[int(next_state), :]) - self.q_values[int(state), action])


    def get_state (self, X, Max):
        """
        :param X: diskretisierte Koordinaten für Zustand s: Xball, Yball, Xgeschw, Ygeschw, Yschläger
        :param Max: maximale Werten für Xball, Yball, Xgeschw, Ygeschw, Yschläger
        :return: Zustand s
        """
        s = X[0]
        for i in range(1,len(X)):
            s = s*Max[i] + X[i]
        return s

if __name__ == '__main__':

    pygame.init()
    screen = pygame.display.set_mode((240, 260))
    pygame.display.set_caption("Ping-Pong")

    # Q-Learning Agent  mit Epsilon-Greedy
    q_learning_agent = QLearningPingPong(space_x=11, space_y=12, actions_num=2, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.1)

    # Max = [ball_x, ball_y, |geschwindigkeit_x|, |geschwindigkeit_y|, schläger_x]
    Max = [11, 12, 2, 2, 8]

    x_racket = 1 # 0 bis 8 = 9 Felder
    x_ball = 1
    y_ball = 1
    vx_ball = 1
    vy_ball = 1
    clock = pygame.time.Clock()
    continueGame = True
    score = 0
    counter = 1
    state = x_ball * y_ball

    while continueGame:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                continueGame = False

        #if counter > 30000 or counter % 1000 == 0:
        font = pygame.font.SysFont("arial", 20)
        text = font.render("score:" + str(score), True, (255, 255, 255))
        textrect = text.get_rect()

        text2 = font.render("games:" + str(counter), True, (255, 255, 255))
        textrect2 = text2.get_rect()

        textrect.left = 20
        textrect2.left = 255-140

        screen.fill((0, 0, 0))

        screen.blit(text, textrect)
        screen.blit(text2, textrect2)
        pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x_racket * 20, 250, 80, 10))
        pygame.draw.rect(screen, (255, 100, 0), pygame.Rect(x_ball * 20, y_ball * 20, 20, 20))

        x_ball = x_ball + vx_ball
        y_ball = y_ball + vy_ball

        X = [x_ball, y_ball, (vx_ball + 1) / 2, (vy_ball + 1) / 2, x_racket]

        if x_ball > 10 or x_ball < 1:
            vx_ball *= -1
        if y_ball > 11 or y_ball < 1:
            vy_ball *= -1

        # Wähle eine Aktion aus (mit epsilon greedy)
        action = q_learning_agent.select_action(int(state))

        # Get new state
        next_state = q_learning_agent.get_state(X, Max)

        # Führe Aktion aus:
        if action == 0 and x_racket > 0:
            # Move racket to the left
            x_racket -= 1
        elif action == 1 and x_racket < 8:
            # Move racket to the right
            x_racket += 1

        # Berechne die Belohnung:
        reward = 0
        if y_ball == 12:
            if (x_ball >= x_racket and x_ball <= x_racket + 4):
                score = score + 1
                reward = +1
                counter += 1
            else:
                score = score - 1
                reward = -1
                counter += 1

        # Aktualisiere Q-values (anhand state, next_state, action und reward)
        q_learning_agent.update_q_values(state, action, reward, next_state)

        # Aktualisiere State für nächsten Schritt
        state = next_state
        # if counter > 30000 or counter % 1000 == 0:
        pygame.display.flip()
        clock.tick(60)  # Refresh-Zeiten festlegen 60 FPS