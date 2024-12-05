import os
import sys

from PyQt6.QtCore import QSize
from PyQt6.QtGui import QAction, QFontDatabase, QIcon
from PyQt6.QtPrintSupport import QPrintDialog
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QMessageBox,
    QPlainTextEdit,
    QStatusBar,
    QToolBar,
    QVBoxLayout,
    QWidget,
)


basedir = os.path.dirname(__file__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        self.editor = (
            QPlainTextEdit()
        )  # Could also use a QTextEdit and set self.editor.setAcceptRichText(False)

        # Setup the QTextEdit editor configuration
        fixedfont = QFontDatabase.systemFont(QFontDatabase.SystemFont.FixedFont)
        fixedfont.setPointSize(12)
        self.editor.setFont(fixedfont)

        # self.path holds the path of the currently open file.
        # If none, we haven't got a file open yet (or creating new).
        self.path = None

        layout.addWidget(self.editor)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.status = QStatusBar()
        self.setStatusBar(self.status)

        file_toolbar = QToolBar("File")
        file_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(file_toolbar)
        file_menu = self.menuBar().addMenu("&File")

        open_file_action = QAction(
            QIcon(os.path.join(basedir, "images", "blue-folder-open-document.png")),
            "Open file...",
            self,
        )
        open_file_action.setStatusTip("Open file")
        open_file_action.triggered.connect(self.file_open)
        file_menu.addAction(open_file_action)
        file_toolbar.addAction(open_file_action)

        save_file_action = QAction(
            QIcon(os.path.join(basedir, "images", "disk.png")), "Save", self
        )
        save_file_action.setStatusTip("Save current page")
        save_file_action.triggered.connect(self.file_save)
        file_menu.addAction(save_file_action)
        file_toolbar.addAction(save_file_action)

        saveas_file_action = QAction(
            QIcon(os.path.join(basedir, "images", "disk--pencil.png")),
            "Save As...",
            self,
        )
        saveas_file_action.setStatusTip("Save current page to specified file")
        saveas_file_action.triggered.connect(self.file_saveas)
        file_menu.addAction(saveas_file_action)
        file_toolbar.addAction(saveas_file_action)

        print_action = QAction(
            QIcon(os.path.join(basedir, "images", "printer.png")),
            "Print...",
            self,
        )
        print_action.setStatusTip("Print current page")
        print_action.triggered.connect(self.file_print)
        file_menu.addAction(print_action)
        file_toolbar.addAction(print_action)

        edit_toolbar = QToolBar("Edit")
        edit_toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(edit_toolbar)
        edit_menu = self.menuBar().addMenu("&Edit")

        undo_action = QAction(
            QIcon(os.path.join(basedir, "images", "arrow-curve-180-left.png")),
            "Undo",
            self,
        )
        undo_action.setStatusTip("Undo last change")
        undo_action.triggered.connect(self.editor.undo)
        edit_toolbar.addAction(undo_action)
        edit_menu.addAction(undo_action)

        redo_action = QAction(
            QIcon(os.path.join(basedir, "images", "arrow-curve.png")),
            "Redo",
            self,
        )
        redo_action.setStatusTip("Redo last change")
        redo_action.triggered.connect(self.editor.redo)
        edit_toolbar.addAction(redo_action)
        edit_menu.addAction(redo_action)

        edit_menu.addSeparator()

        cut_action = QAction(QIcon(os.path.join(basedir, "images", "scissors.png")), "Cut", self)
        cut_action.setStatusTip("Cut selected text")
        cut_action.triggered.connect(self.editor.cut)
        edit_toolbar.addAction(cut_action)
        edit_menu.addAction(cut_action)

        copy_action = QAction(
            QIcon(os.path.join(basedir, "images", "document-copy.png")),
            "Copy",
            self,
        )
        copy_action.setStatusTip("Copy selected text")
        copy_action.triggered.connect(self.editor.copy)
        edit_toolbar.addAction(copy_action)
        edit_menu.addAction(copy_action)

        paste_action = QAction(
            QIcon(os.path.join(basedir, "images", "clipboard-paste-document-text.png")),
            "Paste",
            self,
        )
        paste_action.setStatusTip("Paste from clipboard")
        paste_action.triggered.connect(self.editor.paste)
        edit_toolbar.addAction(paste_action)
        edit_menu.addAction(paste_action)

        select_action = QAction(
            QIcon(os.path.join(basedir, "images", "selection-input.png")),
            "Select all",
            self,
        )
        select_action.setStatusTip("Select all text")
        select_action.triggered.connect(self.editor.selectAll)
        edit_menu.addAction(select_action)

        edit_menu.addSeparator()

        wrap_action = QAction(
            QIcon(os.path.join(basedir, "images", "arrow-continue.png")),
            "Wrap text to window",
            self,
        )
        wrap_action.setStatusTip("Toggle wrap text to window")
        wrap_action.setCheckable(True)
        wrap_action.setChecked(True)
        wrap_action.triggered.connect(self.edit_toggle_wrap)
        edit_menu.addAction(wrap_action)

        sort_toolbar = QToolBar("Sort")
        sort_toolbar.setIconSize(QSize(14, 14))
        self.addToolBar(sort_toolbar)
        sort_menu = self.menuBar().addMenu("&Sort")

        sort_action = QAction("Sort Lines", self)
        sort_action.setStatusTip("Sort text alphabetically")
        sort_action.triggered.connect(self.sort_lines)
        sort_toolbar.addAction(sort_action)
        sort_menu.addAction(sort_action)

        self.update_title()
        self.show()

    def dialog_critical(self, s):
        dlg = QMessageBox(self)
        dlg.setText(s)
        dlg.setIcon(QMessageBox.Icon.Critical)
        dlg.show()

    def file_open(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Open file",
            "",
            "Text documents (*.txt);;All files (*.*)",
        )

        if path:
            try:
                with open(path, "rU") as f:
                    text = f.read()

            except Exception as e:
                self.dialog_critical(str(e))

            else:
                self.path = path
                self.editor.setPlainText(text)
                self.update_title()

    def file_save(self):
        if self.path is None:
            # If we do not have a path, we need to use Save As.
            return self.file_saveas()

        self._save_to_path(self.path)

    def file_saveas(self):
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Save file",
            "",
            "Text documents (*.txt);;All files (*.*)",
        )

        if not path:
            # If dialog is cancelled, will return ''
            return

        self._save_to_path(path)

    def _save_to_path(self, path):
        text = self.editor.toPlainText()
        try:
            with open(path, "w") as f:
                f.write(text)

        except Exception as e:
            self.dialog_critical(str(e))

        else:
            self.path = path
            self.update_title()

    def file_print(self):
        dlg = QPrintDialog()
        if dlg.exec():
            self.editor.print_(dlg.printer())

    def update_title(self):
        self.setWindowTitle(
            "%s - Listie" % (os.path.basename(self.path) if self.path else "Untitled")
        )

    def edit_toggle_wrap(self):
        self.editor.setLineWrapMode(1 if self.editor.lineWrapMode() == 0 else 0)

    def sort_lines(self):
        # Get current text from the QTextEdit
        current_text = self.editor.toPlainText()
        # Split text into lines
        lines = current_text.split("\n")
        # Sort lines alphabetically
        sorted_lines = sorted(lines, key=lambda line: line.lower())
        # Join lines back into a single string
        sorted_text = "\n".join(sorted_lines)
        # Set sorted text back to the QTextEdit
        self.editor.setPlainText(sorted_text)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setApplicationName("Listie")
    app.setOrganizationName("Listie")

    window = MainWindow()
    app.exec()
