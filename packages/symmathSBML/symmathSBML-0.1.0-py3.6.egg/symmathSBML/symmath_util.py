"""Utitility functions"""

from symmathSBML import constants as cn
from symmathSBML import msgs
from symmathSBML.symmath_sbml import SymmathSBML
from symmathSBML.symmath_base import IteratorItem

import os.path
import zipfile


def getZipfilePaths(data_dir=cn.DATA_DIR,
        zip_filename=cn.BIOMODELS_ZIP_FILENAME):
      """
      :param str data_dir: absolute path of the directory containing
          the xml files
      :param str zip_filename: name of the zipfile to process
      :return list-str, ZipFile: list of file paths, ZipFile object for file
      """
      path = os.path.join(data_dir, zip_filename)
      zipper = zipfile.ZipFile(path, "r")
      files = [f.filename for f in zipper.filelist]
      return files, zipper

def modelIterator(initial=0, final=1000,
        data_dir=cn.DATA_DIR,
        zip_filename=cn.BIOMODELS_ZIP_FILENAME):
    """
    Iterates across all models in a data directory.
    :param int initial: initial file to process
    :param int final: final file to process
    :param str data_dir: absolute path of the
        directory containing
        the xml files
    :param str zip_filename: name of the zipfile to process.
        If None, then looks for XML files in the directory.
    :return IteratorItem:
    """
    files, zipper = getZipfilePaths(
          data_dir=data_dir, zip_filename=zip_filename)
    # Functions for file types
    def readXML(filename):
        path = os.path.join(data_dir, filename)
        with open(path, 'r') as fd:
            lines = ''.join(fd.readlines())
        return lines
    def readZip(filename):
        with zipper.open(filename, 'r') as fid:
            lines = fid.read()
        return lines
    #
    if zip_filename is not None:
        read_func = readZip
    else:
        read_func = readXML
    begin_num = max(initial, 0)
    num = begin_num - 1
    end_num = min(len(files), final)
    for filename in files[begin_num:end_num]:
        num += 1
        lines = read_func(filename)
        if isinstance(lines, bytes):
          lines = lines.decode("utf-8")
        try:
            model = SymmathSBML(lines)
        except NameError as err:
            msg = "%s: %s" % (filename, str(err))
            msgs.error(msg)
        iterator_item = IteratorItem(filename=filename,
            model=model, number=num)
        yield iterator_item
