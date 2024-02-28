import os
import sys

import numpy as np
from custom_observation import CustomObservationFunction
from reward import custom_waiting_time_reward

import gymnasium as gym
from stable_baselines3.dqn.dqn import DQN

if "SUMO_HOME" in os.environ:
    tools = os.path.join(os.environ["SUMO_HOME"], "tools")
    sys.path.append(tools)
else:
    sys.exit("Please declare the environment variable 'SUMO_HOME'")
import traci

from sumo_rl import SumoEnvironment

model_path = "model/dqn3"

if __name__ == "__main__":
    env = SumoEnvironment(
        net_file="grid/demo.net.xml",
        route_file="grid/demo.rou.xml",
        out_csv_name="outputs/grid-proto/dqn",
        single_agent=True,
        use_gui=True,
        num_seconds=5000,
        reward_fn=custom_waiting_time_reward,
        observation_class = CustomObservationFunction
    )

    # model = DQN(
    #     env=env,
    #     policy="MlpPolicy",
    #     learning_rate=0.001,
    #     learning_starts=0,
    #     train_freq=1,
    #     target_update_interval=500,
    #     exploration_initial_eps=0.05,
    #     exploration_final_eps=0.01,
    #     verbose=1,
    #     tensorboard_log="./logs/dqn/"
    # )
    # model.learn(total_timesteps=50000)

    # model.save(model_path)

    model = DQN.load(model_path, env=env)

    ep = 1000

    for e in range(ep):
        obs = env.reset()[0]
        truncated = False
        while not truncated:
            env.render()
            action, _ = model.predict(obs)
            obs, reward, done, truncated, info = env.step(action)
            print('Truncated', truncated)

    env.close()

    # obs = env.reset()
    # print(obs[0])

    # model.predict(obs[0])

