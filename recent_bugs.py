#! /usr/bin/env python
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import argparse
import datetime
import os

from launchpadlib.launchpad import Launchpad
from lxml import html
from lxml.html import builder as E

NAME = 'Recent OpenStack Bugs'
LP_INSTANCE = 'production'
LPCACHEDIR = os.path.expanduser(os.environ.get('LPCACHEDIR',
                                               '~/.launchpadlib/cache'))

LPSTATUS = ('New', 'Confirmed', 'Triaged', 'In Progress')


class DataFormatter(object):

    def __init__(self, reports, days, format_as_html):
        self.days = days
        self.format = (
            self._render_to_html if format_as_html else self._render_to_sdout
        )
        self.reports = reports

    def _generate_project_report_in_html(self, project_name, project_bugs):
        report = E.BODY(E.H2(E.CLASS("heading"), "%s (%d)" % (
            project_name, len(project_bugs))))
        for bug in project_bugs:
            bug_link = E.A(bug.title, href=bug.web_link, target='_blank')
            report.append(
                E.P("[%s:%s] " % (bug.importance, bug.status), bug_link)
            )
            if bug.assignee:
                report.append(
                    E.P("Assigned to: %s" % (bug.assignee.display_name))
                )
        return report

    def _render_to_html(self):
        entire_bug_report = E.HTML()
        for k, v in self.reports.iteritems():
            entire_bug_report.append(
                self._generate_project_report_in_html(k, v)
            )
        print html.tostring(entire_bug_report)

    def _render_to_sdout(self):
        for k, v in self.reports.iteritems():
            print "%s bugs opened in the last %d days" % (k, self.days)
            for bug in v:
                print bug.title
                print bug.status + ':' + bug.importance
                print bug.web_link + '\n'


def is_bug_recent(bug, num_of_days):
    """Determine if a bug was created in the last X days."""
    invalid_states = ["Incomplete", "Opinion", "Won't Fix", "Expired",
                      "Fix Released", "Fix Committed"]
    if bug.status not in invalid_states:
        # Create timedelta object to compare bug creation times against.
        delta = datetime.timedelta(days=num_of_days)
        today = datetime.datetime.today()
        # Replace tzinfo so that it doesn't mess with comparisons.
        bug_created_time = bug.date_created.replace(tzinfo=None)
        if bug_created_time >= today - delta:
            return True
        return False
    return False


def get_project(project_name):
    """Return a launchpad project object given a project name."""
    lp = Launchpad.login_anonymously(NAME, LP_INSTANCE, LPCACHEDIR)
    return lp.projects[project_name]


def get_open_project_bugs(project):
    """Given a launchpad project object, grab all bugs."""
    project_bugs = project.searchTasks(status=LPSTATUS,
                                       omit_duplicates=True,
                                       order_by='-importance')
    return project_bugs


def main(days, project_names, format_as_html):
    reports = {}
    for project_name in project_names:
        try:
            project = get_project(project_name)
        except KeyError:
            raise Exception('%s does not exist in Launchpad' % project_name)

        open_project_bugs = get_open_project_bugs(project)
        recent_project_bugs = []
        for bug in open_project_bugs:
            if is_bug_recent(bug, days):
                recent_project_bugs.append(bug)

        reports[project_name] = recent_project_bugs

    formatter = DataFormatter(reports, days, format_as_html)
    formatter.format()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='summarize bugs from a '
                                     'launchpad project')
    parser.add_argument(
        '-d', '--days', default='2', type=int, help='history in number of days'
    )
    parser.add_argument(
        '-p', '--project', nargs='+', required=True,
        help='launchpad project(s) to pull bugs from'
    )
    parser.add_argument(
        '-H', '--html', action='store_true', help='Format the reports as HTML'
    )
    args = parser.parse_args()

    main(args.days, args.project, args.html)
