# coding: utf-8

import os
import sys


class TabReplace(object):
    """docstring for TabReplace"""
    def __init__(self, dirname=None):
        self.fileFilter = ('.js', '.html', '.css')
        self._dirname = dirname

    @property
    def dirname(self):
        return self._dirname

    @dirname.setter
    def dirname(self, dirname):
        if not os.path.exists(dirname):
            raise ValueError('dirname is invalid')
        self._dirname = dirname

    def tab_replace_space(self, filename):
        with open(filename, 'rw') as fg:
            data = fg.read().replace('\t', '    ')
            fg.write(data)

    def get_filename(self, dirname):
        if os.path.isfile(dirname):
            self.tab_replace_space(dirname)
        else:
            for files in os.listdir(dirname):
                codir = os.path.join(dirname, files)
                if os.path.exists(codir):
                    if os.path.isfile(codir):
                        head, ext = os.path.splitext(codir)
                        if ext in self.fileFilter:
                            self.tab_replace_space(codir)
                    else:
                        self.get_filename(codir)

    def process_func(self):
        print 'process_func beginning...'
        if self._dirname:
            self.get_filename(self._dirname)
            return None
        raise ValueError('dirname is invalid')


def fetch_command(subcommand, dirname=None):
    if dirname:
        tr = TabReplace()
        tr.dirname = dirname
    else:
        tr = TabReplace()
        tr.dirname = os.path.dirname(os.path.abspath(__file__))
    tr.process_func()
    return


def main_help_text():
    usage = [
        'Available subcommand:',
        '',
        'run:',
        'if --dir=None or anyless means run it from current dir. else dir=dirname means run it from dirname',
        '',
        'help'
    ]
    return '\n'.join(usage)


def execute_from_command_line(command=None):
    try:
        subcommand = command[1]
    except IndexError:
        subcommand = 'help'

    commands_list = ['help', 'run']
    if not subcommand == 'help' and subcommand in commands_list:
        try:
            dirname_commands = command[2]
            dirname = dirname_commands.replace('--dir=', '')
        except IndexError:
            dirname = None
        fetch_command(subcommand, dirname=dirname)
    else:
        sys.stdout.write(main_help_text())


if __name__ == '__main__':
    execute_from_command_line(command=sys.argv)
