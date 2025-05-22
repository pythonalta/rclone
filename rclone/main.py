import os
import json
import subprocess
from pathlib import Path

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

    def ls(self, bucket="", path=""):
        rclone_path = f'{self.remote}:{bucket}/{path}'
        envs, command = self.cmd(command=f'lsjson {rclone_path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not list files: {err}')
        if out:
            return json.loads(out)

    def lsd(self, bucket="", path=""):
        rclone_path = f'{self.remote}:{bucket}/{path}'
        envs, command = self.cmd(command=f'lsjson --dirs-only {rclone_path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not list the directories: {err}')
        if out:
            return json.loads(out)

    def lsf(self, bucket="", path=""):
        rclone_path = f'{self.remote}:{bucket}/{path}'
        envs, command = self.cmd(command=f'lsjson --files-only {rclone_path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not list the files: {err}')
        if out:
            return json.loads(out)

    def exists(self, bucket="", path=""):
        try:
            rclone_path = f'{self.remote}:{bucket}/{path}'
            envs, command = self.cmd(command=f'lsjson {rclone_path}')
            err, out = Rclone.__run(command=command, envs=envs)
            if err:
                return False
            elif out:
                return True
            else:
                return False
        except RCloneErr as e:
            return False

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

    def mkd(self, bucket="", path=""):
        rclone_path = f'{self.remote}:{bucket}/{path}'
        envs, command = self.cmd(command=f'mkdir {rclone_path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not create the directory: {err}')
        if out:
            print(out)

    def rm(self, bucket="", path=""):
        rclone_path = f'{self.remote}:{bucket}/{path}'
        envs, command = self.cmd(command=f'delete {rclone_path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not remove files: {err}')
        if out:
            print(out)

    def rmd(self, bucket="", path=""):
        rclone_path = f'{self.remote}:{bucket}/{path}'
        envs, command = self.cmd(command=f'delete --rmdirs {rclone_path}')
        err, out = Rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not remove files: {err}')
        if out:
            print(out)
