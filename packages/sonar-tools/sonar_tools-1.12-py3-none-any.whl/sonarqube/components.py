#
# sonar-tools
# Copyright (C) 2019-2022 Olivier Korach
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

    Abstraction of the SonarQube "component" concept

'''

import json
import sonarqube.sqobject as sq
import sonarqube.utilities as util
from sonarqube import env


class Component(sq.SqObject):

    def __init__(self, key, endpoint=None, data=None):
        super().__init__(key, endpoint)
        self._name = None
        self.qualifier = None
        self.path = None
        self.language = None
        self.nbr_issues = None
        self._ncloc = None
        if data is not None:
            self.__load__(data)

    def __load__(self, data):
        self._name = data.get('name', None)
        self.qualifier = data.get('qualifier', None)
        self.path = data.get('path', None)
        self.language = data.get('language', None)

    def __str__(self):
        return self.key

    def get_subcomponents(self, strategy='children', with_issues=False):
        parms = {'component': self.key, 'strategy': strategy, 'ps': 1,
                 'metricKeys': 'bugs,vulnerabilities,code_smells,security_hotspots'}
        resp = env.get('measures/component_tree', params=parms, ctxt=self.endpoint)
        data = json.loads(resp.text)
        nb_comp = data['paging']['total']
        util.logger.debug("Found %d subcomponents to %s", nb_comp, str(self))
        nb_pages = (nb_comp + 500 - 1)//500
        comp_list = {}
        parms['ps'] = 500
        for page in range(nb_pages):
            parms['p'] = page + 1
            resp = env.get('measures/component_tree', params=parms, ctxt=self.endpoint)
            data = json.loads(resp.text)
            for d in data['components']:
                nbr_issues = 0
                for m in d['measures']:
                    nbr_issues += int(m['value'])
                if with_issues and nbr_issues == 0:
                    util.logger.debug("Subcomponent %s has 0 issues, skipping", d['key'])
                    continue
                comp_list[d['key']] = Component(d['key'], self.endpoint, data=d)
                comp_list[d['key']].nbr_issues = nbr_issues
                util.logger.debug("Component %s has %d issues", d['key'], nbr_issues)
        return comp_list

    def get_number_of_filtered_issues(self, params):
        from sonarqube import issues
        params['componentKey'] = self.key
        params['ps'] = 1
        returned_data = issues.search(endpoint=self.endpoint, params=params)
        return returned_data['total']

    def get_number_of_issues(self):
        ''' Returns number of issues of a component '''
        if self.nbr_issues is None:
            self.nbr_issues = self.get_number_of_filtered_issues({'componentKey': self.key})
        return self.nbr_issues

    def get_oldest_issue_date(self):
        ''' Returns the oldest date of all issues found '''
        from sonarqube import issues
        return issues.get_oldest_issue(endpoint=self.endpoint, params={'componentKeys': self.key})

    def get_newest_issue_date(self):
        ''' Returns the newest date of all issues found '''
        from sonarqube import issues
        return issues.get_newest_issue(endpoint=self.endpoint, params={'componentKeys': self.key})

    def get_issues(self):
        from sonarqube import issues
        issue_list = issues.search(endpoint=self.endpoint, params={'componentKeys': self.key})
        self.nbr_issues = len(issue_list)
        return issue_list

    def get_measures(self, metrics_list):
        # Must be implemented in sub classes
        return {}

    def get_measure(self, metric, fallback=None):
        meas = self.get_measures(metric)
        if metric in meas and meas[metric] is not None:
            return meas[metric]
        else:
            return fallback

    def ncloc(self):
        if self._ncloc is None:
            self._ncloc = int(self.get_measure('ncloc', fallback=0))
        return self._ncloc

def get_components(component_types, endpoint=None):
    resp = env.get('projects/search', params={'ps': 500, 'qualifiers': component_types}, ctxt=endpoint)
    data = json.loads(resp.text)
    return data['components']


def get_subcomponents(component_key, strategy='children', with_issues=False, endpoint=None):
    return Component(component_key, endpoint).get_subcomponents(strategy=strategy, with_issues=with_issues)
