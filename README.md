bmv
===

Batch file renaming program using vim/another editor to do the editing of names. You can use any editor you like. You can also use any external program to 'move' files.

## Usage

```
usage: bmv.py [-h] [-s SCRIPT] [-e EDITOR] [-d] FILE [FILE ...]

Text editor based batch file renaming/moving program.

positional arguments:
  FILE                  File to move.

optional arguments:
  -h, --help            show this help message and exit
  -s SCRIPT, --script SCRIPT
                        External command to execute for each file move. Script
                        arguments will be the old and new file names.
                        (default: mv)
  -e EDITOR, --editor EDITOR
                        Editor to edit file names with. (default: vim)
  -d, --delete-empty    Delete empty folders after move. (default: False)
```

## Example

Say we have a directory with files in it named *a*, *b*, and *c*. With the command:
```
bmv.py /path/to/a /path/to/b /path/to/c
```

Vim will open up with a, b, and c each on separate lines of text (in the same order as given on the command line), like so:
```
/path/to/a
/path/to/b
/path/to/c
```

If we then edit these lines like so:
```
/path/to/new/a
/path/to/bbb
/path/to/a
```

If we now save this file, bmv will move the files to their new locations. It will handle the creation of intermediate directories, and will not clobber files upon move. For example, moving file *a* to *b*, while also moving file *b* to *a* will result in the files being swapped correctly. bmv will also operate on directories and other type of files.
