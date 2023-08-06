"""Runner for a specific project.

Runner helps you to write plugins for cc_codechecker, providing facilities to
check requirements on current machine about installed softwares and running
projects.

Anyone can write any runner by extending this module and implementing all
necessaries methods. This makes cc_codechecker extensible as pleasure.

If you need to declare other methods than currently defined, prepend their
names with an _ (underscore).

Submit any new plugin requests to daniele.tentoni.1996@gmail.com .
"""

class Runner(object):
  """Abstract base class for projects execution.

  Extends this class to make custom runners.
  """

  def __init__(self, context) -> None:
    self._context = context

  def position(self):
    """Get the executable position.
    """
    raise NotImplementedError

  def version(self):
    """Get the executable version.
    """
    raise NotImplementedError

  def run(self, *args, **kwargs):
    """Run the executable for the project.
    """
    raise NotImplementedError
