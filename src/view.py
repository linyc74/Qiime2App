from os.path import dirname
from typing import List, Dict, Union, Tuple
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, \
    QPushButton, QScrollArea, QCheckBox, QMessageBox, QFileDialog, QDialog, QFormLayout, \
    QLineEdit, QDialogButtonBox, QTableWidget, QTableWidgetItem


EDIT_KEY_TO_TYPE = {
    'User': QComboBox,
    'Host': QComboBox,
    'Port': QComboBox,
    'Qiime2 Pipeline': QComboBox,

    'sample-sheet': QComboBox,
    'fq-dir': QComboBox,
    'fq1-suffix': QComboBox,
    'fq2-suffix': QComboBox,
    'outdir': QComboBox,

    'feature-classifier': QComboBox,
    'nb-classifier-qza': QComboBox,
    'reference-sequence-qza': QComboBox,
    'reference-taxonomy-qza': QComboBox,
    'vsearch-classifier-max-hits': QComboBox,

    'sequencing-platform': QComboBox,

    'threads': QComboBox,

    'paired-end-mode': QComboBox,
    'skip-otu': QCheckBox,
    'otu-identity': QComboBox,
    'clip-r1-5-prime': QComboBox,
    'clip-r2-5-prime': QComboBox,
    'classifier-reads-per-batch': QComboBox,
    'max-expected-error-bases': QComboBox,
    'alpha-metrics': QComboBox,
    'beta-diversity-feature-level': QComboBox,
    'heatmap-read-fraction': QComboBox,
    'n-taxa-barplot': QComboBox,
    'colormap': QComboBox,
    'invert-colors': QCheckBox,
    'publication-figure': QCheckBox,
    'skip-differential-abundance': QCheckBox,
    'differential-abundance-p-value': QComboBox,
    'run-picrust2': QCheckBox,
}
BUTTON_KEY_TO_LABEL = {
    'illumina_mode': 'Illumina Mode',
    'pacbio_mode': 'PacBio Mode',
    'load_parameters': 'Load Parameters',
    'save_parameters': 'Save Parameters',
    'show_dashboard': 'Dashboard',
    'submit': 'Submit',
}
DASHBOARD_BUTTON_KEY_TO_LABEL = {
    'update_dashboard': 'Update',
    'kill_jobs': 'Kill Jobs',
}


class IlluminaMode:
    NAME = 'Illumina Mode'
    SSH_KEY_TO_VALUES: Dict[str, Union[List[str], bool]] = {
        'User': [''],
        'Host': ['255.255.255.255'],
        'Port': ['22'],
        'Qiime2 Pipeline': ['qiime2_pipeline-2.10.2'],
    }
    QIIME2_KEY_TO_VALUES: Dict[str, Union[List[str], bool]] = {
        'sample-sheet': ['sample-sheet.csv'],
        'fq-dir': ['data'],
        'fq1-suffix': ['_R1.fastq.gz'],
        'fq2-suffix': ['_R2.fastq.gz'],
        'outdir': ['output'],

        'feature-classifier': ['nb', 'vsearch'],
        'nb-classifier-qza': ['silva-138-99-nb-classifier.qza'],
        'reference-sequence-qza': ['silva-138-99-seqs.qza'],
        'reference-taxonomy-qza': ['silva-138-99-tax.qza'],
        'vsearch-classifier-max-hits': ['10'],

        'sequencing-platform': ['illumina'],

        'threads': ['1', '4', '8'],

        'paired-end-mode': ['merge', 'pool'],
        'skip-otu': False,
        'otu-identity': ['0.97'],
        'clip-r1-5-prime': ['17'],
        'clip-r2-5-prime': ['20'],
        'classifier-reads-per-batch': ['1000'],
        'max-expected-error-bases': ['8.0'],
        'alpha-metrics': ['all'],
        'beta-diversity-feature-level': ['feature', 'species', 'genus', 'family', 'order', 'class', 'phylum'],
        'heatmap-read-fraction': ['0.95'],
        'n-taxa-barplot': ['20'],
        'colormap': ['Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2'],
        'invert-colors': False,
        'publication-figure': False,
        'skip-differential-abundance': False,
        'differential-abundance-p-value': ['0.05'],
        'run-picrust2': False,
    }
    BUTTON_KEYS = [
        'pacbio_mode',
        'load_parameters',
        'save_parameters',
        'show_dashboard',
        'submit',
    ]


