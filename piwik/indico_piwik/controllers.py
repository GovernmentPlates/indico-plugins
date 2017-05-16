# This file is part of Indico.
# Copyright (C) 2002 - 2017 European Organization for Nuclear Research (CERN).
#
# Indico is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License as
# published by the Free Software Foundation; either version 3 of the
# License, or (at your option) any later version.
#
# Indico is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Indico; if not, see <http://www.gnu.org/licenses/>.

from flask import jsonify

from indico.core.config import Config
from indico.legacy.webinterface.rh.conferenceModif import RHConferenceModifBase

from indico_piwik.views import WPStatistics
from indico_piwik.reports import (ReportCountries, ReportDevices, ReportDownloads, ReportGeneral, ReportMaterial,
                                  ReportVisitsPerDay)


class RHStatistics(RHConferenceModifBase):
    def _checkParams(self, params):
        RHConferenceModifBase._checkParams(self, params)
        self._params = params
        self._params['loading_gif'] = '{}/images/loading.gif'.format(Config.getInstance().getBaseURL())
        self._params['report'] = ReportGeneral.get(event_id=params.get('confId'), contrib_id=params.get('contrib_id'),
                                                   start_date=params.get('start_date'), end_date=params.get('end_date'))

    def _process(self):
        return WPStatistics.render_template('statistics.html', self._conf, **self._params)


class RHApiBase(RHConferenceModifBase):
    ALLOW_LOCKED = True

    def _checkParams(self, params):
        RHConferenceModifBase._checkParams(self, params)
        self._report_params = {'start_date': params.get('start_date'),
                               'end_date': params.get('end_date')}


class RHApiEventBase(RHApiBase):
    def _checkParams(self, params):
        RHApiBase._checkParams(self, params)
        self._report_params['event_id'] = params['confId']
        self._report_params['contrib_id'] = params.get('contrib_id')


class RHApiDownloads(RHApiEventBase):
    def _checkParams(self, params):
        RHApiEventBase._checkParams(self, params)
        self._report_params['download_url'] = params['download_url']

    def _process(self):
        return jsonify(ReportDownloads.get(**self._report_params))


class RHApiEventVisitsPerDay(RHApiEventBase):
    def _process(self):
        return jsonify(ReportVisitsPerDay.get(**self._report_params))


class RHApiEventGraphCountries(RHApiEventBase):
    def _process(self):
        return jsonify(ReportCountries.get(**self._report_params))


class RHApiEventGraphDevices(RHApiEventBase):
    def _process(self):
        return jsonify(ReportDevices.get(**self._report_params))


class RHApiMaterial(RHApiEventBase):
    def _process(self):
        return jsonify(ReportMaterial.get(**self._report_params))
