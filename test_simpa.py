#!/usr/bin/env python3

# Created for utr-lab3 @ FER
# but should be easily expandable
#
# by: m30ws (05/2021)
# 
# Dirs in root test dir are filtered based on dir name prefix.
#   Can be "" to apply no filter.

# Usage & examples:
# usage: ./program
# usage: ./program <tests_dir>
# usage: ./program <tests_dir> <test_program_name>
#          ./program - SimPa.jar
#          ./program - SimPa.exe
# default: ./program lab3_primjeri[1] SimPa.py
# default: ./program lab3_primjeri[1] SimPa.py primjer.in primjer.out

import os
import subprocess as subp
import time
import sys
import shutil
import ntpath

INFILE_NAME = 'primjer.in'
OUTFILE_NAME = 'primjer.out'
TESTS_DIR = 'lab3_primjeri[1]'
TEST_DIR_PREFIX = 'test' # ex. test02
PROG = 'SimPa.py'

_RUNNER = ['']
_ignore_option = '-'

def print_help():
	fname = ntpath.basename(sys.argv[0])
	print(
	f'''  usage: {fname}
	\b  usage: {fname} <tests_dir>
	\b  usage: {fname} <tests_dir> <test_program_name>
	\b  usage: {fname} <tests_dir> <test_program_name> <infile> <outfile>
	''')

# Cmd args 'parser'
if len(sys.argv) >= 2:
	TESTS_DIR = sys.argv[1] if sys.argv[1] != _ignore_option else TESTS_DIR
	if TESTS_DIR[-1] in ['/', '\\']:
		TESTS_DIR = TESTS_DIR[:-1]

if len(sys.argv) >= 3:
	PROG = sys.argv[2] if sys.argv[2] != _ignore_option else PROG

if len(sys.argv) == 5:
	INFILE_NAME = sys.argv[3] if sys.argv[3] != _ignore_option else INFILE_NAME
	OUTFILE_NAME = sys.argv[4] if sys.argv[4] != _ignore_option else OUTFILE_NAME

if len(sys.argv) == 4 or len(sys.argv) > 5:
	print_help()
	exit(1)

# Detect lang and command
if PROG.endswith('.exe') or '.' not in PROG: # let's hope this works
	pass #_RUNNER = ['']

elif PROG.endswith('.jar'): # Detect java command
	if shutil.which('java') == None:
		print('> Why the fucc are you even trying to do this in java if you don\'t have it installed and/or in path ?')
		exit(1)
	_RUNNER = ['java -jar']

elif PROG.endswith('.java'):
	print('\nI\'m sorry I\'m dumb, I don\'t know how to compile .java yet :\'( , use .jar')
	print('ex. in IntelliJ IDEA: File > Project Structure > Artifacts > add new')
	print('After that Build menu > Build Artifacts')
	exit(1)

else: # Detect python command
	_RUNNER = ['py', 'python3', 'python']
	i = 0
	while i < len(_RUNNER):
		if shutil.which(_RUNNER[0]) == None:
			del _RUNNER[0]
		i += 1

	if len(_RUNNER) == 0:
		print('> Why the fucc are you even trying to do this in python if you don\'t have it installed ?')
		exit(1)

# Test help
if len(sys.argv) >= 2 and sys.argv[1] == '--help':
	print_help()
	exit(0)

# Begin tests
passed = 0
total_time = 0
dirs = os.listdir(TESTS_DIR)

print(f'> Starting tests... ({PROG} @ {TESTS_DIR})')

for tst in dirs:
	if not tst.startswith(TEST_DIR_PREFIX):
		continue

	with open(f'{TESTS_DIR}/{tst}/{INFILE_NAME}') as infile, open(f'{TESTS_DIR}/{tst}/{OUTFILE_NAME}') as outfile:
		progpipe = subp.Popen(f'{_RUNNER[0]} {PROG}', stdin=infile, stdout=subp.PIPE, universal_newlines=True)

		start_time = time.time()

		stroutput = progpipe.communicate()[0]
		progpipe.wait()

		elapsed = time.time() - start_time

		try:
			progpipe.kill()
		except OSError:
			pass

		expected = outfile.read()
		print(f'{tst} ... ', end='')

		if stroutput == expected:
			passed += 1
			print(' YES', end='')
		else:
			print(' NO ', end='')

		total_time += elapsed
		print(f'  ({elapsed:.4f}s)')


print(f'> Passed: {passed}/{len(dirs)} ({passed/len(dirs)*100:.2f}%)')
print(f'> Total time: {total_time:.4f}s')