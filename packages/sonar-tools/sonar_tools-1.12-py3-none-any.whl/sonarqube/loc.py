#!/usr/local/bin/python3
#
# sonar-tools
# Copyright (C) 2022 Olivier Korach
# mailto:olivier.korach AT gmail DOT com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 3 of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program; if not, write to the Free Software Foundation,
# Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
'''
    Exports LoC per projects
'''
import sys
from sonarqube import projects, env, version
import sonarqube.utilities as util


def __deduct_format(fmt, file):
    if fmt is not None:
        return fmt
    if file is not None:
        ext = file.split('.').pop(-1).lower()
        util.logger.debug("File extension = %s", ext)
        if ext == 'json':
            return ext
    return 'csv'


def __csv_header_line(**kwargs):
    line = "# Project Key"
    if kwargs['projectName']:
        line += f"{kwargs['csvSeparator']}Project Name"
    line += f"{kwargs['csvSeparator']}LoC"
    if kwargs['lastAnalysis']:
        line += f"{kwargs['csvSeparator']}Last Analysis"
    return line


def __csv_line(project, **kwargs):
    line = project.key
    if kwargs['projectName']:
        line += f"{kwargs['csvSeparator']}{project.name}"
    line += f"{kwargs['csvSeparator']}{project.ncloc_with_branches()}"
    if kwargs['lastAnalysis']:
        last = project.last_analysis_date(include_branches=True)
        if last is None:
            last = ''
        line += f"{kwargs['csvSeparator']}{last}"
    return line


def __json_data(project, **kwargs):
    data = {'projectKey': project.key, 'ncloc': project.ncloc_with_branches()}
    if kwargs['projectName']:
        data['projectName'] = project.name
    if kwargs['lastAnalysis']:
        data['lastAnalysis'] = util.date_to_string(project.last_analysis_date(include_branches=True))
    return data


def __dump_loc(project_list, file, **kwargs):
    if file is None:
        fd = sys.stdout
        util.logger.info("Dumping LoC report to stdout")
    else:
        fd = open(file, "w", encoding='utf-8')
        util.logger.info("Dumping LoC report to file '%s'", file)

    if kwargs['format'] != 'json':
        print(__csv_header_line(**kwargs), file=fd)
    nb_loc = 0
    nb_projects = 0
    loc_list = []
    for p in project_list.values():
        if kwargs['format'] == 'json':
            loc_list.append(__json_data(p, **kwargs))
        else:
            print(__csv_line(p, **kwargs), file=fd)
        nb_loc += p.ncloc_with_branches()
        nb_projects += 1
        if nb_projects % 50 == 0:
            util.logger.info("%d PROJECTS and %d LoCs, still counting...", nb_projects, nb_loc)
    if kwargs['format'] == 'json':
        print(util.json_dump(loc_list), file=fd)
    if file is not None:
        fd.close()
    util.logger.info("%d PROJECTS and %d LoCs in total", len(project_list), nb_loc)


def main():
    parser = util.set_common_args('Extract projects lines of code, as computed for the licence')
    parser = util.set_component_args(parser)
    parser.add_argument('-n', '--projectName', required=False, default=False, action='store_true',
                        help='Also list the project name on top of the project key')
    parser.add_argument('-a', '--lastAnalysis', required=False, default=False, action='store_true',
                        help='Also list the last analysis date on top of nbr of LoC')
    parser.add_argument('-o', '--outputFile', required=False, help='File to generate the report, default is stdout'
                        'Format is automatically deducted from file extension, if extension given')
    parser.add_argument('-f', '--format', required=False,
                        help='Format of output (json, csv), default is csv')
    parser.add_argument('--csvSeparator', required=False, default=util.CSV_SEPARATOR,
                        help=f'CSV separator (for CSV output), default {util.CSV_SEPARATOR}')
    args = util.parse_and_check_token(parser)
    endpoint = env.Environment(some_url=args.url, some_token=args.token)
    util.check_environment(vars(args))
    util.logger.info('sonar-tools version %s', version.PACKAGE_VERSION)
    args.format = __deduct_format(args.format, args.outputFile)
    project_list = projects.search(endpoint=endpoint)
    __dump_loc(project_list, args.outputFile, **vars(args))
    sys.exit(0)


if __name__ == '__main__':
    main()
