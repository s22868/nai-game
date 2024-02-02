"""
Authors: Mateusz Budzyński, Igor Gutowski
dependencies:
    pip install opencv-python
    pip install gym
    pip install "gym[accept-rom-license, atari]"
    pip install stable_baselines3
    pip install stable-baselines3[extra]      # progress bar
"""
import numpy as np
import gym
from stable_baselines3 import DQN

# Dostępne akcje (FIRE, LEFT, RIGHT)
available_actions = [1, 3, 2]  # FIRE, LEFT, RIGHT

env = gym.make("ALE/Enduro-v5", render_mode="human")

# Ogranicz akcje do FIRE, LEFT, RIGHT
env.action_space.n = len(available_actions)
env.action_space.sample = lambda: np.random.choice(available_actions)

# Definiowanie modelu przy pomocy stable_baselines3
model = ""
try:
    model = DQN.load("enduro_dqn_model")
    print("Wczytano istniejący model.")
except:
    # Jeśli nie ma wcześniej wytrenowanego modelu, stwórz nowy
    model = DQN("MlpPolicy", env, buffer_size=1000, verbose=1)
    print("Stworzono nowy model.")
model = DQN("MlpPolicy", env, buffer_size=1000, verbose=1)

# Uczenie modelu
model.learn(total_timesteps=1000, progress_bar=True)
# Save the trained model
model.save("enduro_dqn_model")

total_reward = 0
vec_env = model.get_env()
obs = vec_env.reset()
while True:
    action, _ = model.predict(obs)
    obs, reward, done, info = vec_env.step(action)
    total_reward += reward

    # Wyświetlanie komunikatu przy wyprzedzeniu
    if reward > 0:
        print(f"Overtake! Current total reward: {total_reward}")

    vec_env.render()

    if done:
        print("Episode finished. Total reward: {}".format(total_reward))
        obs = vec_env.reset()
        total_reward = 0