class PacBioMode:
    NAME = 'PacBio Mode'
    SSH_KEY_TO_VALUES: Dict[str, Union[List[str], bool]] = {
        'User': [''],
        'Host': ['255.255.255.255'],
        'Port': ['22'],
        'Qiime2 Pipeline': ['qiime2_pipeline-2.10.2'],
    }
    QIIME2_KEY_TO_VALUES: Dict[str, Union[List[str], bool]] = {
        'sample-sheet': ['sample-sheet.csv'],
        'fq-dir': ['data'],
        'fq1-suffix': ['.fastq.gz'],
        'outdir': ['output'],

        'feature-classifier': ['nb', 'vsearch'],
        'nb-classifier-qza': ['silva-138-99-nb-classifier.qza'],
        'reference-sequence-qza': ['silva-138-99-seqs.qza'],
        'reference-taxonomy-qza': ['silva-138-99-tax.qza'],
        'vsearch-classifier-max-hits': ['10'],

        'sequencing-platform': ['pacbio'],

        'threads': ['1', '4', '8'],

        'skip-otu': False,
        'otu-identity': ['0.97'],
        'classifier-reads-per-batch': ['1000'],
        'max-expected-error-bases': ['8.0'],
        'alpha-metrics': ['all'],
        'beta-diversity-feature-level': ['feature', 'species', 'genus', 'family', 'order', 'class', 'phylum'],
        'heatmap-read-fraction': ['0.95'],
        'n-taxa-barplot': ['20'],
        'colormap': ['Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2'],
        'invert-colors': False,
        'publication-figure': False,
        'skip-differential-abundance': False,
        'differential-abundance-p-value': ['0.05'],
        'run-picrust2': False,
    }
    BUTTON_KEYS = [
        'illumina_mode',
        'load_parameters',
        'save_parameters',
        'show_dashboard',
        'submit',
    ]


class Edit:

    key: str
    qlabel: QLabel
    qedit: Union[QComboBox, QCheckBox]

    def __init__(self, key: str, qlabel: QLabel, qedit: Union[QComboBox, QCheckBox]):
        self.key = key
        self.qlabel = qlabel
        self.qedit = qedit


class Button:

    key: str
    qbutton: QPushButton

    def __init__(self, key: str, qbutton: QPushButton):
        self.key = key
        self.qbutton = qbutton


class Dashboard(QWidget):

    TITLE = 'Dashboard'
    ICON_FILE = 'icon/logo.ico'
    WIDTH, HEIGHT = 800, 600

    vertical_layout: QVBoxLayout
    table: QTableWidget
    button_layout: QHBoxLayout
    buttons: List[Button]

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.TITLE)
        self.setWindowIcon(QIcon(f'{dirname(dirname(__file__))}/{self.ICON_FILE}'))
        self.resize(self.WIDTH, self.HEIGHT)

        self.vertical_layout = QVBoxLayout()
        self.setLayout(self.vertical_layout)

        self.table = QTableWidget(parent=self)
        self.vertical_layout.addWidget(self.table)

        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch(1)
        self.vertical_layout.addLayout(self.button_layout)

        self.buttons = []
        for key, label in DASHBOARD_BUTTON_KEY_TO_LABEL.items():
            qbutton = QPushButton(label, self)
            self.button_layout.addWidget(qbutton)
            button = Button(key=key, qbutton=qbutton)
            self.buttons.append(button)

        self.display_jobs(jobs=[])

    def display_jobs(self, jobs: List[Tuple[str, str, str]]):
        columns = ['Job ID', 'Start Time', 'Elapsed Time']
        self.table.setRowCount(len(jobs))
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)

        for row, job in enumerate(jobs):
            job_id, start_time, elapsed_time = job
            for col, text in enumerate([job_id, start_time, elapsed_time]):
                item = QTableWidgetItem(text)
                item.setFlags(item.flags() & ~Qt.ItemIsEditable)  # makes the item immutable, i.e. user cannot edit it
                self.table.setItem(row, col, item)

        self.table.resizeColumnsToContents()

    def get_selected_job_ids(self) -> List[str]:
        selected_rows = []
        for item in self.table.selectedItems():
            row = item.row()
            if row not in selected_rows:
                selected_rows.append(row)

        job_ids = [
            self.table.item(row, 0).text()  # column 0 is the job_id
            for row in selected_rows
        ]
        return job_ids


