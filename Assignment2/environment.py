# -*- coding: utf-8 -*- #
"""*********************************************************************************************"""
#   FileName     [ environment.py ]
#   Synopsis     [ environment wrapper for gym ]
#   Author       [ Ting-Wei Liu (Andi611) ]
#   Copyright    [ Copyleft(c), NTUEE, NTU, Taiwan ]
"""*********************************************************************************************"""


###############
# IMPORTATION #
###############
import gym
import numpy as np
from atari_wrapper import make_wrap_atari


class Environment(object):
	def __init__(self, env_name, args, atari_wrapper=False, test=False):
		if atari_wrapper:
			clip_rewards = not test # if not test, clip reward, else not clip reward
			self.env = make_wrap_atari(env_name, clip_rewards)
		else:
			self.env = gym.make(env_name)

		self.action_space = self.env.action_space
		# self.action_space = [1,2,3]
		self.observation_space = self.env.observation_space

		self.do_render = args.do_render

		if args.video_dir:
			self.env = gym.wrappers.Monitor(self.env, args.video_dir, force=True)

	def seed(self, seed):
		'''
		Control the randomness of the environment
		'''
		self.env.seed(seed)

	def reset(self):
		'''
		observation: np.array
			stack 4 last frames, shape: (84, 84, 4)
		'''
		observation = self.env.reset()

		return np.array(observation)


	def step(self,action):
		'''
		observation: np.array
			stack 4 last preprocessed frames, shape: (84, 84, 4)
		reward: int
			wrapper clips the reward to {-1, 0, 1} by its sign
			we don't clip the reward when testing
		done: bool
			whether reach the end of the episode?
		'''
		if not self.env.action_space.contains(action):
			raise ValueError('Ivalid action!!')

		if self.do_render:
			self.env.render()

		observation, reward, done, info = self.env.step(action)

		return np.array(observation), reward, done, info


	def get_action_space(self):
		return self.action_space


	def get_observation_space(self):
		return self.observation_space


	def get_random_action(self):
		return self.action_space.sample()

# env1 = Environment('BreakoutNoFrameskip-v0',--train)
