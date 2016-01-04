#!/usr/bin/python

import sys, os, re, timeit, datetime

class Node:
  def __init__(self, name, parent):
    self.name = name
    self.parent = parent
    self.visited = False
    self.children = []

  def addChild(self, child):
    self.children.append(child)

  def addChildren(self, children):
    for child in children:
      self.addChild(child)

  def fullname(self):
    if self.parent is not None:
      return self.parent.fullname() + os.path.sep + self.name
    else:
      return self.name

  def getParent(self, level):
    localParent = self.parent
    for i in range(level):
      if localParent is None:
        break
      localParent = localParent.parent
    return localParent

  def walk(self):
    list = []
    if len(self.children) is 0:
      list.append(self)
    for child in self.children:
      list.extend(child.walk())
    return list

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
  components = os.path.abspath(path).split(os.path.sep)
  if len(components) is 0:
    return []
  parent = None
  for dir in components[:-1]:
    child = Node(dir, parent)
    if parent is not None:
      parent.addChild(child)
    parent = child
  return _getFiles(path, parent)

def _getFiles(path, parent):
  node = Node(os.path.basename(os.path.abspath(path)), parent)
  list = []
  for file in os.listdir(path):
    fullPath = os.path.join(path, file)
    if os.path.isdir(fullPath):
      children = _getFiles(fullPath, node)
      parent.addChildren(children)
      list.extend(children)
    else:
      child = Node(file, node)
      parent.addChild(child)
      list.append(child)
  return list

def main(argv):
  global shouldDelete

  if len(argv) < 1:
    print "Please specify the search directory"
    sys.exit(0)
  if len(argv) > 1:
    if argv[1].lower() == "delete":
      shouldDelete = True

  start = timeit.default_timer()
  files = walkDir(argv[0])
  walkTime = timeit.default_timer()

  duplicates = []
  # find = re.compile(r"^([^.]*).*")
  for file in files:
    filename = file.name

    # print re.search(find, filename).group(0)
    if file.visited:
      continue

    file.visited = True

    fileFirstPart = filename[0:filename.find('.')]
    fileExtension = os.path.splitext(filename)[1]

    localDuplicates = []

    found = False
    for otherFile in file.getParent(1).walk():
      otherFileName = otherFile.name

      if otherFile.visited:
        continue

      otherFileExtension = os.path.splitext(otherFileName)[1]
      if otherFileName.startswith(fileFirstPart) and fileExtension.lower() in valid_extensions and otherFileExtension.lower() in valid_extensions:
        otherFile.visited = True
        found = True
        localDuplicates.append(otherFile.fullname())

    if found:
      localDuplicates.append(file.fullname())
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

  stop = timeit.default_timer()

  if len(duplicates) > 0:
    print ""

  print "Found " + str(len(duplicates)) + " duplicated entries"
  print "Time needed:"
  print "  Total:\t" + str(datetime.timedelta(seconds=(stop - start)))
  print "  I/O:\t\t" + str(datetime.timedelta(seconds=(walkTime - start)))
  print "  CPU:\t\t" + str(datetime.timedelta(seconds=(stop - walkTime)))
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
