import os
import json
import subprocess

class RCloneErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class Rclone:
    def __init__(self, access_id="", access_secret="", remote="", conf_file=""):
        self.access_id = access_id
        self.access_secret = access_secret
        self.remote = remote
        self.conf_file = conf_file

    def __run(command="", cwd=None, envs=None, **kargs):
        cmd_list = command.split()
        env = os.environ.copy()
        if envs:
            env.update(envs)
        try:
            process = subprocess.run(
                cmd_list,
                cwd=cwd,
                capture_output=True,
                text=True,
                env=env,
                check=True
            )
            return process.stderr, process.stdout
        except subprocess.CalledProcessError as e:
            return e.stderr, e.stdout

    def cmd(self, command=""):
        envs = {
            f'RCLONE_CONFIG_{self.remote.upper()}_ACCESS_KEY_ID': self.access_id,
            f'RCLONE_CONFIG_{self.remote.upper()}_SECRET_ACCESS_KEY': self.access_secret
        }
        core_cmd = f'rclone --config {self.conf_file} {command}'
        return envs, core_cmd

    def exec(self, command=""):
        envs, command_ = self.cmd(command=command)
        err, out = Rclone.__run(command=command_, envs=envs)
        if err:
            raise RCloneErr(f'Could not create the directory: {err}')
        if out:
            print(out)

    def mkd(self, path=""):
        envs, command = self.cmd(command=f'mkdir {path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not create the directory: {err}')
        if out:
            print(out)

    def ls(self, path=""):
        envs, command = self.cmd(command=f'lsjson {path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not list files: {err}')
        if out:
            return json.loads(out)

    def lsd(self, path=""):
        envs, command = self.cmd(command=f'lsjson --dirs-only {path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not list the directories: {err}')
        if out:
            return json.loads(out)

    def lsf(self, path=""):
        envs, command = self.cmd(command=f'lsjson --files-only {path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not list the files: {err}')
        if out:
            return json.loads(out)

    def cp(self, source="", target="", public=False):
        acl = ""
        if public:
            acl = "--s3-acl public-read"
        envs, command = self.cmd(command=f'copy {source} {target} {acl}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not copy files: {err}')
        if out:
            print(out)

    def mv(self, source="", target="", public=False):
        acl = ""
        if public:
            acl = "--s3-acl public-read"
        envs, command = self.cmd(command=f'moveto {source} {target} {acl}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not move files: {err}')
        if out:
            print(out)

    def mvf(self, source="", target="", public=False):
        acl = ""
        if public:
            acl = "--s3-acl public-read"
        envs, command = self.cmd(command=f'move {source} {target} {acl}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not move files: {err}')
        if out:
            print(out)

    def exists(self, dir_path="", name=""):
        files = self.ls(path=dir_path)
        if not files:
            return False
        for file in files:
            if file["Name"] == name:
                return True
        return False

    def rm(self, path=""):
        envs, command = self.cmd(command=f'delete {path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not remove files: {err}')
        if out:
            print(out)

    def rmd(self, path=""):
        envs, command = self.cmd(command=f'delete --rmdirs {path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not remove files: {err}')
        if out:
            print(out)
