import multiprocessing

from package.ui import Ui_SlateInPost
from package.utils.speech_reg import Sr
from package.utils import convert, similarity
import os
from PyQt5 import QtCore, QtWidgets


class SlateInPost(QtWidgets.QApplication):

    def __init__(self, argv):
        super().__init__(argv)
        self.ui = Ui_SlateInPost()
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui.setupUi(self.MainWindow)
        self.ui.importBtn.clicked.connect(self.importMedia)
        self.ui.outputBtn.clicked.connect(self.output)
        self.ui.similaritySlider.valueChanged.connect(self.similarityValue)
        self.ui.actionBtn.clicked.connect(self.action)
        self.ui.convertForMe.stateChanged.connect(self.disableCheck)
        self.ui.speechAPIcombo.currentIndexChanged.connect(self.select_api)
        self.ui.deleteWAV.toggled.connect(self.disableCheck)
        
    def importMedia(self):
        files, _ = QtWidgets.QFileDialog.getOpenFileNames(None, "Select Media Files", "", "Media Files (*.mp4 *.wmv "
                                                                                          "*.mp3 *.mov *.m4a *.wav)")
        if files:
            self.ui.files = list(files)
            print(self.ui.files)

    def output(self):
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(self.ui.centralwidget, "Save output as...", "", "Text File "
                                                                                                         "(*.txt)")
        if fileName:
            path, _ = os.path.split(fileName)
            self.ui.savePath = path
            print(self.ui.savePath)
            self.ui.outputFile = open(fileName, "w+")

    def select_api(self):
        if self.ui.speechAPIcombo.currentText() == "Wit.ai":
            text, okPressed = QtWidgets.QInputDialog.getText(self.ui.centralwidget, "Key Required",
                                                             "Wit.ai key:",
                                                             QtWidgets.QLineEdit.Normal, "")
            if okPressed and text != '':
                self.ui.info = [text]
            else:
                self.ui.speechAPIcombo.setCurrentIndex(0)
        elif self.ui.speechAPIcombo.currentText() == "Bing":
            text, okPressed = QtWidgets.QInputDialog.getText(self.ui.centralwidget, "Key Required",
                                                             "Bing API key:",
                                                             QtWidgets.QLineEdit.Normal, "")
            if okPressed and text != '':
                self.ui.info = [text]
            else:
                self.ui.speechAPIcombo.setCurrentIndex(0)
        elif self.ui.speechAPIcombo.currentText() == "Houndify":
            text, okPressed = QtWidgets.QInputDialog.getText(self.ui.centralwidget, "Client info Required",
                                                             "Please enter you Houdify client info in the format "
                                                             "id,key (your client id then your client key, separated "
                                                             "by a comma):",
                                                             QtWidgets.QLineEdit.Normal, "")
            if okPressed and text != '' and "," in text:
                self.ui.info = text.split(",")
            else:
                self.ui.speechAPIcombo.setCurrentIndex(0)
        elif self.ui.speechAPIcombo.currentText() == "IBM":
            text, okPressed = QtWidgets.QInputDialog.getText(self.ui.centralwidget, "IBM account info required",
                                                             "Please enter you IBM account info in the format "
                                                             "username,password (your username then your password, "
                                                             "separated by a comma):",
                                                             QtWidgets.QLineEdit.Normal, "")
            if okPressed and text != '' and "," in text:
                self.ui.info = text.split(",")
            else:
                self.ui.speechAPIcombo.setCurrentIndex(0)


    def disableCheck(self):
        if not self.ui.convertForMe.isChecked():
            self.ui.deleteWAV.setChecked(False)

    def similarityValue(self):
        self.ui.similarityLabel.setText("Similarity: " + str(self.ui.similaritySlider.value()) + "%")

    def show_popup(self, name, text):
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle(name)
        msg.setText(text)
        x = msg.exec_()

    def _run_reg(self):
        progress_dialog = QtWidgets.QProgressDialog(self.ui.centralwidget)
        progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
        progress_dialog.setWindowTitle("Transcribing your files")
        progress_dialog.setCancelButton(None)
        progress_dialog.setMaximum(100)
        progress_dialog.setMinimum(0)
        progress_dialog.forceShow()
        regconizer = Sr(self.ui.speechAPIcombo.currentText(), self.ui.info)
        p = multiprocessing.Pool()
        result = []

        progress_dialog.setValue(1)
        progress_dialog.setLabelText("Starting transcription...")
        QtCore.QCoreApplication.processEvents()
        for i, r in enumerate(p.imap(regconizer.transcribe_file, self.ui.files), 1):
            progress_dialog.setLabelText("Transcribing {}...".format(r[1]))
            progress = (i / len(self.ui.files)) * 100
            result.append(r)
            progress_dialog.setValue(int(progress))
        progress_dialog.close()
        for tup in result:
            sus, file, transcript = tup
            if sus:
                self.ui.data[transcript] = file
        errors = [tup[1] for tup in result if not tup[0]]
        p.close()
        return errors

    def action(self):
        if not self.ui.outputFile:
            self.ui.show_popup("Error", "Have you chosen your output path yet?")
            return
        self.ui.data = {}
        if self.ui.convertForMe.isChecked():
            progress_dialog = QtWidgets.QProgressDialog(self.ui.centralwidget)
            progress_dialog.setWindowModality(QtCore.Qt.WindowModal)
            progress_dialog.setWindowTitle("Converting your files")
            progress_dialog.setCancelButtonText("Cancel")
            progress_dialog.setMaximum(100)
            progress_dialog.setMinimum(0)
            progress_dialog.forceShow()
            for i in range(len(self.ui.files)):
                progress_dialog.setValue(int((i+1)/len(self.ui.files)*100))
                progress_dialog.setLabelText("Converting {}...".format(self.ui.files[i]))
                new = convert.convert_one_file(self.ui.files[i], self.ui.savePath)
                self.ui.files[i] = new
            progress_dialog.close()
        errors = self._run_reg()
        if self.ui.deleteWAV.isChecked():
            for file in self.ui.files:
                os.remove(file)
        if len(errors) == len(self.ui.files):
            self.ui.show_popup("Complete", "None of your files were successfully transcribed. Did you enter your "
                            "api key/credentials correctly?")
            return
        result = similarity.process_list(self.ui.data, self.ui.similaritySlider.value())
        self.ui.outputFile.write("="*20 + "\nSimilarity Report\n" + "="*20+"\n")
        for nameFile in result.keys():
            self.ui.outputFile.write(nameFile + "\n")
            for other in result[nameFile]:
                self.ui.outputFile.write("\t{}\n".format(other))
        self.ui.outputFile.write("="*20 + "\nTranscripts\n" + "="*20+"\n")
        for script in self.ui.data.keys():
            self.ui.outputFile.write("-"*10 + self.ui.data[script] + "-"*10+"\n")
            self.ui.outputFile.write(script+"\n")
        if errors != []:
            self.ui.outputFile.write("=" * 20 + "\nFiles Not Transcribed\n" + "=" * 20+"\n")
            for name in errors:
                self.ui.outputFile.write(name+"\n")
        self.ui.outputFile.close()
        if len(errors) == 0:
            self.ui.show_popup("Complete", "All your files are successfully transcribed!")
        else:
            files = "\n"
            for file in errors:
                files += file
                files += "\n"
            files = files[:-1]
            self.ui.show_popup("Complete", str(len(self.ui.files) - len(errors)) + " out of " + str(len(self.ui.files))
                            + " files were successfully transcribed. We had trouble transcribing the following files"
                              ":" + files)

    def run(self):
        self.MainWindow.setWindowTitle("SlateInPost (v0.0.1)")
        self.MainWindow.show()
        self.exec_()
