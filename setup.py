from setuptools import setup, find_packages

setup(
	name='codecolab',
	scripts=["scripts/codecolab"],
	version='0.1',
	author='Samuel Christlie',
	description='CodeColab - Run VSCode on Colab!',
	url="https://github.com/samuelchristlie/codecolab",
	packages=find_packages(),
	install_requires=[
		"pycloudflared",
	],
	platforms=["linux", "unix"],
)