#!/usr/bin/env python

import sys, os


class Plugin(object):

	pass


class PluginManager():


	def __init__(self):

		self.plugin_dir = os.path.dirname(__file__) + '/plugins/'

		self.plugins = []

		self._load_plugins()

		self._register_plugins()


	def _load_plugins(self):

		sys.path.append(self.plugin_dir)

		plugin_files = [filename for filename in os.listdir(self.plugin_dir) if filename.startswith('plugin') and filename.endswith('.py')]

		plugin_modules = [filename.split('.')[0] for filename in plugin_files]

		for module in plugin_modules:

			m = __import__(module)


	def _register_plugins(self):

		for subclass in Plugin.__subclasses__():

			obj = subclass()

			self.plugins.append(obj)


if __name__ == '__main__':

	p = PluginManager()
