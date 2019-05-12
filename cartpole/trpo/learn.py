import tensorflow as tf
import numpy as np
import time, os
import gym
from trpo_add import TRPO
from prior import BasePrior
from dynamics import get_linear_dynamics
from scipy.io import savemat
import datetime

class LEARNER():
        # Initialize learner
        def __init__(self, args, sess):
                self.args = args
                self.sess = sess
                [A,B] = get_linear_dynamics()
                self.prior = BasePrior(A,B)
                
                self.env = gym.make(self.args.env_name)
                self.args.max_path_length = self.env.spec.timestep_limit
                self.agent = TRPO(self.args, self.env, self.sess, self.prior)

        # Run learning algorithm
        def learn(self):
                train_index = 0
                total_episode = 0
                total_steps = 0
                all_logs = list()
                while True:
                        train_index += 1
                        start_time = time.time()
                        # Train agent
                        train_log = self.agent.train()
                        total_steps += train_log["Total Step"]
                        total_episode += train_log["Num episode"]

                        all_logs.append(train_log)
                        print(train_index)
                        print(train_log["Episode_Avg_diff"])

                        # Save results
                        if total_steps > self.args.total_train_step:
                                savemat('data12_v6_' + datetime.datetime.now().strftime("%y-%m-%d-%H-%M") + '.mat',dict(data=all_logs, args=self.args))

                                break
