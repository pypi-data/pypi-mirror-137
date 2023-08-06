from gym.envs.registration import register

__version__ = '1.0.1'

register(id='TwoStep-v0', entry_point='marlenvs.two_step_env:TwoStepEnv')
register(id='Switch-v0', entry_point='marlenvs.switch_env:SwitchEnv')
register(id='Navigation-v0', entry_point='marlenvs.navigation_env:NavigationEnv')
