import argparse
from datetime import datetime
import os

from launchpadlib.launchpad import Launchpad
import pytz

from . import conf
from . import constants

NAME = 'OpenStack Bugs'
LP_INSTANCE = 'production'
CACHE_DIR = os.path.expanduser('~/.launchpadlib/cache/')
LP_STATUS = (
    'New', 'Incomplete', 'Opinion', 'Invalid', 'Won\'t Fix', 'Confirmed',
    'Triaged', 'In Progress', 'Fix Committed', 'Fix Released'
)
DT_FORMAT = '%Y-%m-%d:%H:%M'


def valid_date(s):
    try:
        dt = datetime.strptime(s, DT_FORMAT)
        dt = dt.replace(tzinfo=pytz.utc)
        return dt
    except ValueError:
        msg = 'Not a valid date: %s' % s
        raise argparse.ArgumentTypeError(msg)


def main(config, project_names, start, end):
    lp = Launchpad.login_with(
        config.get('launchpad', 'account_name'),
        constants.LP_INSTANCE,
        config.get('launchpad', 'cache_dir')
    )

    for project_name in project_names:
        project = lp.projects[project_name]

        project_bugs = project.searchTasks(
            status=LP_STATUS, omit_duplicates=True, modified_since=start,
        )
        for bug in project_bugs:
            activities = bug.bug.activity
            for activity in activities:
                if activity.datechanged < end and activity.datechanged > start:
                    print bug.title
                    print bug.web_link
                    print activity.whatchanged
                    print activity.person.name
                    print '\n'


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file', default='~/.launchpadtk.conf')
    parser.add_argument('projects', nargs='+', help='Project(s) to report on')
    parser.add_argument(
        '-s', '--start', required=True, type=valid_date,
        help='Start of report in YYYY-MM-DD:HH:mm format'
    )
    parser.add_argument(
        '-e', '--end', type=valid_date,
        help='End of report in YYYY-MM-DD:HH:mm format'
    )

    args = parser.parse_args()
    config = conf.configure(os.path.expanduser(args.config_file))

    start = args.start
    if not args.end:
        end = datetime.now(tz=pytz.utc)
    else:
        end = args.end

    if start > end:
        msg = 'Start date can\'t be after the end date'
        raise argparse.ArgumentParser(msg)

    main(config, args.projects, start, end)
