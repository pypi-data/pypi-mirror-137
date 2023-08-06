"""Codechecker top-level functions.

Functions written in this file has to be considered our public api.
Any change to this file as to be considered a breaking change if it require
any update to other users.
"""

# Standard Library
import argparse
import os
import sys
from textwrap import dedent
from typing import Optional

# Codechecker
from cc_codechecker.challenge import Challenge
from cc_codechecker.configuration import (
  Configuration,
  get_configuration,
  set_configuration,
)
from cc_codechecker.project import Project


def check(argv: Optional[argparse.Namespace] = None) -> int:
  """Check the current configuration.

  Try to load the current configuration to check possible errors.

  Args:
    argv (Optional[Namespace], optional):
      The argparse Namespace object. Defaults to None.

  Returns:
    int: Exit code.
  """
  conf = get_configuration(None)
  if argv and argv.verbose:
    print(conf)
  return os.EX_OK

def init(argv: Optional[argparse.Namespace] = None) -> int:
  """Initialize a new challenge.

  Initialize a new challenge by create the configuration file in the root
  directory where the toll was executed.

  Args:
    argv (Optional[Namespace], optional):
      The argparse Namespace object. Defaults to None.

  Returns:
    int: Exit code.
  """
  verbose = argv and argv.verbose
  if verbose:
    print('Initializing a new challenge')

  hidden = os.path.isfile('.codechecker.yml')
  overwrite = argv and argv.overwrite_yml
  if not overwrite and hidden:
    print('You already have a codechecker project installed')
    return os.EX_CANTCREAT

  # This is the minimal valid configuration.
  conf = Configuration(
    [Challenge(name='base')],
    [Project('bash')],
  )
  set_configuration(conf)
  if verbose:
    print('Initialization completed')

  if not os.path.isfile('README.md'):
    try:
      with open('README.md', 'w', encoding='locale') as writer:
        writer.write('# Coding Challenge')
    except OSError as os_error:
      print(f'Error during README generation {os_error}')
      return os.EX_CANTCREAT

  return os.EX_OK

def run(argv: Optional[argparse.Namespace] = None) -> int:
  """Run the coding challenge.

  Run the coding challenge, executing all challenges for all projects and
  writing a result. Return 0 if all is ok, otherwise try to return the most
  semantic error code from the context.

  Args:
    argv (Optional[Namespace], optional):
      The argparse namespace. Defaults to None.

  Returns:
    int: Exit code.
  """
  verbose = argv.verbose is True if argv else False
  configuration = get_configuration(None)
  if configuration is None:
    if verbose:
      print('Configuration file is empty, no work to do')
    return os.EX_CONFIG

  if not isinstance(configuration, Configuration):
    if verbose:
      c = configuration.__class__
      print(f'''Configuration not well formed, found {c} instead of
            cc_codechecker.configuration.Configuration''')

    return os.EX_CONFIG

  configuration.run(verbose = verbose)
  return os.EX_OK

def main():
  parser = argparse.ArgumentParser(
    description=dedent('''\
      ╭━━━╮    ╭╮   ╭━━━┳╮       ╭╮
      ┃╭━╮┃    ┃┃   ┃╭━╮┃┃       ┃┃
      ┃┃ ╰╋━━┳━╯┣━━╮┃┃ ╰┫╰━┳━━┳━━┫┃╭┳━━┳━╮
      ┃┃ ╭┫╭╮┃╭╮┃┃━┫┃┃ ╭┫╭╮┃┃━┫╭━┫╰╯┫┃━┫╭╯
      ┃╰━╯┃╰╯┃╰╯┃┃━┫┃╰━╯┃┃┃┃┃━┫╰━┫╭╮┫┃━┫┃
      ╰━━━┻━━┻━━┻━━╯╰━━━┻╯╰┻━━┻━━┻╯╰┻━━┻╯

      Manage coding challenges
      '''),
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='''run the program in verbose version, making easy following the
    program flow''')
  subparsers = parser.add_subparsers(
    title='subcommands',
    description='valid subcommands',
    help='additional help',
  )
  config_parser = subparsers.add_parser(
    'config',
    description='run a check of the challenge configuration',
    help='help you to config codechecker',
    )
  config_parser.set_defaults(func=check)
  config_parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='print the configuration read to screen',
  )
  init_parser = subparsers.add_parser(
    'init',
    description='''init a new challenge in the current directory. This command
    doesn\'t have any effect if ran in a folder with already a challenge
    configured. If you want to overwrite current configuration, see
    --overwrite-* options.''',
    help='help you create a new challenge',
  )
  init_parser.set_defaults(func=init)
  init_parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='print initialization steps to screen'
  )
  init_parser.add_argument(
    '-o',
    '--overwrite-yml',
    action='store_true',
    help='overwrite current yaml configuration file.',
  )
  run_parser = subparsers.add_parser(
    'run',
    description='run the challenge',
    help='run the coding challenge',
  )
  run_parser.set_defaults(func=run)
  run_parser.add_argument(
    '-v',
    '--verbose',
    action='store_true',
    help='print run steps to screen',
  )
  args = parser.parse_args()

  try:
    sys.exit(args.func(args))
  except AttributeError as aex:
    if 'verbose' in args and args.verbose:
      if not hasattr(args, 'func'):
        print('''You had run an unknown command. Ask for help running
              `cc_codechecker -h`''')
      else:
        print(f'Attribute exception {aex}')

    sys.exit(os.EX_NOINPUT)
  except Exception as ex: # pylint: disable=broad-except
    if 'verbose' in args and args.verbose:
      print(f'Unknown error {ex}')

    sys.exit(os.EX_CONFIG)
