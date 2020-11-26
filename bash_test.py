import pytest
import subprocess

from timtools import bash

test_str = "Hello World"

def test_bash_getoutput():
	assert bash.get_output(["echo", test_str]) == test_str


def test_bash_run():
	# Check output of command
	assert bash.run(["echo", test_str]) == ""
	assert bash.run(["echo", test_str], capture_stdout=True) == test_str
	assert bash.run(["echo", test_str], capture_stderr=True) == ""

	# Check command that does not exist
	with pytest.raises(FileNotFoundError):
		bash.run(["thiscommanddoesnotexist"])

	# Check failing command
	with pytest.raises(subprocess.CalledProcessError):
		bash.run(["false"])
	assert bash.run(["false"], passable_exit_codes=[1]) == ""
