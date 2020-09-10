#! /usr/bin/python3

import logging
import subprocess


def run_bash(cmd: str, passable_exit_codes: list = None, capture_stdout: bool = True, capture_stderr: bool = False) -> str:
	logging.debug(f'Executing \"{cmd}\"')
	
	if passable_exit_codes is None:
		passable_exit_codes = list()

	# Execute command and redirect output
	if capture_stdout and capture_stderr:
		process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	elif capture_stdout and not capture_stderr:
		process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
	elif not capture_stdout and capture_stderr:
		process = subprocess.Popen(cmd.split(), stderr=subprocess.PIPE)
	else:
		process = subprocess.Popen(cmd.split())

	# Capture output
	output = process.communicate()[0] or bytes()
	output_str = output.decode().rstrip()

	# Capture exitcorde
	exitcode = process.returncode

	# Log execution and raise error in case of failure
	log_str = f"\"{cmd}\" has exited with code {exitcode}: {output_str}"
	if exitcode not in [0] + passable_exit_codes and "*" not in passable_exit_codes:
		logging.error(log_str)
		raise subprocess.CalledProcessError(exitcode, cmd, output=output_str)
	else:
		logging.error(log_str)
	
	return output_str
