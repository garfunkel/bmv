#!/usr/bin/env python

from sys import stderr, argv
from os import system, makedirs, path, listdir, rmdir
from shutil import move
from argparse import ArgumentParser

TMP_FILE = '/tmp/bmv.tmp'

def main():
	argParser = ArgumentParser(description = 'Text editor based batch file renaming/moving script.')

	argParser.add_argument('-s', '--script', type = str, help = 'External script/program/command to execute ' \
	                                                            'for each file move. Script arguments ' \
	                                                            'will be the old and new file names.')
	argParser.add_argument('-e', '--editor', type = str, default = 'vim', help = 'Editor to edit file names with.')
	argParser.add_argument('-d', '--delete-empty', action = 'store_true', default = False, help = 'Delete empty folders after move.')	
	argParser.add_argument('files', metavar='FILE', type = str, nargs = '+', help = 'File to move.')

	args = argParser.parse_args()
	moved = 0
	oldFiles = []

	for oldFile in args.files:
		if oldFile not in oldFiles:
			if path.exists(oldFile):
				oldFiles.append(oldFile)

			else:
				print >> stderr, 'WARNING: file %s does not exist.' % oldFile

	if oldFiles:
		with open(TMP_FILE, 'w') as bmvHandle:
			for oldFile in oldFiles:
				print >> bmvHandle, oldFile

		vimStatus = system('%s %s' % (args.editor, TMP_FILE))

		with open(TMP_FILE) as bmvHandle:
			newFiles = [newFile.strip('\n\r') for newFile in bmvHandle.readlines() if newFile.strip('\n\r') != '']

		if vimStatus != 0:
			print >> stderr, 'ERROR: Editor error.'

			return 1

		if len(oldFiles) != len(newFiles):
			print >> stderr, 'ERROR: Number of files to move is different than expected.'

			return 2

		if len(newFiles) != len(set(newFiles)):
			print >> stderr, 'ERROR: file names must be unique.'

			return 3

		for i in xrange(len(oldFiles)):
			if oldFiles[i] != newFiles[i]:
				try:
					newDir = path.dirname(newFiles[i])

					if newDir and not path.exists(newDir):
						makedirs(newDir)

					if args.script:
						system('%s "%s" "%s"' % (args.script, oldFiles[i], newFiles[i] or './'))

					else:
						move(oldFiles[i], newFiles[i] or './')

					if args.delete_empty:
						oldDir = path.dirname(os.path.abspath(oldFiles[i]))

						while True:
							if not listdir(oldDir):
								rmdir(oldDir)

							else:
								break

							tmp = path.join(oldDir)

							if tmp == oldDir:
								break

							oldDir = tmp

				except Exception as e:
					print >> stderr, 'WARNING: Cannot move %s to %s - %s.' % (oldFiles[i], newFiles[i], str(e))

				else:
					print '%s\t%s' % (oldFiles[i], newFiles[i])

					moved += 1

		if moved:
			print

	print '%s files moved.' % moved

if __name__ == '__main__':
	main()
