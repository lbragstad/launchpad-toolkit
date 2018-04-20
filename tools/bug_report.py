import argparse
import ConfigParser

import dateparser

import os

from launchpadlib import launchpad

LP_INSTANCE = 'production'
LP_STATUS = (
    'New', 'Incomplete', 'Opinion', 'Invalid', 'Won\'t Fix', 'Confirmed',
    'Triaged', 'In Progress', 'Fix Committed', 'Fix Released'
)
CLOSED_STATUS = (
    'Opinion', 'Invalid', 'Won\'t Fix',
)
FIXED_STATUS = (
    'Fix Committed', 'Fix Released'
)


def configure(config_file):
    config = ConfigParser.SafeConfigParser()
    config.read(config_file)
    return config


def main(launchpad_config, report_config):
    lp = launchpad.Launchpad.login_with(
        launchpad_config.get('launchpad', 'account_name'),
        LP_INSTANCE,
        launchpad_config.get('launchpad', 'cache_dir')
    )

    start_date = report_config.get('report', 'start_date')
    end_date = report_config.get('report', 'end_date')
    settings = {'TO_TIMEZONE': 'UTC'}
    start_datetime = dateparser.parse(start_date, settings=settings)
    end_datetime = dateparser.parse(end_date, settings=settings)

    created_bugs = []
    closed_bugs = []
    fixed_bugs = []
    for project in report_config.get('report', 'projects').split():
        bugs = lp.projects[project].searchTasks(
            status=LP_STATUS, modified_since=start_datetime
        )
        for bug in bugs:
            created_at = bug.date_created
            if created_at <= end_datetime and created_at >= start_datetime:
                created_bugs.append(bug)

            if bug.status in CLOSED_STATUS:
                closed_at = bug.date_closed
                if closed_at <= end_datetime and closed_at >= start_datetime:
                    closed_bugs.append(bug)

            if bug.status in FIXED_STATUS:
                closed_at = bug.date_closed
                if not closed_at:
                    closed_at = bug.date_fix_committed
                if closed_at <= end_datetime and closed_at >= start_datetime:
                    fixed_bugs.append(bug)

    print('Bugs opened (%d)' % len(created_bugs))
    for bug in created_bugs:
        s = 'Bug #%(number)s (%(target)s:%(sev)s) opened by %(owner)s %(link)s'
        s = s % {
            'number': bug.bug.id,
            'target': bug.bug_target_name,
            'sev': bug.importance,
            'owner': bug.owner.display_name,
            'link': bug.web_link
        }
        print(s)

    print('\nBugs closed (%d)' % len(closed_bugs))
    for bug in closed_bugs:
        s = 'Bug #%(number)s (%(target)s:%(sev)s) %(link)s'
        s = s % {
            'number': bug.bug.id,
            'target': bug.bug_target_name,
            'sev': bug.importance,
            'link': bug.web_link
        }
        print(s)

    print('\nBugs fixed (%d)' % len(fixed_bugs))
    for bug in fixed_bugs:
        assignee = bug.assignee.display_name
        s = ('Bug #%(number)s (%(target)s:%(sev)s) fixed by '
             '%(assignee)s %(link)s')
        s = s % {
            'number': bug.bug.id,
            'target': bug.bug_target_name,
            'sev': bug.importance,
            'assignee': assignee if assignee else 'no one',
            'link': bug.web_link
        }
        print(s)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Automated bug reports.')
    parser.add_argument(
        '--launchpad-config-file', default='~/.launchpadtk.conf'
    )
    parser.add_argument('--report-config-file', default='sample.conf')
    args = parser.parse_args()

    launchpad_config = configure(
        os.path.expanduser(args.launchpad_config_file)
    )
    report_config = configure(args.report_config_file)
    main(launchpad_config, report_config)
