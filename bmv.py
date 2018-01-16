#!/usr/bin/env python

from __future__ import print_function
from sys import stderr, argv
from os import system, makedirs, path, listdir, rmdir, remove
from shutil import move
from argparse import ArgumentParser
from tempfile import NamedTemporaryFile

def main():
	argParser = ArgumentParser(description = "Text editor based batch file renaming/moving program.")

	argParser.add_argument("-s", "--script", type = str,
	                       help = "External command to execute for each file move. " \
	                              "Script arguments will be the old and new file names.")
	argParser.add_argument("-e", "--editor", type = str, default = "vim",
	                       help = "Editor to edit file names with.")
	argParser.add_argument("-d", "--delete-empty", action = "store_true", default = False,
	                       help = "Delete empty folders after move.")
	argParser.add_argument("files", metavar="FILE", type = str, nargs = "+", help = "File to move.")

	args = argParser.parse_args()
	moved = 0
	oldFiles = []

	for oldFile in args.files:
		if oldFile not in oldFiles:
			if path.exists(oldFile):
				oldFiles.append(oldFile)

			else:
				print("WARNING: file %s does not exist." % oldFile, file = stderr)

	if oldFiles:
		bmvHandle = NamedTemporaryFile(mode = "w", delete = False)

		for oldFile in oldFiles:
			print(oldFile, file = bmvHandle)

		bmvHandle.close()

		vimStatus = system("\"%s\" \"%s\"" % (args.editor, bmvHandle.name))

		if vimStatus != 0:
			print("ERROR: Editor error.", file = stderr)

			exit(-2)

		with open(bmvHandle.name) as bmvHandle:
			newFiles = bmvHandle.read().splitlines()

		remove(bmvHandle.name)

		if len(oldFiles) != len(newFiles):
			print("ERROR: Number of files to move is different than expected.", file = stderr)

			exit(-2)

		if len(newFiles) != len(set(newFiles)):
			print("ERROR: file names must be unique.", file = stderr)

			exit(-2)

		tmpFiles = []

		for newFile in newFiles:
			tmpFiles.append(path.join(path.dirname(newFile), ".bmv_" + path.basename(newFile)))

		for moveType in ("tmp", "final"):
			for i in range(len(oldFiles)):
				if newFiles[i] == "" or oldFiles[i] == newFiles[i]:
					continue

				try:
					if moveType == "tmp":
						newDir = path.dirname(newFiles[i])

						if newDir != "" and not path.exists(newDir):
							makedirs(newDir)

					if moveType == "tmp":
						src = oldFiles[i]
						dest = tmpFiles[i]

					else:
						src = tmpFiles[i]
						dest = newFiles[i]

					if args.script:
						system("\"%s\" \"%s\" \"%s\"" % (args.script, src, dest))

					else:
						move(src, dest)

					if moveType == "tmp" and args.delete_empty:
						oldDir = path.dirname(os.path.abspath(oldFiles[i]))

						if listdir(oldDir) == []:
							rmdir(oldDir)

				except Exception as e:
					print("WARNING: Cannot move %s to %s - %s." % (oldFiles[i], newFiles[i], str(e)), file = stderr)

				else:
					if moveType == "final":
						print("%s\t%s" % (oldFiles[i], newFiles[i]))

						moved += 1

		if moved:
			print()

	print("%s files moved." % moved)

if __name__ == "__main__":
	main()
