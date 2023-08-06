"""Projects module.

A Project represent a program that the user has to produce to complete
exercises for challenges.
"""

# Standard Library
import glob
import os
import subprocess
from typing import Any, Optional

def bash_position() -> str:
  args = ['command -v bash']
  return subprocess.check_output(
    args,
    encoding='locale',
    shell=True,
    stderr=subprocess.STDOUT,
  )

def bash_installation(**kwargs) -> bool:
  """Check bash installation.

  Run a check on current system for an installed bash. If bash is not installed,
  Projects targetting this platform could not be executed. Using the POSIX
  standard command *command* make us more cross-platform. Look at this page for
  more info https://pubs.opengroup.org/onlinepubs/9699919799/utilities/command.html.

  This method can be moved to a plugin for *bash* language.
  """
  verbose = 'verbose' in kwargs and kwargs['verbose']

  bash = bash_position()
  if not bash:
    print('Bash not installed. You cannot run bash based projects.')
  elif verbose:
    print(f'Found bash {str(bash)}')

  return bash

def bash_run(**kwargs) -> tuple[int, str]:
  """Run bash project.

  This method can be moved to a plugin for *bash* language.
  """
  verbose = 'verbose' in kwargs and kwargs['verbose']
  bash_pos = bash_position().rstrip('\n')
  try:
    args = ['./bash/program.sh']
    program = subprocess.run(
      args,
      capture_output=True,
      check=False,
      shell=True,
      executable=bash_pos,
    )
    return (program.returncode, str(program.stdout, 'utf-8'))
  except PermissionError as perm:
    if verbose:
      print(f'Permission Error executing bash project: {perm}')
    return (-1, '')

def dotnet_installation(**kwargs):
  """Check the dotnet installation."""
  verbose = 'verbose' in kwargs and kwargs['verbose']
  args = ['dotnet --version']
  dotnet = subprocess.check_output(
    args,
    encoding='UTF-8',
    shell=True,
    stderr=subprocess.STDOUT,
  )
  if dotnet is False:
    if verbose:
      print(f'Dotnet version not correctly installed {dotnet}')

    return False

  if verbose:
    print(f'Dotnet version found: {dotnet}')

  return True

def dotnet_run(**kwargs) -> tuple[int, str]:
  """Run dotnet project."""
  verbose = 'verbose' in kwargs and kwargs['verbose']
  try:
    # Get *.csproj project file to run.
    folder_name = 'csharp'
    proj_name = 'csharp'
    proj = glob.glob(os.path.join(folder_name, f'{proj_name}.csproj'))
    if len(proj) != 1:
      return (-2, '')

    args = ['dotnet', 'run', '--project', proj[0]]
    program = subprocess.run(
      args,
      capture_output=True,
      check=False,
    )
    return (program.returncode, program.stdout.decode('utf-8'))
  except PermissionError as perm:
    if verbose:
      print(f'Permission error: {perm}')
    return (-1, '')

known_languages = {
  'bash': {
    'version': bash_installation,
    'run': bash_run,
  },
  'csharp': {
    'version': dotnet_installation,
    'run': dotnet_run,
  },
}

class Project():
  """Define a Project."""
  language: str

  def __init__(
    self,
    language: str,
  ) -> None:
    """Creates a new Project instance.

    Creates a new Project instance checking that language given is in known
    languages array.

    Args:
      language (str): programming language supported

    Raises:
      ValueError: Thrown when invoking without a language
      ValueError: Thrown when giving a not known language
    """
    if not language:
      raise ValueError('Expected language for each project defined.')

    if not language in known_languages:
      raise ValueError(f'Language {language} is not supported by codechecker')

    super().__init__()

    self.language = language

  def __repr__(self) -> str:
    return f'{self.__class__.__name__}(language={self.language})'

  def dump(self) -> dict[str, Any]:
    """Dump the project to a dictionary.

    Dump all project data to a dictionary for a better yaml handling.

    Returns:
      dict[str, Any]: dictionary dumped.
    """
    result: dict = {}
    valued = [(k,v) for k, v in self.__dict__.items() if v]
    for key, value in valued:
      result[key] = value

    return result

  def version(self, **kwargs) -> bool:
    """Check if required tools are installed in the current machine.

    Returns:
      bool: True if tools are installed, false otherwise.
    """
    return known_languages[self.language]['version'](**kwargs)

  def run(self, contents, **kwargs) -> tuple[int, str]:
    """Execute the project with kwargs arguments.

    Args:
      contents (list): List of contents to give to command.

    Returns:
      tuple[int, str]: points and message.
    """
    verbose = 'verbose' in kwargs and kwargs['verbose']
    if verbose:
      print(f'Run Project {self.language}')

    if not self.version(**kwargs):
      return (-1, 'Unknown version')

    return known_languages[self.language]['run'](
      contents = contents, **kwargs
    )

def get_project(kwargs) -> Optional[Project]:
  """Get a Project object from a string dictionary.

  Generate a new Project object from a string dictionary, useful to retrieve
  configuration from a YAML configuration file.
  """
  try:
    return Project(**kwargs)
  except ValueError as v_er:
    raise ValueError(f'Failed to add {kwargs}') from v_er
