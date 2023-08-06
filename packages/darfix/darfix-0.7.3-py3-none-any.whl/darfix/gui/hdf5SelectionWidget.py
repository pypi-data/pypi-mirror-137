# coding: utf-8
# /*##########################################################################
#
# Copyright (c) 2016-2017 European Synchrotron Radiation Facility
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# ###########################################################################*/


__authors__ = ["J. Garriga"]
__license__ = "MIT"
__date__ = "19/05/2021"

import logging
import os

from silx.gui import qt
from silx.gui.dialog.DataFileDialog import DataFileDialog
from darfix.core.dataset import Dataset

_logger = logging.getLogger(__file__)


class HDF5SelectionWidget(qt.QTabWidget):
    """
    Widget that creates a dataset from a list of files or from a single filename.
    It lets the user add the first filename of a directory of files, or to
    upload manually each of the files to be read.
    If both options are filled up, only the files in the list of filenames
    are read.
    """
    sigProgressChanged = qt.Signal(int)

    def __init__(self, parent=None):
        qt.QTabWidget.__init__(self, parent)

        # Raw data
        self._rawFileData = FileSelectionWidget()
        self._inDiskCB = qt.QCheckBox("Use data from disk", self)
        rawData = qt.QWidget(self)
        rawData.setLayout(qt.QVBoxLayout())
        rawData.layout().addWidget(self._rawFileData)
        rawData.layout().addWidget(self._inDiskCB)
        self.addTab(rawData, 'raw data')

        self._inDisk = False

        # Dark data
        self._darkFileData = FileSelectionWidget()
        self.addTab(self._darkFileData, 'dark data')

        # Treated data
        self._treatedDirData = DirSelectionWidget(parent=self)
        self.addTab(self._treatedDirData, 'treated data')

        self._dataset = None
        self.bg_dataset = None
        self.indices = None
        self.bg_indices = None

        self.getTreatedDir = self._treatedDirData.getDir
        self.setTreatedDir = self._treatedDirData.setDir

        self._inDiskCB.stateChanged.connect(self.__inDisk)

    def loadDataset(self):
        """
        Loads the dataset from the filenames.
        """
        try:
            _dir = self._treatedDirData.getDir()
            rawDataUrl = self._rawFileData.getUrl()

            _dir = _dir if _dir != "" else os.path.dirname(rawDataUrl.file_path())
            self._dataset = Dataset(_dir=_dir,
                                    first_filename=rawDataUrl, isH5=True,
                                    in_memory=not self._inDisk, copy_files=True)
            return True
        except Exception as e:
            raise e
            return False

    @property
    def dataset(self):
        return self._dataset

    def getDataset(self):
        return self._dataset, self.indices, self.bg_indices, self. bg_dataset

    def updateProgress(self, progress):
        self.sigProgressChanged.emit(progress)

    def __inDisk(self, inDisk):
        self._inDisk = bool(inDisk)


class FileSelectionWidget(qt.QWidget):

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)
        self._dataUrl = None
        self._urlLabel = qt.QLabel("")
        self._uploadButton = qt.QPushButton("Upload hdf5 file", parent=self)
        widget = qt.QWidget(parent=self)
        widget.setMinimumWidth(200.0)
        layout = qt.QHBoxLayout()
        layout.addWidget(self._urlLabel)
        layout.addWidget(self._uploadButton)
        widget.setLayout(layout)

        self._uploadButton.clicked.connect(self.uploadRawData)

    def uploadRawData(self):
        dialog = DataFileDialog()
        if dialog.exec_():
            self._dataUrl = dialog.selectedDataUrl()
            self._urlLabel.setText(dialog.selectedFile())
        else:
            _logger.warning("Could not open dataset")

    def getUrl(self):
        return self._dataUrl



class DirSelectionWidget(qt.QWidget):
    """
    Widget used to obtain a filename (manually or from a file)
    """

    dirChanged = qt.Signal()

    def __init__(self, parent=None):
        qt.QWidget.__init__(self, parent)

        self._dir = qt.QLineEdit('', parent=self)
        self._dir.editingFinished.connect(self.dirChanged)
        self._addButton = qt.QPushButton("Upload directory", parent=self)
        # self._okButton =  qt.QPushButton("Ok", parent=self)
        self._addButton.pressed.connect(self._uploadDir)
        # self._okButton.pressed.connect(self.close)
        self.setLayout(qt.QHBoxLayout())

        self.layout().addWidget(self._dir)
        self.layout().addWidget(self._addButton)
        # self.layout().addWidget(self._okButton)

    def _uploadDir(self):
        """
        Loads the file from a FileDialog.
        """
        fileDialog = qt.QFileDialog()
        fileDialog.setOption(qt.QFileDialog.ShowDirsOnly)
        fileDialog.setFileMode(qt.QFileDialog.Directory)
        if fileDialog.exec_():
            self._dir.setText(fileDialog.directory().absolutePath())
            self.dirChanged.emit()
        else:
            _logger.warning("Could not open directory")

    def getDir(self):
        return str(self._dir.text())

    def setDir(self, _dir):
        self._dir.setText(str(_dir))
