import copy
from dataclasses import dataclass

from sust.api.generated.climate_explorer import ApiClient, Configuration
from sust.api.generated.climate_explorer.api import portfolios_api
from sust.api.generated.climate_explorer.model.portfolio_create_request import PortfolioCreateRequest


@dataclass(frozen=True)
class Scenarios:
    SSP126 = 'ssp126'
    SSP245 = 'ssp245'
    SSP585 = 'ssp585'


@dataclass(frozen=True)
class RiskTypes:
    FIRE = "fire"
    FLOOD = "flood"
    SPEI = "SPEI"
    SLR = "SLR"
    HEATWAVES = "heatwaves"
    OBS_FIRE = "obs_fire"
    OBS_FLOOD = "obs_flood"
    OBS_CYCLONE = "obs_cyclone"


class ClimateExplorerClient:
    def __init__(self, api_key, project=None, endpoint=None):
        self._default_req_kwargs = {}
        if project:
            self._default_req_kwargs['project'] = project

        self._openapi_config = Configuration(host=endpoint)
        self._openapi_config.api_key['api_key'] = api_key

        openapi_client = ApiClient(self._openapi_config)
        self._openapi_instance = portfolios_api.PortfoliosApi(openapi_client)

    def _openapi_request(self, request_name, request_args, request_kwargs):
        rk = copy.deepcopy(self._default_req_kwargs)
        rk.update(request_kwargs)
        return getattr(self._openapi_instance, request_name)(*request_args, **rk)

    def _paginated_openapi_request(self, request_name, request_args, request_kwargs):
        rk = copy.deepcopy(self._default_req_kwargs)
        rk.update(request_kwargs)
        return PageIterator(getattr(self._openapi_instance, request_name), request_args, rk)

    def portfolios(self):
        #NOTE(bcwaldon): this should be paginated, but is not yet implemented in the API
        it = self._openapi_request('portfolios_list', (), {})
        return (Portfolio(self, obj) for obj in it)
        
    def create(self, portfolio_name):
        req = PortfolioCreateRequest(portfolio_name)
        obj = self._openapi_request('portfolios_create', (req,), {})
        return Portfolio(self, obj)
        
    def upload_assets(self, portfolio_name, assets_path):
        file = open(assets_path, "rb")
        obj = self._openapi_request('portfolios_assets_import_create', (portfolio_name, file), {})
        return obj
    
        

    def portfolio(self, portfolio_name):
        obj = self._openapi_request('portfolios_read', (portfolio_name,), {})
        return Portfolio(self, obj)


class Portfolio:
    def __init__(self, client, obj):
        self._client = client
        self._obj = obj
        self.name = obj["portfolio_name"]

    def __getitem__(self, key):
        return self._obj[key]

    def assets(self, labels=None):
        it = self._client._paginated_openapi_request('portfolios_assets_list', (self._obj['portfolio_name'],), {})

        objects = [
            obj for obj in it if
              (labels == None or all(obj['labels'].get(k) == v for k, v in labels.items()))
        ]

        return AssetList(self._client, self, objects)
        
        

class AssetList:
    def __init__(self, client, portfolio, objects):
        self._client = client
        self._portfolio = portfolio
        self._objects = objects
        self._index = dict((obj['entity_id'], obj) for obj in objects)

    def to_dicts(self):
        return [obj.to_dict() for obj in self._objects]

    def physical_risk_timeseries(self, scenario=None, risk_type=None):
        req_kwargs = {}
        if scenario:
            req_kwargs['scenario'] = scenario
        if risk_type:
            req_kwargs['risk_type'] = risk_type

        it = self._client._paginated_openapi_request('portfolios_datasets_physical_items_list', (self._portfolio['portfolio_name'],), req_kwargs)

        objects = []
        for obj in it:
            if obj['entity_id'] not in self._index:
                continue
            obj_d = obj.to_dict()
            re = obj_d.pop('risk_exposure')
            obj_d.update(re)
            objects.append(obj_d)

        return PhysicalRiskAnnualList(objects)

    def physical_risk_summary(self, scenario=None):
        req_kwargs = {}
        if scenario:
            req_kwargs['scenario'] = scenario

        it = self._client._paginated_openapi_request('portfolios_datasets_physical_summary_list', (self._portfolio['portfolio_name'],), req_kwargs)

        objects = []
        for obj in it:
            if obj['entity_id'] not in self._index:
                continue
            obj_d = obj.to_dict()
            summaries = obj_d.pop('risk_summary')
            for (scenario, summary) in summaries.items():
                obj_d_cp = copy.deepcopy(obj_d)
                obj_d_cp['scenario'] = scenario
                obj_d_cp.update(summary)
                objects.append(obj_d_cp)

        return PhysicalRiskSummaryList(objects)


class PhysicalRiskAnnualList:
    def __init__(self, dict_objects):
        self._dict_objects = dict_objects

    def to_dicts(self):
        return self._dict_objects


class PhysicalRiskSummaryList:
    def __init__(self, dict_objects):
        self._dict_objects = dict_objects

    def to_dicts(self):
        return self._dict_objects


class PageIterator:
    def __init__(self, req_func, req_args, req_kwargs):
        self.req_func = req_func
        self.req_args = req_args
        self.req_kwargs = req_kwargs

        self.req_kwargs['page'] = 1
        self.req_kwargs.setdefault('rows', 100)

        self.cache = []
        self.exhausted = False

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.cache) == 0 and not self.exhausted:
            resp = self.req_func(*self.req_args, **self.req_kwargs)
            self.cache = resp

            if len(resp) < self.req_kwargs['rows']:
                self.exhausted = True
            else:
                self.req_kwargs['page'] = self.req_kwargs['page'] + 1

        if len(self.cache) > 0:
            return self.cache.pop(0)

        raise StopIteration
