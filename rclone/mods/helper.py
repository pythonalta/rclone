import os
import subprocess

def cmd_(api_key, api_secret, remote, cmd, conf_file="rclone.conf"):
    envs = {
        f'RCLONE_CONFIG_{up(remote)}_ACCESS_KEY_ID': api_key,
        f'RCLONE_CONFIG_{up(remote)}_SECRET_ACCESS_KEY': api_secret
    }
    core_cmd = f'rclone --config {conf_file} {cmd}'
    return envs, core_cmd

def run_(cmd, envs=None, **kargs):
    cmd_list = cmd.format_map({**globals(), **locals(), **kargs}).split()
    env = os.environ.copy()
    if envs:
        env.update(envs)
    process = subprocess.run(cmd_list, capture_output=True, text=True, env=env)
    return process.stderr, process.stdout


