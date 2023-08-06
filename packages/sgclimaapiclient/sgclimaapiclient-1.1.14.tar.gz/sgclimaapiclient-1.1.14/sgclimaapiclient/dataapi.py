from typing import List, Union

import pandas as pd
from datetime import datetime, date, timedelta

from sgclimaapiclient.baseapi import BaseAPI


class SGClimaDataAPI(BaseAPI):
    """
    A Python client to seamlessly use the SGClima Data API
    """

    def __init__(self, token: str, endpoint: str = 'https://data-api.dc.indoorclima.com', verify: bool = True):
        """
        SGClimaDataAPI contructor
        :param token: API Key for authentication
        :param endpoint: API endpoint.
        :param verify: Whether to verify the requests
        """
        super().__init__(token, endpoint, verify)

    def list_organizations(self, name: str = None, sector: str = None) -> dict:
        """
        List all the organizations.
        \f
        :param name: Filter by name of the organization
        :param sector: Filter by sector of the organization
        """
        params = self._build_params(name=name, sector=sector)
        return self._call_json("/organizations/", params=params)

    def get_organization(self, organization_id: int) -> dict:
        """
        Get a single organization based on its identifier.
        \f
        :param organization_id: Organization id
        """
        return self._call_json("/organizations/{id}".format(id=organization_id))

    def get_organization_sites(self, organization_id: int) -> dict:
        """
        Get all sites of a given organization.
        \f
        :param organization_id: Organization id
        """
        return self._call_json("/organizations/{id}".format(id=organization_id))

    def list_sites(self, name: str = None, sector: str = None) -> dict:
        """
        List all the sites.
        \f
        :param name: Filter by name of the site
        :param sector: Filter by sector of the site
        """
        params = self._build_params(name=name, sector=sector)
        return self._call_json("/sites/", params=params)

    def get_site(self, site_id: int) -> dict:
        """
        Get a single site based on its identifier.
        \f
        :param site_id: Site id
        """

        return self._call_json("/sites/{id}".format(id=site_id))

    def get_site_zones(self, site_id: int) -> dict:
        """
        Get all zones of a given site.
        \f
        :param site_id: Site id
        """
        return self._call_json("/sites/{id}/zones".format(id=site_id))

    def get_site_equipments(self, site_id: int, equipment_type: str = None) -> dict:
        """
        Get all equipments of a given site.
        \f
        :param site_id: Site id
        """
        params = self._build_params(equipment_type=equipment_type)
        return self._call_json("/sites/{id}/equipments".format(id=site_id), params=params)

    def download_site_data(
            self,
            site_id: int,
            start: Union[datetime, date, str],
            end: Union[datetime, date, str],
            filter_by_pid: List[int] = None,
            filter_by_named_pid: List[str] = None
    ) -> pd.DataFrame:
        """
        Get the Site data for each Parameter given a date/timestamp range.
        Things to consider about the data:

        * Each column represents a Parameter identified by 'NAMED_PARAMETER:PARAMETER_ID'.
        * Each row has a timestamp multiple of 5 meaning that for each day there are 288 rows from 00:00 to 23:55. Even
        if there is no data available for a timestamp the row is returned.
        \f
        :param site_id: Site id
        :param start: The from to be requested. Either a date (yyyy-mm-dd) or a timestamp (yyyy-mm-ddTHH:MM:SS).
        :param end: The to day to be requested. Either a date (yyyy-mm-dd) or a timestamp (yyyy-mm-ddTHH:MM:SS).
        Example: 2021-01-01 will return data up to 2020-12-31"
        :param filter_by_pid: Filter the data to only have the pids specified in the query. It is expected a list
        of pids. Example: [12345,12346,12347].
        :param filter_by_named_pid: Filter the data to only have the named PIDs specified in the query. It is expected
        a list of pids names. Example: ["outside_hum_pid","pot_clim_gen_pid","set_point_zone_pid"]
        """
        if filter_by_pid is not None:
            filter_by_pid = ",".join(str(pid) for pid in filter_by_pid)
        if filter_by_named_pid is not None:
            filter_by_named_pid = ",".join(filter_by_named_pid)

        params = self._build_params(start=start, end=end, filter_by_pid=filter_by_pid,
                                    filter_by_named_pid=filter_by_named_pid)
        return self._call_df("/sites/{id}/data/download".format(id=site_id), params=params)

    def download_site_last_values(
            self,
            site_id: int,
            filter_by_pid: List[int] = None,
            filter_by_named_pid: List[str] = None
    ) -> pd.DataFrame:
        """
        TODO: This endpoint will be changed
        \f
        :param site_id: Site identifier
        :param filter_by_pid: Filter the data to only have the pids specified in the query. It is expected a list
        of pids. Example: [12345,12346,12347].
        :param filter_by_named_pid: Filter the data to only have the named PIDs specified in the query. It is expected
        a list of pids names. Example: ["outside_hum_pid","pot_clim_gen_pid","set_point_zone_pid"]
        """
        if filter_by_pid is not None:
            filter_by_pid = ",".join(str(pid) for pid in filter_by_pid)
        if filter_by_named_pid is not None:
            filter_by_named_pid = ",".join(filter_by_named_pid)

        params = self._build_params(filter_by_pid=filter_by_pid, filter_by_named_pid=filter_by_named_pid)
        return self._call_df("/sites/{id}/last_values/download".format(id=site_id), params=params)

    def get_site_health_history(
            self,
            site_id: int,
            start: Union[datetime, date, str],
            end: Union[datetime, date, str],
            threshold: int = 70,
            max_consecutive_days_below: int = 1
    ) -> pd.DataFrame:
        """
        NOTE: Before using this endpoint please take a look at the concept [PIDs Health](/sgclima/health/index.html).

        Download the site health history and get the PIDs that match the desired threshold given a timeframe.
        Things to consider about the data:

        * The columns matches the specified date range.
        * The rows matches the found PIDs.

        It is possible the endpoint returns the error "Missing health dates.". This means that the PIDs health is not
        calculated and thus is not yet available. To fix this it is necessary to call the endpoint
        `/{site_id}/health/calculate` for the missing dates.

        \f
        :param site_id: Site identifier
        :param start: The from day to be requested as a date (yyyy-mm-dd).
        :param end: The to day to be requested as a date (yyyy-mm-dd).
        :param threshold: The minimum health allowed for a PID. Example: The value 70 will return the PIDs that have an
        average health greater or equal than 70.
        :param max_consecutive_days_below: The maximum number of consecutive days a PID can stay below the threshold.
        Example: If a PID falls lower than the specified `threshold` during less or equal to `max_consecutive_days_below`
        the PID will still be valid and returned. This allows for a sensor to fall for a given period of time without
        ignoring it.
        """
        params = self._build_params(start=start, end=end, threshold=threshold,
                                    max_consecutive_days_below=max_consecutive_days_below
                                    )
        return self._call_df("/sites/{id}/health/history".format(id=site_id), params=params)

    def calculate_site_health(self, site_id: int, date: Union[date, str]):
        """
        NOTE: Before using this endpoint please take a look at the concept [PIDs Health](/sgclima/health/index.html).

        Calculate the site health on a given date.

        \f
        :param site_id: Site identifier
        :param date: Desired date
        """
        params = self._build_params(date=date)
        return self._call("/sites/{id}/health/calculate".format(id=site_id), params=params)

    def list_zones(self) -> dict:
        """
        List all the zones.
        \f
        """
        return self._call_json("/zones/")

    def get_zone(self, zone_id: str) -> dict:
        """
        Get a single zone based on its identifier.
        \f
        :param zone_id: Zone id
        """

        return self._call_json("/zones/{id}".format(id=zone_id))

    def get_zone_equipments(self, zone_id: str, equipment_type: str = None) -> dict:
        """
        Get all equipments of a given zone.
        \f
        :param zone_id: Zone id
        """
        params = self._build_params(equipment_type=equipment_type)
        return self._call_json("/zones/{id}/equipments".format(id=zone_id), params=params)
    
    def download_equipment_efficiency(
            self,
            equipment_id: str,
            start: Union[datetime, date, str],
            end: Union[datetime, date, str]
    ) -> pd.DataFrame:
        """
        Get the Zone data for each Parameter given a date/timestamp range.
        Things to consider about the data:

        * Each column represents a Parameter identified by 'NAMED_PARAMETER:PARAMETER_ID'.
        * Each row has a timestamp multiple of 5 meaning that for each day there are 288 rows from 00:00 to 23:55. Even
        if there is no data available for a timestamp the row is returned.
        \f
        :param zone_id: Zone id
        :param start: The from to be requested. Either a date (yyyy-mm-dd) or a timestamp (yyyy-mm-ddTHH:MM:SS).
        :param end: The to day to be requested. Either a date (yyyy-mm-dd) or a timestamp (yyyy-mm-ddTHH:MM:SS).
        Example: 2021-01-01 will return data up to 2020-12-31"
        :param filter_by_pid: Filter the data to only have the pids specified in the query. It is expected a list
        of pids. Example: [12345,12346,12347].
        :param filter_by_named_pid: Filter the data to only have the named PIDs specified in the query. It is expected
        a list of pids names. Example: ["outside_hum_pid","pot_clim_gen_pid","set_point_zone_pid"]
        """
        params = self._build_params(start=start, end=end)
        return self._call_df("/equipments/{id}/efficiency".format(id=equipment_id), params=params)


    def download_zone_data(
            self,
            zone_id: str,
            start: Union[datetime, date, str],
            end: Union[datetime, date, str],
            filter_by_pid: List[int] = None,
            filter_by_named_pid: List[str] = None,
            partition: bool = False
    ) -> pd.DataFrame:
        """
        Get the Zone data for each Parameter given a date/timestamp range.
        Things to consider about the data:

        * Each column represents a Parameter identified by 'NAMED_PARAMETER:PARAMETER_ID'.
        * Each row has a timestamp multiple of 5 meaning that for each day there are 288 rows from 00:00 to 23:55. Even
        if there is no data available for a timestamp the row is returned.
        \f
        :param zone_id: Zone id
        :param start: The from to be requested. Either a date (yyyy-mm-dd) or a timestamp (yyyy-mm-ddTHH:MM:SS).
        :param end: The to day to be requested. Either a date (yyyy-mm-dd) or a timestamp (yyyy-mm-ddTHH:MM:SS).
        Example: 2021-01-01 will return data up to 2020-12-31"
        :param filter_by_pid: Filter the data to only have the pids specified in the query. It is expected a list
        of pids. Example: [12345,12346,12347].
        :param filter_by_named_pid: Filter the data to only have the named PIDs specified in the query. It is expected
        a list of pids names. Example: ["outside_hum_pid","pot_clim_gen_pid","set_point_zone_pid"]
        """
        if filter_by_pid is not None:
            filter_by_pid = ",".join(str(pid) for pid in filter_by_pid)
        if filter_by_named_pid is not None:
            filter_by_named_pid = ",".join(filter_by_named_pid)
        if partition:
            if isinstance(start, str):
                try:
                    start = datetime.strptime(start, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    c = datetime.strptime(start, "%Y-%m-%d")
            if isinstance(end, str):
                try:
                    end = datetime.strptime(end, "%Y-%m-%dT%H:%M:%S")
                except ValueError:
                    end = datetime.strptime(end, "%Y-%m-%d")

            dfs = []
            found = False
            c_start = c
            while not found:

                c_end = c_start + timedelta(days=30)
                if c_end > end:
                    c_end = end
                    found = True
                params = self._build_params(start=c_start.strftime("%Y-%m-%dT%H:%M:%S"), end=c_end.strftime("%Y-%m-%dT%H:%M:%S"), filter_by_pid=filter_by_pid, filter_by_named_pid=filter_by_named_pid)
                dfs.append(self._call_df("/zones/{id}/data/download".format(id=zone_id), params=params))
                c_start = c_end
            return pd.concat(dfs)
        else:
            params = self._build_params(start=start, end=end, filter_by_pid=filter_by_pid,
                                        filter_by_named_pid=filter_by_named_pid)
            return self._call_df("/zones/{id}/data/download".format(id=zone_id), params=params)

    def download_zone_last_values(
            self,
            zone_id: str,
            filter_by_pid: List[int] = None,
            filter_by_named_pid: List[str] = None
    ) -> pd.DataFrame:
        """
        TODO: This endpoint will be changed
        \f
        :param zone_id: Zone identifier
        :param filter_by_pid: Filter the data to only have the pids specified in the query. It is expected a list
        of pids. Example: [12345,12346,12347].
        :param filter_by_named_pid: Filter the data to only have the named PIDs specified in the query. It is expected
        a list of pids names. Example: ["outside_hum_pid","pot_clim_gen_pid","set_point_zone_pid"]
        """
        if filter_by_pid is not None:
            filter_by_pid = ",".join(str(pid) for pid in filter_by_pid)
        if filter_by_named_pid is not None:
            filter_by_named_pid = ",".join(filter_by_named_pid)

        params = self._build_params(filter_by_pid=filter_by_pid, filter_by_named_pid=filter_by_named_pid)
        return self._call_df("/zones/{id}/last_values/download".format(id=zone_id), params=params)

    def list_equipments(self, equipment_type: str = None) -> dict:
        """
        List all the equipments.
        \f
        :param equipment_type: Type of equipment
        """
        params = self._build_params(equipment_type=equipment_type)
        return self._call_json("/equipments/", params=params)

    def get_equipment(self, equipment_id: str) -> dict:
        """
        Get a single equipment based on its identifier.
        \f
        :param equipment_id: Equipment id
        """

        return self._call_json("/equipments/{id}".format(id=equipment_id))

    def list_gateways(self) -> dict:
        """
        List all the gateways.
        \f
        """
        return self._call_json("/gateways/")

    def get_gateway(self, gateway_id: int) -> dict:
        """
        Get a single gateway based on its identifier.
        \f
        :param gateway_id: Gateway id
        """

        return self._call_json("/gateways/{id}".format(id=gateway_id))

    def get_gateway_parameters(self, gateway_id: int) -> dict:
        """
        Get all parameters of a given gateway.
        \f
        :param gateway_id: Gateway id
        """
        return self._call_json("/gateways/{id}/parameters".format(id=gateway_id))

    def list_parameters(self, site_id: int = None, gateway_id: int = None) -> dict:
        """
        List all the parameters.
        \f
        :param site_id: Filter by site based on its identifier
        :param gateway_id: Filter by gateway based on its identifier
        """
        params = self._build_params(site_id=site_id, gateway_id=gateway_id)
        return self._call_json("/parameters/", params=params)

    def get_parameter(self, parameter_id: int) -> dict:
        """
        Get a single parameter based on its identifier.
        \f
        :param parameter_id: Parameter id
        """

        return self._call_json("/parameters/{id}".format(id=parameter_id))

    # this method extracts pids from layout
    def extract_pids(self, x) -> List[str]:
        pids = []
        if type(x) == dict:
            for k, v in x.items():
                if k.endswith('_pid'):
                    try:
                        pids.append({k: int(v)})
                    except TypeError:
                        # print(k, '=>', v, 'is not ok')
                        pids.append({k: None})
                        pass
                    except ValueError:
                        pids.append({k: None})
                else:
                    pids.extend(self.extract_pids(v))
        elif type(x) == list:
            for v in x:
                pids.extend(self.extract_pids(v))
        return pids

    def extract_filtered_pids(self, x: Union[dict, List[dict]], tags: List[str] = [], with_tags: bool = False) -> List[str]:
        """
        Method that given a set of SGClima entities (Site, Zone) it returns its PIDs in the format of
        <pid>.
        :param: x: SGClima entity
        :param: tags: List of pids to filter. Returned named pid will match with the ones in the list.
        """
        pids = []

        for k, v in self._extract(x, tags):
            try:
                if k in tags:
                    if with_tags:
                        pids.append(f"{k}:{str(v)}")
                    else:
                        pids.append(str(v))
            except TypeError:
                pass
            except ValueError:
                pass
        return pids

    def extract_filtered_named_pids(self, x: Union[dict, List[dict]], tags: List[str] = [], with_tags: bool = False) -> List[str]:
        """
        Method that given a set of SGClima entities (Site, Zone) it returns its named PIDs in the format of
        <named_pid>:<pid>.
        :param: x: SGClima entity
        :param: tags: List of named pids to filter. Returned named pid will match with the ones in the list.
        """
        pids = []
        tags_values = [int(tag.split(":")[-1]) for tag in tags]
        tags_names = [tag.split(":")[0] for tag in tags]
        for k, v in self._extract(x, tags):
            try:
                if k in tags_names and v == tags_values[tags_names.index(k)]:
                    if with_tags:
                        pids.append(f"{k}:{str(v)}")
                    else:
                        pids.append(str(v))
            except TypeError:
                pass
            except ValueError:
                pass
        return pids

    def _extract(self, x, tags):
        if type(x) == dict:
            for k, v in x.items():
                if k.endswith('_pid'):
                    yield k, int(v) if v is not None else None
                else:
                    yield from self._extract(v, tags)
        elif type(x) == list:
            for v in x:
                yield from self._extract(v, tags)