class View(QWidget):

    TITLE = 'Qiime2 App'
    ICON_FILE = 'icon/logo.ico'
    WIDTH, HEIGHT = 1000, 1000

    edits: List[Edit]
    buttons: List[Button]
    dashboard: Dashboard

    question_layout: QVBoxLayout
    button_layout: QHBoxLayout
    scroll_area: QScrollArea
    scroll_contents: QWidget
    main_layout: QVBoxLayout
    dashboard: Dashboard

    mode: Union[IlluminaMode, PacBioMode]

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon(f'{dirname(dirname(__file__))}/{self.ICON_FILE}'))
        self.resize(self.WIDTH, self.HEIGHT)

        self.__init_edits()
        self.__init_buttons()
        self.dashboard = Dashboard()

        self.__init_question_layout()
        self.__init_button_layout()
        self.__init_scroll_area_and_contents()
        self.__init_main_layout()

        self.__init_ui_methods()

        self.show_illumina_mode()

    def __init_edits(self):
        self.edits = []
        for key, type_ in EDIT_KEY_TO_TYPE.items():
            qlabel = QLabel(f'{key}:', self)

            if type_ is QCheckBox:
                qedit = QCheckBox(self)
            else:
                qedit = QComboBox(self)
                qedit.setEditable(True)

            qlabel.hide()  # hide by default, show it later depending on the mode
            qedit.hide()

            edit = Edit(key=key, qlabel=qlabel, qedit=qedit)
            self.edits.append(edit)

    def __init_buttons(self):
        self.buttons = []
        for key, label in BUTTON_KEY_TO_LABEL.items():
            qbutton = QPushButton(label, self)
            qbutton.hide()
            button = Button(key=key, qbutton=qbutton)
            self.buttons.append(button)

    def __init_question_layout(self):
        self.question_layout = QVBoxLayout()
        for edit in self.edits:
            self.question_layout.addWidget(edit.qlabel)
            self.question_layout.addWidget(edit.qedit)

    def __init_button_layout(self):
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch(1)
        self.question_layout.addLayout(self.button_layout)
        for button in self.buttons:
            self.button_layout.addWidget(button.qbutton)

    def __init_scroll_area_and_contents(self):
        self.scroll_area = QScrollArea(self)
        self.scroll_contents = QWidget(self.scroll_area)  # the QWidget with all items
        self.scroll_contents.setLayout(self.question_layout)
        self.scroll_area.setWidget(self.scroll_contents)  # set the scroll_area's widget to be scroll_contents
        self.scroll_area.setWidgetResizable(True)

    def __init_main_layout(self):
        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.scroll_area)  # add scroll_area to the main_layout
        self.setLayout(self.main_layout)

    def __init_ui_methods(self):
        self.message_box_info = MessageBoxInfo(self)
        self.message_box_error = MessageBoxError(self)
        self.message_box_yes_no = MessageBoxYesNo(self)
        self.file_dialog_open = FileDialogOpen(self)
        self.file_dialog_save = FileDialogSave(self)
        self.password_dialog = PasswordDialog(self)

    def show_illumina_mode(self):
        self.mode = IlluminaMode()
        self.__show_mode()

    def show_pacbio_mode(self):
        self.mode = PacBioMode()
        self.__show_mode()

    def __show_mode(self):

        self.setWindowTitle(f'{self.TITLE} - {self.mode.NAME}')

        key_to_values: Dict[str, Union[List[str], bool]]
        key_to_values = {**self.mode.SSH_KEY_TO_VALUES, **self.mode.QIIME2_KEY_TO_VALUES}  # combine the two dictionaries

        for edit in self.edits:

            values = key_to_values.get(edit.key, None)

            if values is None:  # key not in the current mode
                edit.qlabel.hide()
                edit.qedit.hide()
                continue

            if type(edit.qedit) is QComboBox:
                edit.qedit.clear()
                edit.qedit.addItems(values)  # values is a list of strings for QComboBox
            elif type(edit.qedit) is QCheckBox:
                edit.qedit.setChecked(values)  # values is a boolean for QCheckBox

            edit.qlabel.show()
            edit.qedit.show()

        for button in self.buttons:
            if button.key in self.mode.BUTTON_KEYS:
                button.qbutton.show()
            else:
                button.qbutton.hide()

    def get_key_values(self) -> Dict[str, Union[str, bool]]:
        keys = list(self.mode.SSH_KEY_TO_VALUES.keys()) + list(self.mode.QIIME2_KEY_TO_VALUES.keys())
        return self.__get_key_values(keys=keys)

    def get_ssh_key_values(self) -> Dict[str, Union[str, bool]]:
        keys = list(self.mode.SSH_KEY_TO_VALUES.keys())
        return self.__get_key_values(keys=keys)

    def get_qiime2_key_values(self) -> Dict[str, Union[str, bool]]:
        keys = list(self.mode.QIIME2_KEY_TO_VALUES.keys())
        return self.__get_key_values(keys=keys)

    def __get_key_values(self, keys: List[str]) -> Dict[str, str]:
        ret = {}

        for edit in self.edits:
            if edit.key not in keys:
                continue

            e = edit.qedit
            if e.isHidden():
                continue

            if type(e) is QComboBox:
                ret[edit.key] = e.currentText()
            elif type(e) is QCheckBox:
                ret[edit.key] = e.isChecked()

        return ret

    def set_parameters(self, parameters: Dict[str, Union[str, bool]]):
        # Reset all visible flags to False because
        #   when a flag is not present in parameters, it should be False
        for edit in self.edits:
            e = edit.qedit
            if e.isHidden():
                continue
            if type(e) is QCheckBox:
                e.setChecked(False)

        for edit in self.edits:
            e = edit.qedit
            if e.isHidden():
                continue

            val = parameters.get(edit.key, None)
            if val is None:
                continue

            if type(e) is QComboBox:
                e.setCurrentText(val)
            elif type(e) is QCheckBox:
                e.setChecked(True)  # when the key if present, the flag should be True

    def get_all_buttons(self) -> List[Button]:
        return self.buttons + self.dashboard.buttons

    def show_dashboard(self):
        self.dashboard.show()
        self.dashboard.raise_()
        self.dashboard.activateWindow()

    def display_jobs(self, jobs: List[Tuple[str, str, str]]):
        self.dashboard.display_jobs(jobs)
        self.dashboard.raise_()
        self.dashboard.activateWindow()

    def closeEvent(self, event):
        self.dashboard.close()


