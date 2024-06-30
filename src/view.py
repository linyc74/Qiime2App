from os.path import dirname
from typing import List, Tuple, Dict, Union
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, \
    QPushButton, QScrollArea, QCheckBox, QMessageBox, QFileDialog, QDialog, QFormLayout, \
    QLineEdit, QDialogButtonBox


DEFAULT_KEY_VALUES = {
    'User': [''],
    'Host': ['255.255.255.255'],
    'Port': ['22'],
    'Qiime2 Pipeline': ['qiime2_pipeline-2.3.0'],

    'sample-sheet': ['sample-sheet.csv'],
    'fq-dir': ['data'],
    'fq1-suffix': ['_R1.fastq.gz'],
    'fq2-suffix': ['_R2.fastq.gz'],
    'nb-classifier-qza': ['silva-138-99-nb-classifier.qza'],
    'outdir': ['output'],
    'paired-end-mode': ['merge', 'pool'],
    'skip-otu': False,
    'classifier-reads-per-batch': ['1000'],
    'alpha-metrics': ['all'],
    'clip-r1-5-prime': ['17'],
    'clip-r2-5-prime': ['20'],
    'max-expected-error-bases': ['8.0'],
    'heatmap-read-fraction': ['0.95'],
    'n-taxa-barplot': ['20'],
    'beta-diversity-feature-level': ['feature', 'species', 'genus', 'family', 'order', 'class', 'phylum'],
    'colormap': ['Set1', 'Set2', 'Set3', 'tab10', 'tab20', 'tab20b', 'tab20c', 'Pastel1', 'Pastel2', 'Paired', 'Accent', 'Dark2'],
    'invert-colors': False,
    'publication-figure': False,
    'skip-differential-abundance': False,
    'run-picrust2': True,
    'threads': ['1', '4', '8'],
}
BUTTON_NAME_TO_LABEL = {
    'basic_mode': 'Basic Mode',
    'advanced_mode': 'Advanced Mode',
    'load_parameters': 'Load Parameters',
    'save_parameters': 'Save Parameters',
    'submit': 'Submit',
}


class BasicMode:
    SSH_KEYS = [
        'User',
        'Host',
        'Port',
        'Qiime2 Pipeline',
    ]
    QIIME2_KEYS = [
        'sample-sheet',
        'fq-dir',
        'fq1-suffix',
        'fq2-suffix',
        'nb-classifier-qza',
        'outdir',
    ]
    BUTTON_NAMES = [
        'advanced_mode',
        'load_parameters',
        'save_parameters',
        'submit',
    ]


class AdvancedMode:
    SSH_KEYS = [
        'User',
        'Host',
        'Port',
        'Qiime2 Pipeline',
    ]
    QIIME2_KEYS = [
        'sample-sheet',
        'fq-dir',
        'fq1-suffix',
        'fq2-suffix',
        'nb-classifier-qza',
        'outdir',
        'paired-end-mode',
        'skip-otu',
        'classifier-reads-per-batch',
        'alpha-metrics',
        'clip-r1-5-prime',
        'clip-r2-5-prime',
        'max-expected-error-bases',
        'heatmap-read-fraction',
        'n-taxa-barplot',
        'beta-diversity-feature-level',
        'colormap',
        'invert-colors',
        'publication-figure',
        'skip-differential-abundance',
        'run-picrust2',
        'threads',
    ]
    BUTTON_NAMES = [
        'basic_mode',
        'load_parameters',
        'save_parameters',
        'submit',
    ]


