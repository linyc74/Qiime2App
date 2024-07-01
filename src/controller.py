from typing import Dict
from os.path import basename
from fabric import Connection
from .io import IO
from .view import View


class Controller:

    view: View

    def __init__(self, io: IO, view: View):
        self.io = io
        self.view = view
        self.__connect_buttons_to_actions()
        self.view.show()

    def __connect_buttons_to_actions(self):
        for button in self.view.button_dict.values():
            key = button.key
            qbutton = button.qbutton
            action_method = getattr(self, f'action_{key}', None)
            if action_method is not None:
                qbutton.clicked.connect(action_method)

    def action_basic_mode(self):
        self.view.show_basic_mode()

    def action_advanced_mode(self):
        self.view.show_advanced_mode()

    def action_load_parameters(self):
        ActionLoadParameters(self).exec()

    def action_save_parameters(self):
        ActionSaveParameters(self).exec()

    def action_submit(self):
        ActionSubmit(self).exec()


class Action:

    io: IO
    view: View

    def __init__(self, controller: Controller):
        self.io = controller.io
        self.view = controller.view


class ActionLoadParameters(Action):

    def exec(self):
        file = self.view.file_dialog_open()
        if file == '':
            return

        try:
            parameters = self.io.read(file=file)
            self.view.set_parameters(parameters=parameters)
        except Exception as e:
            self.view.message_box_error(msg=str(e))


class ActionSaveParameters(Action):

    def exec(self):
        file = self.view.file_dialog_save()
        if file == '':
            return

        try:
            parameters = self.view.get_key_values()
            self.io.write(file=file, parameters=parameters)
        except Exception as e:
            self.view.message_box_error(msg=str(e))


class ActionSubmit(Action):

    ROOT_DIR = '~/Qiime2App'
    BASH_PROFILE = '.bash_profile'

    view: View

    ssh_password: str
    ssh_key_values: Dict[str, str]
    qiime2_key_values: Dict[str, str]
    con: Connection
    qiime2_cmd: str
    submit_cmd: str

    def exec(self):

        self.ssh_password = self.view.password_dialog()
        if self.ssh_password == '':
            return

        if not self.view.message_box_yes_no(msg='Are you sure you want to submit the job?'):
            return

        try:
            self.get_key_values()
            self.set_qiime2_cmd()
            self.set_submit_cmd()
            self.connect()
            self.submit_job()
            self.view.message_box_info(msg='Job submitted!')

        except Exception as e:
            self.view.message_box_error(msg=str(e))

    def get_key_values(self):
        self.ssh_key_values = self.view.get_ssh_key_values()
        self.qiime2_key_values = self.view.get_qiime2_key_values()

    def set_qiime2_cmd(self):
        qiime2_pipeline = self.ssh_key_values['Qiime2 Pipeline']
        outdir = self.qiime2_key_values['outdir']

        args = [f'python {qiime2_pipeline}']
        for key, val in self.qiime2_key_values.items():
            if type(val) is bool:
                if val is True:
                    args.append(f'--{key}')

            else:  # val is string
                args.append(f"--{key}='{val}'")

        args.append(f'2>&1 | tee {outdir}/progress.txt')  # `2>&1` stderr to stdout --> tee to progress.txt

        self.qiime2_cmd = ' '.join(args)

        if '"' in self.qiime2_cmd:
            print('Warning: double quotes in the Qiime2 pipeline command will be replaced by single quotes', flush=True)
            # self.qiime2_cmd will be wrapped in double quotes in self.submit_cmd
            # so double quotes needs to be avoided
            self.qiime2_cmd = self.qiime2_cmd.replace('"', '\'')

    def set_submit_cmd(self):
        outdir = self.qiime2_key_values['outdir']
        job_name = basename(outdir).replace(' ', '_')
        sample_sheet = self.qiime2_key_values['sample-sheet']

        # the environment (.bash_profile) needs to be activated right before the qiime2_cmd
        script = f'source {self.BASH_PROFILE} && {self.qiime2_cmd}'
        cmd_txt = f'{outdir}/command.txt'

        self.submit_cmd = ' && '.join([
            f'mkdir -p "{outdir}"',
            f'cp "{sample_sheet}" "{outdir}/"',
            f'echo "{script}" > "{cmd_txt}"',
            f'screen -dm -S {job_name} bash "{cmd_txt}"'
        ])

    def connect(self):
        s = self.ssh_key_values
        self.con = Connection(
            host=s['Host'],
            user=s['User'],
            port=int(s['Port']),
            connect_kwargs={'password': self.ssh_password}
        )

    def submit_job(self):
        with self.con.cd(self.ROOT_DIR):
            self.con.run(self.submit_cmd, echo=True)  # echo=True for printing out the command
        self.con.close()