#


class MessageBox:

    TITLE: str
    ICON: QMessageBox.Icon

    box: QMessageBox

    def __init__(self, parent: QWidget):
        self.box = QMessageBox(parent)
        self.box.setWindowTitle(self.TITLE)
        self.box.setIcon(self.ICON)

    def __call__(self, msg: str):
        self.box.setText(msg)
        self.box.exec_()


class MessageBoxInfo(MessageBox):

    TITLE = 'Info'
    ICON = QMessageBox.Information


class MessageBoxError(MessageBox):

    TITLE = 'Error'
    ICON = QMessageBox.Warning


class MessageBoxYesNo(MessageBox):

    TITLE = ' '
    ICON = QMessageBox.Question

    def __init__(self, parent: QWidget):
        super(MessageBoxYesNo, self).__init__(parent)
        self.box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        self.box.setDefaultButton(QMessageBox.No)

    def __call__(self, msg: str) -> bool:
        self.box.setText(msg)
        return self.box.exec_() == QMessageBox.Yes


#


class FileDialog:

    parent: QWidget

    def __init__(self, parent: QWidget):
        self.parent = parent


class FileDialogOpen(FileDialog):

    def __call__(self) -> str:
        d = QFileDialog(self.parent)
        d.resize(1200, 800)
        d.setWindowTitle('Open')
        d.setNameFilter('All Files (*.*);;CSV files (*.csv);;TSV files (*.tsv);;tab files (*.tab);;TXT files (*.txt)')
        d.selectNameFilter('CSV files (*.csv)')
        d.setOptions(QFileDialog.DontUseNativeDialog)
        d.setFileMode(QFileDialog.ExistingFile)  # only one existing file can be selected
        d.exec_()
        selected = d.selectedFiles()
        return selected[0] if len(selected) > 0 else ''


