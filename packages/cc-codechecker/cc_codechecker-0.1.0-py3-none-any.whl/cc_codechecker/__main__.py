"""Coding Challenge Code Checker

Use this tool to collect coding challenge projects, run and evaluate them.
Configure using YAML notation and produce output in many formats.

Rode map before release 0.1.0:
1. Read YAML file codechecker.yml in the root of a repository
2. Execute code inside a project
3. Produce output in txt format
"""

# Standard Library
import argparse
import os
import sys
from textwrap import dedent

# Codechecker
import cc_codechecker.codechecker
import cc_codechecker.configuration


def check_git_repository() -> bool:
  """Report error if this is not a git repository

  Returns:
      bool: [description]
  """

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
config_parser.set_defaults(func=cc_codechecker.codechecker.check)
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
init_parser.set_defaults(func=cc_codechecker.codechecker.init)
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
run_parser.set_defaults(func=cc_codechecker.codechecker.run)
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
