
import os


def load(env, default=None):
    """ utility to check if a env variable exists as a path to file """
    value = default

    env_value = os.getenv(env)

    # check if the environment exist
    if env_value is not None:
        return env_value

    # check if a env + _FILE exists
    env_value = os.getenv(env+'_FILE')

    if env_value is not None: 
        try:
            with open(env_value, 'r') as f:
                value = f.read()
        except FileNotFoundError:
            pass

    return value