class FileDialogSave(FileDialog):

    def __call__(self, filename: str = '') -> str:
        d = QFileDialog(self.parent)
        d.resize(1200, 800)
        d.setWindowTitle('Save As')
        d.selectFile(filename)
        d.setNameFilter('All Files (*.*);;CSV files (*.csv);;TSV files (*.tsv);;tab files (*.tab);;TXT files (*.txt)')
        d.selectNameFilter('CSV files (*.csv)')
        d.setOptions(QFileDialog.DontUseNativeDialog)
        d.setAcceptMode(QFileDialog.AcceptSave)

        ret = ''  # default, no file object selected and accepted
        accepted = d.exec_()
        if accepted:
            files = d.selectedFiles()
            name_filter = d.selectedNameFilter()
            ext = name_filter.split('(*')[-1].split(')')[0]  # e.g. 'CSV files (*.csv)' -> '.csv'
            if len(files) > 0:
                ret = files[0]
                if not ret.endswith(ext):  # add file extension if not present
                    ret += ext
        return ret


#


class PasswordDialog:

    LINE_TITLE = 'Password:'
    LINE_DEFAULT = ''

    parent: QWidget

    dialog: QDialog
    layout: QFormLayout
    line_edit: QLineEdit
    button_box: QDialogButtonBox

    def __init__(self, parent: QWidget):
        self.parent = parent
        self.__init_dialog()
        self.__init_layout()
        self.__init_line_edit()
        self.__init_button_box()

    def __init_dialog(self):
        self.dialog = QDialog(parent=self.parent)
        self.dialog.setWindowTitle(' ')

    def __init_layout(self):
        self.layout = QFormLayout(parent=self.dialog)

    def __init_line_edit(self):
        self.line_edit = QLineEdit(self.LINE_DEFAULT, parent=self.dialog)
        self.line_edit.setEchoMode(QLineEdit.Password)
        self.layout.addRow(self.LINE_TITLE, self.line_edit)

    def __init_button_box(self):
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self.dialog)
        self.button_box.accepted.connect(self.dialog.accept)
        self.button_box.rejected.connect(self.dialog.reject)
        self.layout.addWidget(self.button_box)

    def __call__(self) -> Union[str, tuple]:
        if self.dialog.exec_() == QDialog.Accepted:
            return self.line_edit.text()
        else:
            return ''
