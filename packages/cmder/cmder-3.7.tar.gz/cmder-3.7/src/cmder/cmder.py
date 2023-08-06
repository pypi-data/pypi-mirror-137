#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
A shortcut for running shell command.
"""
import argparse
import subprocess
import os
import sys
import shlex
import tempfile

CMD_LINE_LENGTH = 100
PMT = False

try:
    from loguru import logger
    logger.remove()
    logger.add(sys.stderr, format="<level>{message}</level>", filter=lambda record: record["level"].name == "DEBUG")
    logger.add(sys.stderr, format="<light-green>[{time:HH:mm:ss}]</light-green> <level>{message}</level>", level="INFO")
except ImportError:
    import logging
    logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
    logger = logging.getLogger()


def run(cmd, **kwargs):
    """ Run cmd or raise exception if run fails. """
    def format_cmd(command):
        if isinstance(command, str):
            command = shlex.shlex(command, posix=True, punctuation_chars=True)
            command.whitespace_split = True
            command = list(command)
        elif isinstance(command, (list, tuple)):
            command = [str(c) for c in command]
        else:
            raise TypeError('Command only accepts a string or a list (or tuple) of strings.')
        exe = command[0]
        if len(' '.join(command)) <= CMD_LINE_LENGTH:
            return exe, ' '.join(command)
        command = ' '.join([f'\\\n  {c}' if c.startswith('-') or '<' in c or '>' in c else c for c in command])
        command = command.splitlines()
        commands = []
        for i, c in enumerate(command):
            if i == 0:
                commands.append(c)
            else:
                if len(c) <= 80:
                    commands.append(c)
                else:
                    items = c.strip().replace(' \\', '').split()
                    commands.append(f'  {items[0]} {items[1]} \\')
                    for item in items[2:]:
                        commands.append(' ' * (len(items[0]) + 3) + item + ' \\')
        command = '\n'.join(commands)
        if command.endswith(' \\'):
            command = command[:-2]
        return exe, command
    
    def parse_profile():
        try:
            with open(profile_output) as f:
                t, m = f.read().strip().split()
                t = t.split(".")[0]
                try:
                    hh, mm, ss = t.split(':')
                except ValueError:
                    hh, (mm, ss) = 0, t.split(':')
                t = f'{int(hh):02d}:{int(mm):02d}:{int(ss):02d}'
                m = float(m)
                if m < 1000:
                    m = f'{m:.2f}KB'
                elif m < 1000 * 1000:
                    m = f'{m / 1000:.2f}MB'
                else:
                    m = f'{m / 1000 / 1000:.2f}GB'
                s = f'{t} {m}'
        except FileNotFoundError:
            s = '00:00:00 0.00KB'
        return s
    
    msg, pmt, fmt_cmd = kwargs.pop('msg', ''), kwargs.pop('pmt', False), kwargs.pop('fmt_cmd', True)
    log_cmd, debug = kwargs.pop('log_cmd', True), kwargs.pop('debug', False)
    exit_on_error = kwargs.pop('exit_on_error', False)
    if fmt_cmd:
        program, cmd = format_cmd(cmd)
    else:
        if isinstance(cmd, str):
            program, cmd = cmd.split()[0], cmd
        else:
            program, cmd = cmd[0], ' '.join([str(c) for c in cmd])
    if msg:
        logger.info(msg)
    if log_cmd:
        logger.debug(cmd)
    cwd = kwargs.pop('cwd', None)
    profile_output = tempfile.mktemp(suffix='.txt', prefix='.profile.', dir=cwd)
    try:
        if msg and (pmt or PMT):
            cmd = f'/usr/bin/time -f "%E %M" -o {profile_output} {cmd}'
        kwargs['stdout'] = kwargs.pop('stdout', sys.stdout if debug else subprocess.PIPE)
        kwargs['stderr'] = kwargs.pop('stderr', sys.stderr if debug else subprocess.PIPE)
        process = subprocess.Popen(cmd, universal_newlines=True, shell=True, cwd=cwd, **kwargs)
        process.wait()
        if process.returncode: 
            stdout, stderr = process.communicate()
            logger.error(f'Failed to run {program} (exit code {process.returncode}):\n{stderr or stdout}')
            if exit_on_error:
                sys.exit(process.returncode)
        if not process.returncode and msg:
            msg = msg.replace(' ...', f' complete.')
            if pmt or PMT:
                msg = f'{msg[:-1]} [{parse_profile()}].' if msg.endswith('.') else f'{msg} [{parse_profile()}].'
            logger.info(msg)
    finally:
        if os.path.isfile(profile_output):
            os.unlink(profile_output)
    return process


def parse(jobname='', email='', runtime=2, memory=1, cores=1, nodes=1, excludes=None, **kwargs):
    if excludes:
        if isinstance(excludes, str):
            excludes = [excludes]
        elif isinstance(excludes, (list, tuple)):
            pass
        else:
            logger.warning('Invalid argument excludes, it only accepts a str, list, or tuple, ignored.')
            excludes = []
    else:
        excludes = []
    parser = argparse.ArgumentParser(**kwargs)
    if 'jobname' not in excludes:
        parser.add_argument('--job', help='Name of a job, default: %(default)s.', default=jobname)
    if 'email' not in excludes:
        parser.add_argument('--email', default=email,
                            help='Email address for notifying you the start, end, and abort of a job, '
                                 'default: %(default)s.')
    if 'runtime' not in excludes:
        parser.add_argument('--runtime', type=int, default=runtime,
                            help='Time (in integer hours) for running a job, default: %(default)s.')
    if 'memory' not in excludes:
        parser.add_argument('--memory', type=int, default=memory,
                            help='Amount of memory (in GB, integer) for all CPU cores, default: %(default)s.')
    if 'cores' not in excludes:
        parser.add_argument('--cores', type=int, default=cores,
                            help='Number of CPU cores on each node can be used for a job, default: %(default)s.')
    if 'nodes' not in excludes:
        parser.add_argument('--nodes', type=int, default=nodes,
                            help='Number of nodes can be used for a job, default: %(default)s.')
    if 'hold' not in excludes:
        parser.add_argument('--hold', action='store_true',
                            help='Generate the submit script but hold it without submitting to the job scheduler.')
    if 'debug' not in excludes:
        parser.add_argument('--debug', action='store_true', help='Invoke debug mode (for development use only).')
    if 'dryrun' not in excludes:
        parser.add_argument('--dryrun', action='store_true',
                            help='Print out steps and IO of each step without actually running the pipeline.')
    return parser


def filename(p):
    if p and not os.path.isfile(p):
        logger.error(f'Path "{p}" may not be a file or does not exist.')
        sys.exit(1)
    return p


def dirname(p):
    if p and not os.path.isdir(p):
        logger.error(f'Path "{p}" may not be a directory or does not exist.')
        sys.exit(1)
    return p
    

if __name__ == '__main__':
    pass
