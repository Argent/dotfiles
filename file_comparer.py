#!/usr/bin/python

import sys, os, re

valid_extensions = [".avi", ".mkv", ".mp4"]
qualities = ["bluray", "web-dl", "web.dl", "webrip", "hdtv"]

shouldDelete = False

def cmp_items(a, b):
  reversedQualities = list(reversed(qualities))

  indexA = -1
  indexB = -1

  for index, quality in enumerate(reversedQualities):
    if indexA == -1:
      if quality in a.lower():
        indexA = index

    if indexB == -1:
      if quality in b.lower():
        indexB = index

  if indexA < indexB:
    return 1
  elif indexA == indexB:
    return 0
  else:
    return -1

def sizeof_fmt(num, suffix='B'):
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def walkDir(path):
  retVal = []
  for (dir, _, files) in os.walk(path):
    for f in files:
      path = os.path.join(dir, f)
      retVal.append(path)
  return retVal

def main(argv):
  global shouldDelete

  if len(argv) < 1:
    print "Please specify the search directory"
    sys.exit(0)
  if len(argv) > 1:
    if argv[1].lower() == "delete":
      shouldDelete = True
  files = walkDir(argv[0])
  files = [[file, False] for file in files]
  duplicates = []
  #find = re.compile(r"^([^.]*).*")
  for index, (file, visited) in enumerate(files):
    #print re.search(find, file).group(0)
    if visited:
      continue

    files[index][1] = True

    fileFirstPart = file[0:file.find('.')]
    fileExtension = os.path.splitext(file)[1]

    localDuplicates = []

    found = False
    for index, (otherFile, visited) in enumerate(files):
      if visited:
        continue

      otherFileExtension = os.path.splitext(otherFile)[1]
      if otherFile.startswith(fileFirstPart) and fileExtension.lower() in valid_extensions and otherFileExtension.lower() in valid_extensions:
        files[index][1] = True
        found = True
        localDuplicates.append(otherFile)

    if found:
      localDuplicates.append(file)
      localDuplicates.sort(cmp_items)
      for toDelete in localDuplicates[1:]:
        duplicates.append(toDelete)
        if shouldDelete:
          print "Deleting: " + toDelete
          os.remove(toDelete)
        else:
          print "Would delete: " + toDelete

  fileSizeSum = 0
  for duplicate in duplicates:
    fileSizeSum += os.stat(duplicate).st_size

  if len(duplicates) > 0:
    print ""

  print "Found " + str(len(duplicates)) + " duplicated entries"
  print "Total file size: " + sizeof_fmt(fileSizeSum)

  if not shouldDelete and len(duplicates) > 0:
    print ""
    response = query_yes_no("Do you want to delete these files now?")
    if response == True:
      for duplicate in duplicates:
        print "Deleting: " + duplicate
        os.remove(duplicate)

if __name__ == "__main__":
  #print 'Number of arguments:', len(sys.argv), 'arguments.'
  #print 'Argument List:', str(sys.argv)
  main(sys.argv[1:])



