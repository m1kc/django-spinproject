#!/usr/bin/env python

import os
import sys
import subprocess

argv = sys.argv[1:]
if (len(argv) not in [1,2]) or (argv == ['-h']) or (argv == ['--help']):
	print('Usage: startproject.py <name> [path]')
	sys.exit(2)

name = argv[0]
path = argv[0]
if len(argv) == 2:
	path = argv[1]
	
print(f"Creating project `{name}`, path: {path}")

subprocess.run(['mkdir', '-p', path], check=True)
subprocess.run(['django-admin', 'startproject', name, path], check=True)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

subprocess.run([os.path.join(BASE_DIR, 'enhance-srta.py'), name, path], check=True)
subprocess.run([os.path.join(BASE_DIR, 'enhance-dockerfile.py'), name, path], check=True)
subprocess.run([os.path.join(BASE_DIR, 'enhance-makefile.py'), name, path], check=True)
subprocess.run([os.path.join(BASE_DIR, 'enhance-settings.py'), name, path], check=True)
