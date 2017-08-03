# launchpad-toolkit
A set of scripts to help with administrative tasks and management of projects hosted on Launchpad.

## Installing Dependencies

All dependencies except `dbus-python` are included in `requirements.txt`. The
`dbus-python` package can be installed via packages but it needs to be included
in the virtualenv if one is being used:

```
$ sudo dnf install dbus-python
$ virtualenv --system-site-packages .venv
$ source .venv/bin/activate
(.venv)$ pip install -r requirements.txt
```

## Recent Bugs

A basic script that reports all new bug activity within a given time period.

```
$ python -m tools.recent_bugs --help
usage: recent_bugs.py [-h] [--config-file CONFIG_FILE] [-d DAYS] [-H]
                      projects [projects ...]

summarize bugs from a launchpad project

positional arguments:
  projects

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
  -d DAYS, --days DAYS  history in number of days
  -H, --html            Format the reports as HTML
```

### Example Usage

Generate a weekly report for all bugs recently opened in OpenStack Identity
project.

```
(.venv)$ python -m tools.recent_bugs -d 7 -p keystone
```

Generate a monthly report for all bugs opened against all OpenStack Identity
projects.

```
(.venv)$ python -m tools.recent_bugs -d 30 -p keystone keystoneauth keystonemiddleware python-keystoneclient
```
