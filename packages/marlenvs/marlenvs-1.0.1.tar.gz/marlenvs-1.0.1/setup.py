from setuptools import setup, find_packages
from marlenvs import __version__

setup(
		name='marlenvs',
		version=__version__,
		author='Lukas König',
		author_email='lukasmkoenig@gmx.net',
        packages=find_packages(),
		python_requires='>=3.9',
		install_requires=['gym', 'numpy', 'wheel', 'pyglet'],
		decription="Multi-Agent Reinforcement Learning environments for gym."
	)
