import json

from .helpers import to_unix_time


class Alert(object):
    """An alert within the Freedom Robotics API. Not intended to be manually instantiated by the user of the API.

    Args:
        _id (str): Alert ID.
        _data (`dict`): Alert data.
        **kwargs: Extra arguments that could be used for set extra attributes
                  that are not part of the alert such as account and device names.
    """

    def __init__(self, _id, _data, **kwargs):
        self._id = _id
        self._data = _data
        self._account_name = kwargs.get('account_name')
        self._device_name = kwargs.get('device_name')

    def __repr__(self):
        return "<Alert: {} {} {}>".format(self._id, self._data.get("name", ""), self.level)

    def __eq__(self, obj):
        return isinstance(obj, Alert) and obj._id == self._id and obj.level == self.level

    @property
    def attributes(self):
        return self._data.get("attributes")

    @property
    def action(self):
        return self._data.get('action')

    @property
    def account_name(self):
        if self._account_name is not None:
            account_name = self._account_name
        else:
            account_name = self._data.get("account_name")
        return account_name

    @property
    def description(self):
        return self._data.get("description")

    @property
    def device_name(self):
        if self._device_name is not None:
            device_name = self._device_name
        else:
            device_name = self._data.get('device_name')
        return device_name

    @property
    def device_id(self):
        return self._data.get("device_id")

    @property
    def topics_snapshot(self):
        return self._data.get("topics_snapshot")

    @property
    def level(self):
        return self._data.get("level")

    @property
    def name(self):
        return self._data.get("name")

    @property
    def replay_url(self):
        return self._data.get("replay_url")

    @property
    def type(self):
        return self._data.get("type")

    @property
    def utc_time(self):
        if 'creation_timestamp' in self._data:
            utc_time = self._data['creation_timestamp']
        else:
            utc_time = self._data.get('utc_time')
        return to_unix_time(utc_time)


def get_alert(api, account_id, alert_id, attributes=None, params=None, **kwargs):
    """:obj:`Alert` : Fetch an Alert by its ID (ALTXXXXXXXXXXXX).

    Args:
        api (ApiHandler): Api handler object.
        account_id (str): Account ID.
        alert_id (str): Alert ID.
        attributes (list): Optional list of alert attributes to return.
        params (dict): Optional query parameters.
        **kwargs: Extra keyword arguments passed to Alert object.
    """
    if params is None:
        params = {}
    if attributes is not None:
        params["attributes"] = json.dumps(attributes)

    path = '/accounts/{}/alerts/{}'.format(account_id, alert_id)

    alert_data = api.call("GET", path, params=params)
    if not alert_data:
        return None
    alert = Alert(alert_data["id"], alert_data, **kwargs)
    return alert


def get_alerts(api, account_id, device_id=None, zone_id=None, attributes=None, params=None, **kwargs):
    """:obj:`list` : Fetch a list of alerts for an account, device or zone.

    Args:
        api (ApiHandler): Api handler object.
        account_id (str): Account ID.
        device_id (str): Optional device ID.
        zone_id (str): Optional zone ID.
        attributes (list): Optional list of alert attributes to return.
        params (dict): Optional query parameters.
        **kwargs: Extra keyword arguments passed to Alert object.
    """
    if params is None:
        params = {}
    if attributes is not None:
        params["attributes"] = json.dumps(attributes)

    path = '/accounts/{}'.format(account_id)
    if device_id is not None:
        path = '{}/devices/{}/alerts'.format(path, device_id)
    elif zone_id is not None:
        path = '{}/zones/{}/alerts'.format(path, zone_id)
    else:
        path = '{}/alerts'.format(path)

    alerts_data = api.call("GET", path, params=params)
    if not alerts_data:
        return []
    alerts = [Alert(alert_data["id"], alert_data, **kwargs) for alert_data in alerts_data]
    return alerts
