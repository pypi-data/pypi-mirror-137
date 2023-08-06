"""Configuration module.

A configuration represent the complete definition of the current coding
challenge.
"""

# Standard Library
from typing import Any, Optional, Union

import yaml

# Codechecker
from cc_codechecker.challenge import Challenge, get_challenge
from cc_codechecker.project import Project, get_project

DEFAULT_OUTPUT = 'output.txt'
FILE_NAME = '.codechecker.yml'

class Configuration():
  """Define a complete configuration for code checker.

  Raises:
    ValueError: thrown if no challenges are given
    ValueError: thrown if no projects are given
  """
  challenges: list[Challenge]
  output: str = DEFAULT_OUTPUT
  projects: list[Project]

  def __init__(
    self,
    challenges: list[Challenge],
    projects: list[Project],
    output: str = DEFAULT_OUTPUT,
  ) -> None:
    if not challenges or len(challenges) < 1:
      raise ValueError('Expected at least one challenge')
    if not projects or len(projects) < 1:
      raise ValueError('Expected at least one project')

    super().__init__()

    self.challenges = challenges
    self.output = output
    self.projects = projects

  def __repr__(self) -> str:
    args: list[str] = []
    if hasattr(self, 'challenges') and self.challenges:
      c_string = ','.join(str(c) for c in self.challenges)
      args.append(f'challenges=[{c_string}]')
    if hasattr(self, 'output') and self.output != DEFAULT_OUTPUT:
      print(f'Append output: {self.output}')
      args.append(f'output:{self.output}')
    if self.projects:
      p_string = ','.join(str(p) for p in self.projects)
      args.append(f'projects=[{p_string}]')
    args_string = ','.join(args)
    return f'{self.__class__.__name__}({args_string})'

  def dump(self) -> dict[str, Any]:
    """Dump the configuration to a dictionary.

    Dump all configuration data to a dictionary for a better yaml handling.

    Returns:
      dict[str, Any]: dictionary dumped.
    """
    result: dict = {}
    challenges = [k.dump() for k in self.challenges]
    projects = [k.dump() for k in self.projects]
    result['challenges'] = challenges
    result['projects'] = projects
    excluded = ['challenges', 'projects']
    items = self.__dict__.items()
    valued = [(k,v) for k, v in items if v and k not in excluded]
    for key, value in valued:
      if key != 'output' or value != 'output.txt':
        result[key] = value

    return result

  def run(self, verbose: bool = False):
    """Run the configuration.

    Args:
      verbose (bool, optional): run in verbose mode, reporting more info on
      the stdout. Defaults to False.
    """
    score: int = 0
    for challenge in self.challenges:
      points = challenge.run(self.projects, verbose = verbose)
      score = score + points
      if verbose:
        print(f'Gained {points} points, now {score}')

    try:
      with open('score.txt', 'w', encoding='locale') as score_writer:
        score_writer.write(str(score))
    except OSError as ex:
      print(f'Exception in writing scores: {ex}')

def set_configuration(configuration: Configuration):
  """Set the configuration to yaml

  Write the .codechecker.yml file in the root directory to save the current
  configuration.

  Args:
    configuration (Configuration):
      Configuration object to save.
  """
  try:
    with open(FILE_NAME, 'w', encoding='locale') as file:
      file.write(yaml.dump(configuration.dump()))
    return True
  except yaml.YAMLError as exc:
    print(f'Error in configuration file: {exc}')
    return False

def get_configuration(
  dic: dict[str, Any]
) -> Optional[Configuration]:
  """Get the configuration from yaml

  Read the codechecker.yml file in the root directory and read it to get the
  actual configuration provided. If something given in dic, convert it.

  Args:
    dic (dict[str, Any], optional):
      Dictionary of a yaml object. If left None, configuration will be read
      from ``.codechecker.yml`` file inside root dir.
      Defaults to None.

  Returns:
    Optional[Configuration]:
      The Configuration object produced. None if dictionary or file input is
      invalid.
  """
  if not dic:
    try:
      with open(FILE_NAME, encoding='locale') as file:
        dic = yaml.full_load(file)
    except OSError as os_error:
      print(f'Problem opening the configuration file: {os_error}')
      raise ValueError('Fail to retrieve configuration file') from os_error
    except Exception as ex:
      print(f'Unknown exception while reading configuration {dic} due to {ex}')
      raise Exception from ex

  if 'projects' not in dic:
    raise ValueError('Necessary at least one project')
  if 'challenges' not in dic:
    raise ValueError('Necessary at least one challenge')

  try:
    raw_projects: dict = dic.get('projects', {})
    projects = get_projects(raw_projects)

    raw_challenges = dic.get('challenges', {})
    challenges = get_challenges(raw_challenges)

    conf = Configuration(
      challenges=challenges,
      projects=projects,
      )
    return conf
  except yaml.YAMLError as exc:
    print(f'Error in configuration file: {exc}')
    return None

def get_projects(raw_projects: Union[Any, dict]) -> list[Project]:
  """Get projects from raw dictionary.

  Args:
    raw_projects (Union[Any): raw projects collection.

  Returns:
    list[Project]: Projects list.
  """
  projects: list[Project] = []
  if isinstance(raw_projects, str):
    proj = get_project({'language': raw_projects})
    if proj is not None:
      projects.append(proj)
  else:
    for raw_proj in raw_projects:
      if isinstance(raw_proj, str):
        proj = get_project({'language': raw_proj})
      else:
        proj = get_project(raw_proj)

      if proj is not None:
        projects.append(proj)

  return projects

def get_challenges(raw_challenges: Union[Any, dict]) -> list[Challenge]:
  """Get challenges from raw challenge dictionary.

  Args:
    raw_challenges (Union[Any): raw challenge collection.

  Returns:
    list[Challenge]: Challenge list.
  """
  challenges: list[Challenge] = []
  if isinstance(raw_challenges, str):
    challenge = get_challenge({'name': raw_challenges})
    challenges.append(challenge)
  else:
    for raw_challenge in raw_challenges:
      if isinstance(raw_challenge, str):
        challenge = get_challenge({'name': raw_challenge})
      else:
        challenge = get_challenge(raw_challenge)

      if challenge is not None:
        challenges.append(challenge)

  return challenges
