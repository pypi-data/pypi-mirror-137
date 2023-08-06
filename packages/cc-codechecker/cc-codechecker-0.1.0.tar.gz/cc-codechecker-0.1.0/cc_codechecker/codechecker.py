"""Codechecker top-level functions.

Functions written in this file has to be considered our public api.
Any change to this file as to be considered a breaking change if it require
any update to other users.
"""

# Standard Library
import os
from argparse import Namespace
from typing import Optional

# Codechecker
from cc_codechecker.challenge import Challenge
from cc_codechecker.configuration import (
  Configuration,
  get_configuration,
  set_configuration,
)
from cc_codechecker.project import Project


def check(argv: Optional[Namespace] = None) -> int:
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

def init(argv: Optional[Namespace] = None) -> int:
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

def run(argv: Optional[Namespace] = None) -> int:
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
