"""Tools for running commands on the shell"""

import dataclasses
import logging
import os
import subprocess


@dataclasses.dataclass
class CommandResult:
    """Dataclass for storing the result of a command run"""

    output: str
    exit_code: int


def get_output(  # pylint: disable=too-many-arguments
    cmd: list,
    passable_exit_codes: list = None,
    capture_stdout: bool = True,
    capture_stderr: bool = False,
    custom_env: dict = None,
    timeout: float = None,
    **kwargs
) -> str:
    """Run a command and return the output"""
    result: CommandResult = run(
        cmd,
        passable_exit_codes=passable_exit_codes,
        capture_stdout=capture_stdout,
        capture_stderr=capture_stderr,
        custom_env=custom_env,
        timeout=timeout,
        **kwargs
    )
    return result.output


def run(  # pylint: disable=too-many-arguments,too-many-locals
    cmd: (list, str),
    passable_exit_codes: list = None,
    capture_stdout: bool = False,
    capture_stderr: bool = False,
    custom_env: dict = None,
    timeout: float = None,
    **kwargs
) -> CommandResult:
    """Run a command"""
    cmd: list[str]
    if isinstance(cmd, str):
        cmd = cmd.split()
    cmd_str = " ".join(cmd)
    logging.debug('Executing "%s"', cmd_str)

    if passable_exit_codes is None:
        passable_exit_codes = []

    env = os.environ.copy()
    if custom_env is not None:
        env.update(custom_env)

    # Execute command and redirect
    output_args: dict[str]
    if capture_stdout and capture_stderr:
        output_args = {"stdout": subprocess.PIPE, "stderr": subprocess.PIPE}
    elif capture_stdout and not capture_stderr:
        output_args = {"stdout": subprocess.PIPE}
    elif not capture_stdout and capture_stderr:
        output_args = {"stderr": subprocess.PIPE}
    else:
        output_args = {}

    process = subprocess.Popen(  # pylint: disable=consider-using-with
        cmd, env=env, **output_args, **kwargs
    )
    output = process.communicate(timeout=timeout)[0] or bytes()
    exitcode = process.returncode

    output_str = output.decode().rstrip()

    # Log execution and raise error in case of failure
    if exitcode not in [0] + passable_exit_codes and "*" not in passable_exit_codes:
        raise subprocess.CalledProcessError(exitcode, cmd_str, output=output_str)

    logging.debug('"%s" has exited with code %s: %s', cmd_str, exitcode, output_str)

    result = CommandResult(output=output_str, exit_code=exitcode)

    return result


def run_bash():
    """Old implementation of bash.run, now deprecated"""
    raise DeprecationWarning("bash.run_bash has been replaced by bash.run")
