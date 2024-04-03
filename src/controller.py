from typing import Dict
from fabric import Connection
from .io import IO
from .view import View


class Controller:

    view: View

    def __init__(self, io: IO, view: View):
        self.io = io
        self.view = view
        self.__init_actions()
        self.__connect_buttons_to_actions()
        self.view.show()

    def __init_actions(self):
        self.action_load_parameters = ActionLoadParameters(self)
        self.action_save_parameters = ActionSaveParameters(self)
        self.action_submit = ActionSubmit(self)

    def __connect_buttons_to_actions(self):
        for name, button in self.view.buttons.items():
            action_method = getattr(self, f'action_{name}', None)
            if action_method is not None:
                button.clicked.connect(action_method)


class Action:

    io: IO
    view: View

    def __init__(self, controller: Controller):
        self.io = controller.io
        self.view = controller.view


class ActionLoadParameters(Action):

    def __call__(self):
        file = self.view.file_dialog_open()
        if file == '':
            return

        try:
            parameters = self.io.read(file=file)
            self.view.set_parameters(parameters=parameters)
        except Exception as e:
            self.view.message_box_error(msg=str(e))


class ActionSaveParameters(Action):

    def __call__(self):
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

    view: View

    ssh_password: str
    ssh_key_values: Dict[str, str]
    qiime2_key_values: Dict[str, str]
    con: Connection
    env_cmd: str
    qiime2_cmd: str
    submit_cmd: str

    def __call__(self):

        self.ssh_password = self.view.password_dialog()
        if self.ssh_password == '':
            return

        if not self.view.message_box_yes_no(msg='Are you sure you want to submit the job?'):
            return

        try:
            self.get_key_values()
            self.set_env_cmd()
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

    def set_env_cmd(self):
        qiime2_env = self.ssh_key_values['Qiime2 Version']
        self.env_cmd = f'source ~/anaconda3/bin/activate {qiime2_env} && export QT_QPA_PLATFORM=offscreen'

    def set_qiime2_cmd(self):
        qiime2_pipeline = self.ssh_key_values['Pipeline Version']
        outdir = self.qiime2_key_values['outdir']

        args = [f'python {qiime2_pipeline}']
        for key, val in self.qiime2_key_values.items():
            if type(val) is bool:
                if val is True:
                    args.append(f'--{key}')
            else:
                args.append(f'--{key} {val}')
        args.append(f'2>&1 | tee {outdir}/progress.txt')  # `2>&1` stderr to stdout --> tee to progress.txt
        self.qiime2_cmd = ' '.join(args)

        if '"' in self.qiime2_cmd:
            print('Warning: double quotes in the Qiime2 pipeline command will be replaced by single quotes', flush=True)
            # self.qiime2_cmd will be wrapped in double quotes in self.submit_cmd
            # so double quotes needs to be avoided
            self.qiime2_cmd = self.qiime2_cmd.replace('"', '\'')

    def set_submit_cmd(self):
        sample_sheet = self.qiime2_key_values['sample-sheet']
        outdir = self.qiime2_key_values['outdir']

        self.submit_cmd = ' && '.join([
            f'mkdir -p {outdir}',
            f'cp {sample_sheet} {outdir}/',
            f'echo "{self.qiime2_cmd}" > {outdir}/command.txt',
            f'screen -dm bash -c "{self.qiime2_cmd}"'
        ])

    def connect(self):
        s = self.ssh_key_values
        self.con = Connection(
            host=s['Host'],
            user=s['User'],
            port=s['Port'],
            connect_kwargs={'password': self.ssh_password}
        )

    def submit_job(self):
        with self.con.cd(self.ROOT_DIR):
            with self.con.prefix(self.env_cmd):
                self.con.run(self.submit_cmd, echo=True)  # echo=True for printing out the command
        self.con.close()
