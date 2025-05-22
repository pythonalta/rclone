# About

`rclone` is a simple Python wrapper for the core commands of the [rclone](https://rclone.org/) utility, focused in `S3` providers.

# Dependences

- [rclone](https://rclone.org/)

# Install

With `pip`: 
```
pip install git+https://github.com/pythonalta/rclone
```

With [py](https://github.com/ximenesyuri/py):
```
py install --from github pythonalta/rclone
```

# Usage

Create a `rclone.conf` file somewhere inside your project, defining its remote metadata, as follows:
```
[<your-remote-name>]
type = s3
provider = <YourS3Provider>
env_auth = false
access_key_id =
secret_access_key = 
endpoint = <your-provider-base-url>
region = <your-region>
location_constraint = <your-region>
```

Get your credentials and put them into your `.env` file:

```
...
MY_RCLONE_ACCESS_ID="<your-provider-access-id>"
MY_RCLONE_ACCESS_SECRET="<you-provider-access-secret>"
...
```

```python
from rclone import Rclone

# source the envs as you like, then initialize the class
rclone = Rclone(
    access_id=MY_RCLONE_ACCESS_ID,
    access_secret=MY_RCLONE_ACCESS_SECRET,
    remote="my_remote",
    conf_file="/path/to/rclone.conf".
)

# execute some command and collects the output
files = rclone.ls(
    path=f"{rclone.remote}:/path/to/somewhere"
)
...
```

# Commands

```
command      meaning
---------------------------------------------------
exists       check if given object exists
ls           list objects and return in json format
lsf          list files and return in json format
lsd          list dirs and return in json format
cp           copy files from source to target
mv           move everything from source to target
mvf          move files from sourcer to target
rm           remove an object
rmd          remove an object and empty directories
```

You can also execute any `rclone` command with:

```python
rclone.exec(command)
```