class View(QWidget):

    TITLE = 'Qiime2 App'
    ICON_FILE = 'icon/logo.ico'
    WIDTH, HEIGHT = 800, 1000

    # UI items
    label_combo_pairs: List[Tuple[QLabel, QComboBox]]
    buttons: Dict[str, QPushButton]

    # UI layouts
    question_layout: QVBoxLayout
    button_layout: QHBoxLayout
    scroll_area: QScrollArea
    scroll_contents: QWidget
    main_layout: QVBoxLayout

    mode: Union[BasicMode, AdvancedMode]
    shown_label_combo_pairs: List[Tuple[QLabel, QComboBox]]

    def __init__(self):
        super().__init__()
        self.setWindowTitle(self.TITLE)
        self.setWindowIcon(QIcon(f'{dirname(dirname(__file__))}/{self.ICON_FILE}'))
        self.resize(self.WIDTH, self.HEIGHT)

        self.__init_label_combo_pairs()
        self.__init_buttons()

        self.__init_question_layout()
        self.__init_button_layout()
        self.__init_scroll_area_and_contents()
        self.__init_main_layout()

        self.__init_ui_methods()

        self.show_basic_mode()

    def __init_label_combo_pairs(self):
        self.label_combo_pairs = []
        for key, values in DEFAULT_KEY_VALUES.items():
            label = QLabel(f'{key}:', self)

            if type(values) is bool:
                combo = QCheckBox(self)
                combo.setChecked(values)
            else:
                combo = QComboBox(self)
                combo.addItems(values)
                combo.setEditable(True)

            label.hide()
            combo.hide()

            self.label_combo_pairs.append((label, combo))

    def __init_buttons(self):
        self.buttons = dict()
        for name, label in BUTTON_NAME_TO_LABEL.items():
            button = QPushButton(label, self)
            self.buttons[name] = button
            button.hide()

    def __init_question_layout(self):
        self.question_layout = QVBoxLayout()
        for label, combo in self.label_combo_pairs:
            self.question_layout.addWidget(label)
            self.question_layout.addWidget(combo)

    def __init_button_layout(self):
        self.button_layout = QHBoxLayout()
        self.button_layout.addStretch(1)
        self.question_layout.addLayout(self.button_layout)
        for button in self.buttons.values():
            self.button_layout.addWidget(button)

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

    def show_basic_mode(self):
        self.mode = BasicMode()
        self.__show_mode()

    def show_advanced_mode(self):
        self.mode = AdvancedMode()
        self.__show_mode()

    def __show_mode(self):
        self.shown_label_combo_pairs = []

        for label, combo in self.label_combo_pairs:
            key = label.text()[:-1]
            if key in self.mode.QIIME2_KEYS + self.mode.SSH_KEYS:
                label.show()
                combo.show()
                self.shown_label_combo_pairs.append((label, combo))
            else:
                label.hide()
                combo.hide()

        for name, button in self.buttons.items():
            if name in self.mode.BUTTON_NAMES:
                button.show()
            else:
                button.hide()

    def get_key_values(self) -> Dict[str, Union[str, bool]]:
        return self.__get_key_values(keys=self.mode.SSH_KEYS + self.mode.QIIME2_KEYS)

    def get_ssh_key_values(self) -> Dict[str, Union[str, bool]]:
        return self.__get_key_values(keys=self.mode.SSH_KEYS)

    def get_qiime2_key_values(self) -> Dict[str, Union[str, bool]]:
        return self.__get_key_values(keys=self.mode.QIIME2_KEYS)

    def __get_key_values(self, keys: List[str]) -> Dict[str, str]:
        ret = {}
        for label, item in self.shown_label_combo_pairs:
            k = label.text()[:-1]
            if k not in keys:
                continue
            if type(item) is QComboBox:
                ret[k] = item.currentText()
            elif type(item) is QCheckBox:
                ret[k] = item.isChecked()
        return ret

    def set_parameters(self, parameters: Dict[str, Union[str, bool]]):
        # Reset flags to False because
        #   when a flag is not present in parameters, it should be False
        for _, combo in self.shown_label_combo_pairs:
            if type(combo) is QCheckBox:
                combo.setChecked(False)

        for key, val in parameters.items():
            for label, combo in self.shown_label_combo_pairs:
                if label.text()[:-1] == key:
                    if type(combo) is QComboBox:
                        combo.setCurrentText(val)
                    elif type(combo) is QCheckBox:
                        combo.setChecked(True)  # when the key if present, the flag should be True


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
        d.exec_()

        files = d.selectedFiles()

        name_filter = d.selectedNameFilter()
        ext = name_filter.split('(*')[-1].split(')')[0]  # e.g. 'CSV files (*.csv)' -> '.csv'

        if len(files) == 0:
            ret = ''
        else:
            ret = files[0]
            if not ret.endswith(ext):  # add file extension if not present
                ret += ext

        return ret


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
