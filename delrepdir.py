#!/usr/bin/env python
# encoding: utf-8

import os
import shutil
dirname = os.path.dirname(os.path.abspath(__file__))

for files in os.listdir(dirname):
    if os.path.isdir(files):
        codir = os.path.join(dirname, files, files)
        print codir
        if os.path.exists(codir):
            try:
                os.removedirs(codir)
            except OSError:
                shutil.rmtree(codir)
