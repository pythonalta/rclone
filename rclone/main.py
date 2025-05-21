import os
import json
import subprocess

class RCloneErr(Exception):
    def __init__(self, message=""):
        super().__init__(message)

class rclone:
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

    def cmd(access_id="", access_secret="", remote="", command="", conf_file="rclone.conf"):
        envs = {
            f'RCLONE_CONFIG_{remote.upper()}_ACCESS_KEY_ID': access_id,
            f'RCLONE_CONFIG_{remote.upper()}_SECRET_ACCESS_KEY': access_secret
        }
        core_cmd = f'rclone --config {conf_file} {command}'
        return envs, core_cmd

    def mkd(access_id="", access_secret="", remote="", path="", conf_file="rclone.conf"):
        envs, command = rclone.cmd(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            command=f'mkdir {path}',
            conf_file=conf_file
        )
        err, out = rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not create the directory: {err}')
        if out:
            print(out)

    def ls(access_id="", access_secret="", remote="", path="", conf_file="rclone.conf"):
        envs, command = rclone.cmd(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            command=f'lsjson {path}',
            conf_file=conf_file
        )
        err, out = rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not list files: {err}')
        if out:
            return json.loads(out)

    def lsd(access_id="", access_secret="", remote="", path="", conf_file="rclone.conf"):
        envs, command = rclone.cmd(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            command=f'lsjson --dirs-only {path}',
            conf_file=conf_file
        )
        err, out = rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not list the directories: {err}')
        if out:
            return json.loads(out)

    def lsf(access_id="", access_secret="", remote="", path="", conf_file="rclone.conf"):
        envs, command = rclone.cmd(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            command=f'lsjson --files-only {path}',
            conf_file=conf_file
        )
        err, out = rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not list the files: {err}')
        if out:
            return json.loads(out)

    def cp(access_id="", access_secret="", remote="", source="", target="", conf_file="rclone.conf", public=False):
        acl = ""
        if public:
            acl = "--s3-acl public-read"
        envs, command = rclone.cmd(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            command=f'copy {source} {target} {acl}',
            conf_file=conf_file
        )
        err, out = rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not copy files: {err}')
        if out:
            print(out)

    def mv(access_id="", access_secret="", remote="", source="", target="", conf_file="rclone.conf", public=False):
        acl = ""
        if public:
            acl = "--s3-acl public-read"
        envs, command = rclone.cmd(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            command=f'moveto {source} {target} {acl}',
            conf_file=conf_file
        )
        err, out = rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not move files: {err}')
        if out:
            print(out)

    def mvf(access_id="", access_secret="", remote="", source="", target="", conf_file="rclone.conf", public=False):
        acl = ""
        if public:
            acl = "--s3-acl public-read"
        envs, command = rclone.cmd(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            command=f'move {source} {target} {acl}',
            conf_file=conf_file
        )
        err, out = rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not move files: {err}')
        if out:
            print(out)

    def exists(access_id="", access_secret="", remote="", path="", name="", conf_file="rclone.conf"):
        files = rclone.ls(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            path=path,
            conf_file=conf_file
        )
        if not files:
            return False
        for file in files:
            if file["Name"] == name:
                return True
        return False

    def rm(access_id="", access_secret="", remote="", path="", conf_file="rclone.conf"):
        envs, command = rclone.cmd(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            command=f'delete {path}',
            conf_file=conf_file
        )
        err, out = rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not remove files: {err}')
        if out:
            print(out)

    def rmd(access_id="", access_secret="", remote="", path="", conf_file="rclone.conf"):
        envs, command = rclone.cmd(
            access_id=access_id,
            access_secret=access_secret,
            remote=remote,
            command=f'delete --rmdirs {path}',
            conf_file=conf_file
        )
        err, out = rclone.__run(command=command, envs=envs)
        if err:
            raise RCloneErr(f'Could not remove files: {err}')
        if out:
            print(out)
