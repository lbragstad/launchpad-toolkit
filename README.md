# launchpad-toolkit
A set of scripts to help with administrative tasks and management of projects
hosted on Launchpad.

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

## Building Bug Reports

This script will scrap Launchpad for bugs within a given time window and
attempt to build a report.

```
$ python bug_report.py -h
usage: bug_report.py [-h] [--launchpad-config-file LAUNCHPAD_CONFIG_FILE]
                     [--report-config-file REPORT_CONFIG_FILE]

Keystone bug reports.

optional arguments:
  -h, --help            show this help message and exit
  --launchpad-config-file LAUNCHPAD_CONFIG_FILE
  --report-config-file REPORT_CONFIG_FILE
```

Start by putting the report dates and projects in a configuration file:

```
$ cat << EOF > report.conf
> [report]
> projects = keystone keystoneauth keystonemiddleware python-keystoneclient
> start_date = 'April 13, 2018 12:00 AM CST'
> end_date = 'April 20, 2018 12:00 AM CST'
> EOF
```

Then run the script:

```
$ python bug_report.py
Bugs opened (5)
Bug #1763824 (keystone:Medium) opened by Morgan Fainberg https://bugs.launchpad.net/keystone/+bug/1763824
Bug #1765193 (keystone:Medium) opened by Lance Bragstad https://bugs.launchpad.net/keystone/+bug/1765193
Bug #1764272 (keystone:Undecided) opened by lucky https://bugs.launchpad.net/keystone/+bug/1764272
Bug #1764274 (keystone:Undecided) opened by lucky https://bugs.launchpad.net/keystone/+bug/1764274
Bug #1764282 (keystone:Undecided) opened by lucky https://bugs.launchpad.net/keystone/+bug/1764282

Bugs closed (0)

Bugs fixed (4)
Bug #1763824 (keystone:Medium) fixed by Morgan Fainberg https://bugs.launchpad.net/keystone/+bug/1763824
Bug #1754413 (keystone:Low) fixed by Russell Tweed https://bugs.launchpad.net/keystone/+bug/1754413
Bug #1754417 (keystone:Low) fixed by Russell Tweed https://bugs.launchpad.net/keystone/+bug/1754417
Bug #1755874 (keystone:Undecided) fixed by Morgan Fainberg https://bugs.launchpad.net/keystone/+bug/1755874
```

This script does use a ``.launchpadtk.conf`` file to pull information from
Launchpad using your account information. A sample one has been included in
this repository and by default ``bug_report.py`` will look for it in your home
directory.

## Recent Bugs

Note that most of this functionality has been superseded by ``bug_report.py``,
which is easier to use.

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

## Office Hours

Note that most of this functionality has been superseded by ``bug_report.py``,
which is easier to use.

Generate a report consisting of all bug activity for a project within a given
time period.

```
$ python -m tools.office_hours --help
usage: office_hours.py [-h] [--config-file CONFIG_FILE] -s START [-e END]
                       projects [projects ...]

positional arguments:
  projects              Project(s) to report on

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
  -s START, --start START
                        Start of report in YYYY-MM-DD:HH:mm format
  -e END, --end END     End of report in YYYY-MM-DD:HH:mm format
```

### Example Usage

Generate a report for keystone's office hours.

```
(.venv)$ python -m tools.office_hours -s 2017-08-01:19:00 -e 2017-08-01:22:00 keystone
```
