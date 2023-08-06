from setuptools import setup
from marlenvs import __version__

setup(
		name='marlenvs',
		version=__version__,
		author='Lukas König',
		author_email='lukasmkoenig@gmx.net',
		python_requires='>=3.9',
		install_requires=['gym', 'numpy', 'wheel', 'pyglet'],
		decription="Multi-Agent Reinforcement Learning environments for gym."
	)
