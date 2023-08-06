from .entity import Entity
from .alert import get_alerts


class Zone(Entity):

    def _make_url(self):
        return "/accounts/{}/zones/{}".format(self._data.get('account_id'), self._id)

    @property
    def account_id(self):
        """str: Account id.
        """
        return self._data.get("account_id")

    @property
    def name(self):
        """str: Zone name.
        """
        return self._data.get("name")

    @property
    def sub_zones(self):
        """:obj:`list` of :obj:`Zone`: Fetch a list of all zones in the account.
        """
        if not self._data.get("has_subzones"):
            return []
        return [Zone(data['id'], data, api=self.api) for data in self._data.get("sub_zones", [])]

    def get_alerts(self, attributes=None, params=None):
        """:obj:`list` of :obj:`Alert`: Fetch a list of alerts for the zone, according to the used params

        Args:
            attributes (list): Optional list of attributes to request.
            params (dict): Optional query parameters.
        """
        alerts = get_alerts(
            self.api,
            self.account_id,
            zone_id=self._id,
            attributes=attributes,
            params=params,
        )
        return alerts
