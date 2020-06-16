import os

def get_env_var(var_name):
    if (os.environ.get(var_name)) is not None:
        print(f"\nUsing environment variable: {var_name}")
        return os.environ.get(var_name)
    else:
        raise EnvironmentError (f"\nUnable to locate environment variable: {var_name}")

phone_number = get_env_var("PHONE_NUMBER")
