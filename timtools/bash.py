#! /usr/bin/python3
"""Tools for running commands on the shell"""

import dataclasses
import logging
import os
import subprocess


@dataclasses.dataclass
class CommandResult:
    output: str
    exit_code: int


def get_output(
    cmd: list,
    passable_exit_codes: list = None,
    capture_stdout: bool = True,
    capture_stderr: bool = False,
    custom_env: dict = None,
    timeout: float = None,
) -> str:
    """Run a comand and return the output"""
    result: CommandResult = run_bash(
        cmd,
        passable_exit_codes=passable_exit_codes,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        custom_env=custom_env,
        timeout=timeout,
    )
    return result.output


def run(
    cmd: (list, str),
    passable_exit_codes: list = None,
    capture_stdout: bool = False,
    capture_stderr: bool = False,
    custom_env: dict = None,
    timeout: float = None,
) -> CommandResult:
    """Run a command"""
    if isinstance(cmd, str):
        cmd_str = cmd
        cmd = cmd.split()
    else:
        cmd_str: str = '"' + '" "'.join(cmd) + '"'
    logging.debug('Executing "%s"', cmd_str)

    if passable_exit_codes is None:
        passable_exit_codes = []

    env = os.environ.copy()
    if custom_env is not None:
        for key in custom_env.keys():
            env[key] = custom_env[key]

    # Execute command and redirect output
    if capture_stdout and capture_stderr:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env
        )
    elif capture_stdout and not capture_stderr:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
    elif not capture_stdout and capture_stderr:
        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, env=env)
    else:
        process = subprocess.Popen(cmd, env=env)

    # Capture output
    output = process.communicate(timeout=timeout)[0] or bytes()
    output_str = output.decode().rstrip()

    # Capture exitcode
    exitcode = process.returncode

    # Log execution and raise error in case of failure
    log_str = f'"{cmd_str}" has exited with code {exitcode}: {output_str}'
    if exitcode not in [0] + passable_exit_codes and "*" not in passable_exit_codes:
        raise subprocess.CalledProcessError(exitcode, cmd_str, output=output_str)

    logging.debug(log_str)

    result = CommandResult(output=output_str, exit_code=exitcode)

    return result


run_bash = run
