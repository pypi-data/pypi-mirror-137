from setuptools import setup

setup(name='gym_csle_ctf',
      version='0.0.1',
      install_requires=['gym', 'pyglet', 'numpy', 'torch', 'docker', 'paramiko', 'stable_baselines3', 'scp',
                        'random_username', 'jsonpickle', 'Sphinx', 'sphinxcontrib-napoleon',
                        'sphinx-rtd-theme', 'csle-common', 'pyperclip'],
      author='Kim Hammar',
      author_email='hammar.kim@gmail.com',
      description='csle is a platform for evaluating and developing reinforcement learning agents for '
                  'control problems in cyber security; gym-csle-ctf implements a CTF minigame in csle',
      license='Creative Commons Attribution-ShareAlike 4.0 International',
      keywords='Reinforcement-Learning Cyber-Security',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Science/Research',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Programming Language :: Python :: 3.8'
      ]
)