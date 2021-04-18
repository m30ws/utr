#!/usr/bin/env python3

# Created for utr-lab2 @ FER
# but should be easily expandable
# 
# Dirs in root test dir are filtered based on dir name prefix.
#   Can be "" to apply no filter.


# usage: ./program.py
# usage: ./program.py <tests_dir>
# usage: ./program.py <tests_dir> <test_program_name>

import os
import subprocess as subp
import time
import sys
import shutil

INFILE_NAME = 't.ul'
OUTFILE_NAME = 't.iz'
TESTS_DIR = 'lab2_primjeri[1]'
TEST_DIR_PREFIX = 'test'
PROG = 'MinDka.py'
_RUNNER = ['py', 'python3', 'python']

# 
if len(sys.argv) >= 2:
	TESTS_DIR = sys.argv[1]
	if TESTS_DIR[-1] in ['/', '\\']:
		TESTS_DIR = TESTS_DIR[:-1]

if len(sys.argv) >= 3:
	PROG = sys.argv[2]

if len(sys.argv) >= 4:
	print(
	f'''  usage: {sys.argv[0]}
	\b  usage: {sys.argv[0]} <tests_dir>
	\b  usage: {sys.argv[0]} <tests_dir> <test_program_name>
	''')
	exit(1)
	

# Detect python command
i = 0
while i < len(_RUNNER):
	if shutil.which(_RUNNER[0]) == None:
		del _RUNNER[0]
	i += 1

if len(_RUNNER) == 0:
	print('> Why the fucc are you even trying to do this in python if you don\'t have it installed ?')
	exit(1)


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