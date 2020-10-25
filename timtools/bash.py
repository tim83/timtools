#! /usr/bin/python3

import logging
import subprocess


def get_output(cmd: list, passable_exit_codes: list = None, capture_stdout: bool = True, capture_stderr: bool = False) -> str:
	return run_bash(cmd, passable_exit_codes=passable_exit_codes, capture_stdout=capture_stdout, capture_stderr=capture_stderr)


def run(cmd: (list, str), passable_exit_codes: list = None, capture_stdout: bool = False, capture_stderr: bool = False) -> str:
	if type(cmd) == str:
		cmd_str = cmd
		cmd = cmd.split()
	else:
		cmd_str: str = "\"" + "\" \"".join(cmd) + "\""
	logging.debug(f'Executing \"{cmd_str}\"')

	if passable_exit_codes is None:
		passable_exit_codes = list()

	# Execute command and redirect output
	if capture_stdout and capture_stderr:
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	elif capture_stdout and not capture_stderr:
		process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
	elif not capture_stdout and capture_stderr:
		process = subprocess.Popen(cmd, stderr=subprocess.PIPE)
	else:
		process = subprocess.Popen(cmd)

	# Capture output
	output = process.communicate()[0] or bytes()
	output_str = output.decode().rstrip()

	# Capture exitcode
	exitcode = process.returncode

	# Log execution and raise error in case of failure
	log_str = f"\"{cmd_str}\" has exited with code {exitcode}: {output_str}"
	if exitcode not in [0] + passable_exit_codes and "*" not in passable_exit_codes:
		logging.error(log_str)
		raise subprocess.CalledProcessError(exitcode, cmd_str, output=output_str)
	else:
		logging.debug(log_str)

	return output_str


run_bash = run
