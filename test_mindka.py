#!/usr/bin/env python3

# Created for utr-lab2 @ FER (MinDka.py)
# but should be easily expandable

# usage: ./program.py
# usage: ./program.py <tests_dir>
# usage: ./program.py <tests_dir> <test_program_name>

import os
import subprocess as subp
import time
import sys
import shutil

infile_name = 't.ul'
outfile_name = 't.iz'
tests_dir = 'lab2_primjeri[1]'
prog = 'MinDka.py'
_runner = ['py', 'python3', 'python']

# 
if len(sys.argv) >= 2:
	tests_dir = sys.argv[1]
	if tests_dir[-1] in ['/', '\\']:
		tests_dir = tests_dir[:-1]

if len(sys.argv) >= 3:
	prog = sys.argv[2]

if len(sys.argv) >= 4:
	print(
	f'''  usage: {sys.argv[0]}
	\b  usage: {sys.argv[0]} <tests_dir>
	\b  usage: {sys.argv[0]} <tests_dir> <test_program_name>
	''')
	exit(1)
	

# Detect python command
i = 0
while i < len(_runner):
	if shutil.which(_runner[0]) == None:
		del _runner[0]
	i += 1

if len(_runner) == 0:
	print('> Why the fucc are you even trying to do this in python if you don\'t have it installed ?')
	exit(1)


passed = 0
total_time = 0
dirs = os.listdir(tests_dir)

print(f'> Starting tests... ({prog} @ {tests_dir})')

for tst in dirs:

	with open(f'{tests_dir}/{tst}/{infile_name}') as infile, open(f'{tests_dir}/{tst}/{outfile_name}') as outfile:
		progpipe = subp.Popen(f'{_runner[0]} {prog}', stdin=infile, stdout=subp.PIPE, universal_newlines=True)

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
