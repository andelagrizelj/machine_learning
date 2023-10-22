import gym


env = gym.make("MountainCar-v0", render_mode='human')
env.reset()

done = False

while not done:
    action = 2
    new_state, reward, done, truncated, info = env.step(action)

env.close()
