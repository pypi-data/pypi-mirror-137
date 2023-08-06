# coding=utf8

from time import sleep
from os.path import isfile

# Quick and dirty tool to compare two environment files for new, missing, mismatches
# This is a devops tool to check for changes in environment variable configurations
# This is not to inspect runtime environment variables

# Not case-sensitive names
common_env_names = ['env', 'environment']
common_env_names = common_env_names + [f'.{name}' for name in common_env_names]
found_envs = set()

# check local path to find common env files
for common_env_name in common_env_names + [f'.{name}' for name in common_env_names]:
  if isfile(common_env_name):
    found_envs.add(common_env_name)

def parse_env_to_dict(env_file):
  env_dict = {}
  with open(env_file, 'r') as env_f:
    # Split into lines
    lines = env_f.read().splitlines()
    lines = [line for line in lines if 
      # Remove strippable lines
      line.strip() 
      # Remove comment lines
      and line[0] != '#'
      # Remove anything not an env assignment
      and line.count('=') == 1
      and len(line.split('=')) == 2
    ]
    # Add to dict
    for line in lines:
      line = line.split('=')
      env_dict[line[0]] = line[1]

  return env_dict

def prompt_user(message):
  print(message)
  sleep(.4)

def create_env(env_filename, extension, base_env, appending_env):
  with open(env_filename + extension, 'w') as new_env:
    # Write current environment values
    for k, v in base_env.items():
      new_env.write(f'{k}={v}\n') # <<< looks dirty
    # Write new enviroment values
    for k, v in appending_env.items():
      user_supplied_env = input(f'\nType new value or enter/return to use default\n{k}={v}\n')
      if user_supplied_env == '':
        new_env.write(f'{k}={v}\n')
      else:
        new_env.write(f'{k}={user_supplied_env}\n')

  print(f'Wrote new environment file {env_filename + extension}')

def parse_valid_env_configuration(env_filename):
  try:
    current_env_dict = parse_env_to_dict(env_filename)
    example_env_dict = parse_env_to_dict(f'{env_filename}.example')
    print(f'\nComparing {env_filename} with {env_filename}.example')

    # Find shared items
    shared_items = {k: current_env_dict[k] for k in current_env_dict if k in example_env_dict and current_env_dict[k] == example_env_dict[k]}

    # Find items in env but not in example
    old_env_items = {k: current_env_dict[k] for k in current_env_dict if k not in example_env_dict }

    # Find items in example but not in env
    new_env_items = {k: example_env_dict[k] for k in example_env_dict if k not in current_env_dict }

    for k, v in shared_items.items():
      print(k, v)

    prompt_user(f'\n🔑 👍 Found {len(shared_items)} matching')
    input('\nPress enter/return to continue...\n')

    for k, v in old_env_items.items():
      print(k, v)

    prompt_user(f'\n🔑 🚨 Found {len(old_env_items)} in environment but not in example')
    input('\nPress enter/return to continue...\n')

    for k, v in new_env_items.items():
      print(k, v)

    prompt_user(f'\n🔑 ✅ Found {len(new_env_items)} new from example')
    try:
      response = input('\nAdd new variables? [y/n]\n')
      if response[0].lower() == 'y':
        create_env(env_filename, '.new', current_env_dict, new_env_items)
      else:
        print('Exiting...')
    except Exception :
      print('Exiting...')

  except FileNotFoundError:
    pass

def main():
  if len(found_envs) >= 1:
    print('\nFound environment variable file(s)\n')
    for found_env in found_envs:
      print(found_env)

    for found_env in found_envs:
      # check for example files
      if isfile(f'{found_env}.example'):
        print(f'{found_env}.example')

    for found_env in found_envs:
      # TODO: add checks for extra unmatched pairs, more than one pair etc
      parse_valid_env_configuration(found_env)

  else:
    print('Found no environment variable files')

if __name__ == "__main__":
    main()
