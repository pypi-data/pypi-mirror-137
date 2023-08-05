import random

import requests

from .data import string_to_raw, time_to_raw, float_to_raw
from .stream import Stream


class Client:

    def __init__(self, system_url='https://api.vyze.io/system/', stream_url='wss://api.vyze.io/stream', app_url='https://api.vyze.io/app/', timeout=300):
        self.__app_url = app_url
        self.__stream_url = stream_url
        self.__system_url = system_url

        self.__universe = None
        self.__space = None

        self.__user_id = None
        self.__refresh_token = None
        self.__access_token = None
        self.__space_tokens = {}

        self.__resolve_cache = {}
        self.__abstract_cache = {}
        self.__special_cache = {}
        self.__targets_cache = {}
        self.__origins_cache = {}

        self.__timeout = timeout

    def login(self, username, password):
        resp = requests.post(f'{self.__app_url}user/login', json={
            'username': username,
            'password': password,
        })

        if resp.status_code != 200:
            return False

        self.__user_id = resp.json()['userId']
        self.__refresh_token = resp.json()['refreshToken']

        self.__refresh()

        return True

    def resolve_universe(self, name):
        return self.__get(f'{self.__app_url}universe/resolve/{name}')

    def use_universe(self, name):
        universe_id = self.resolve_universe(name)
        if not universe_id:
            raise RuntimeError('invalid universe')
        self.__universe = self.__get(f'{self.__app_url}universe/{universe_id}')
        if not self.__universe:
            raise RuntimeError('could not resolve universe')
        self.__space = self.__universe['space']

    def resolve(self, identifier):
        if isinstance(identifier, list):
            return [self.resolve(i) for i in identifier]

        if len(identifier) == 32:
            return identifier

        if '.' not in identifier:
            if not self.__universe:
                raise RuntimeError('no universe selected')
            identifier = f'{self.__universe["name"]}.{identifier}'

        if '/' not in identifier:
            if not self.__universe:
                raise RuntimeError('no universe selected')
            identifier = f'{identifier}/{self.__universe["name"]}'

        obj = self.__resolve_cache.get(identifier)
        if obj is None:
            resp = requests.get(f'{self.__app_url}universe/resolve', params={'i': identifier})
            obj = resp.json()
            self.__resolve_cache[identifier] = obj

        return obj

    def create_object(self, abstracts, name='', space=None, dependent=False):
        if not isinstance(abstracts, list):
            abstracts = [abstracts]
        if not space:
            if not self.__space:
                raise RuntimeError('no universe or space selected')
            space = self.__space

        return self.__post(f'{self.__system_url}objects', {
            'abstracts': self.resolve(abstracts),
            'space': space,
            'name': name,
            'dependent': dependent,
        })['object']

    def create_relation(self, origin_id, target_id, abstracts, name='', space=None, time=None):
        if not isinstance(abstracts, list):
            abstracts = [abstracts]
        if not space:
            if not self.__space:
                raise RuntimeError('no universe or space selected')
            space = self.__space

        body = {
            'origin': origin_id,
            'target': target_id,
            'abstracts': self.resolve(abstracts),
            'space': space,
            'name': name
        }

        if time is not None:
            body['time'] = time.isoformat() + 'Z'

        return self.__post(f'{self.__system_url}relations', body)['relation']

    def get_object(self, id: str):
        return self.__get(f'{self.__system_url}objects/{self.resolve(id)}')['object']

    def delete_object(self, id: str):
        return self.__delete(f'{self.__system_url}objects/{self.resolve(id)}')

    def set_name(self, id: str, name: str):
        self.__post(f'{self.__system_url}objects/{self.resolve(id)}/name', {
            'name': name,
        })

    def get_data(self, id: str) -> bytes:
        return self.__get(f'{self.__system_url}objects/{self.resolve(id)}/data', is_json=False)

    def set_data(self, id: str, data: bytes, chunks=None, update=None):
        if not chunks:
            return self.__post(f'{self.__system_url}objects/{self.resolve(id)}/data', data, is_json=False) is not False
        else:
            offset = 0
            while True:
                if update:
                    update(offset, len(data))
                data_chunk = data[offset:min(offset + chunks, len(data))]
                if self.__post(f'{self.__system_url}objects/{self.resolve(id)}/data?a=1', data_chunk, is_json=False) is False:
                    return False
                offset += chunks
                if offset >= len(data):
                    if update:
                        update(len(data), len(data))
                    return True

    def get_abstracts(self, id: str, include_self=False, include_direct=True, include_transitive=False):
        return self.__get_hierarchy(self.resolve(id), include_self, include_direct, include_transitive, 'abstracts', self.__abstract_cache)

    def get_specials(self, id: str, include_self=False, include_direct=True, include_transitive=False):
        return self.__get_hierarchy(self.resolve(id), include_self, include_direct, include_transitive, 'specials', self.__special_cache)

    def get_targets(self, id: str) -> dict:
        return self.__get_relations(self.resolve(id), 'targets', self.__targets_cache)

    def get_origins(self, id: str) -> dict:
        return self.__get_relations(self.resolve(id), 'origins', self.__origins_cache)

    def set_value(self, id: str, field: str, value):
        self.add_value(id, field, value)

    def add_value(self, id: str, field: str, value, time=None):
        field_id = self.resolve(field)
        targets = self.get_targets(field_id)
        target_id = targets['ffffffffffffffffffffffffffffffff']
        data = self.__get_type(target_id)
        if data == 'string':
            data = string_to_raw(value)
        elif data == 'float':
            data = float_to_raw(value)
        elif data == 'time':
            data = time_to_raw(value)
        target = self.create_object([target_id], dependent=True)
        self.set_data(target['id'], data)
        r = self.create_relation(id, target['id'], [field_id], time=time)
        return r

    def get_value(self, id: str, field: str) -> any:
        vals = self.get_values(id, field)
        return vals[0] if len(vals) == 1 else None

    def get_values(self, id: str, field: str):
        field_id = self.resolve(field)
        query, abbr = self.__get_values_query(field_id, 'val')
        vals = self.query(query, {'obj': {'id': id}, abbr: {'id': field_id}})
        return [v['val'] for v in vals]

    def get_dict_values(self, id: str, defs: dict, names):
        query = ''
        d = {}
        v = {}
        for name in names:
            field_id = self.resolve(defs[name])
            frag, abbr = self.__get_values_query(field_id, name)
            query += frag
            v[abbr] = {'id': field_id}
        v['obj'] = {'id': id}
        vals = self.query(query, v)
        if not vals or len(vals) != 1:
            return None
        return vals[0]

    def set_dict_values(self, id: str, defs: dict, vals: dict):
        items = list(vals.items())
        random.shuffle(items)
        for key, val in items:
            self.set_value(id, defs[key], val)

    def stream(self) -> Stream:
        return Stream(self, self.__stream_url)

    def query(self, query, valuation):
        return self.__post(f'{self.__system_url}text_query', {
            'query': query,
            'valuation': valuation,
        })['valuations']

    def __get_values_query(self, field_id, name):
        targets = self.get_targets(field_id)
        target_id = targets['ffffffffffffffffffffffffffffffff']
        data = self.__get_type(target_id)
        abbr = 'A' + field_id[:6]
        return f'$obj.[_:${abbr}] == {abbr};' \
               f'{data}({abbr}) => {name};', abbr

    def __get_type(self, id: str):
        abs = self.get_abstracts(id, True, True, True)
        if self.resolve('data.@string') in abs:
            return 'string'
        if self.resolve('data.@float') in abs:
            return 'float'
        if self.resolve('data.@integer') in abs:
            return 'int'
        if self.resolve('data.@boolean') in abs:
            return 'boolean'
        if self.resolve('data.@time') in abs:
            return 'time'
        return None

    def __get_hierarchy(self, id: str, include_self: bool, include_direct: bool, include_transitive: bool, name: str, cache: dict):
        ck = f'{id}_{"1" if include_self else "0"}{"1" if include_direct else "0"}{"1" if include_transitive else "0"}'
        hier = cache.get(ck)
        if not hier:
            hier = self.__get(
                f'{self.__system_url}objects/{id}/{name}'
                f'?self={"1" if include_self else "0"}'
                f'&direct={"1" if include_direct else "0"}'
                f'&transitive={"1" if include_transitive else "0"}')['ids']
            cache[ck] = hier
        return hier

    def __get_relations(self, id: str, name: str, cache: dict) -> dict:
        ck = f'{id}'
        rel = cache.get(ck)
        if not rel:
            resp = self.__get(f'{self.__system_url}objects/{id}/{name}')
            if resp:
                rel = resp['idPairs']
                cache[ck] = rel
        return rel

    def __get(self, url, is_json=True, **kwargs):
        resp = requests.get(url, headers=self.__get_headers(), timeout=self.__timeout, **kwargs)
        if resp.status_code == 200:
            return resp.json() if is_json else resp.content
        elif resp.status_code == 403:
            if self.__request_permission(resp.text):
                return self.__get(url, is_json=is_json, **kwargs)
        return None

    def __post(self, url, data, is_json=True, **kwargs):
        if is_json:
            resp = requests.post(url, json=data, headers=self.__get_headers(), timeout=self.__timeout, **kwargs)
        else:
            resp = requests.post(url, data=data, headers=self.__get_headers(), timeout=self.__timeout, **kwargs)
        if resp.status_code == 200:
            return resp.json() if is_json else resp.content
        elif resp.status_code == 403:
            if self.__request_permission(resp.text):
                return self.__post(url, data=data, is_json=is_json, **kwargs)
            else:
                return False
        else:
            return False

    def __put(self, url, data, is_json=True, **kwargs):
        if is_json:
            resp = requests.post(url, json=data, headers=self.__get_headers(), timeout=self.__timeout, **kwargs)
        else:
            resp = requests.post(url, data=data, headers=self.__get_headers(), timeout=self.__timeout, **kwargs)
        if resp.status_code == 200:
            return resp.json() if is_json else resp.content
        elif resp.status_code == 403:
            if self.__request_permission(resp.text):
                return self.__put(url, data=data, is_json=is_json, **kwargs)
        return None

    def __delete(self, url, is_json=True, **kwargs):
        resp = requests.delete(url, headers=self.__get_headers(), timeout=self.__timeout, **kwargs)
        if resp.status_code == 200:
            return resp.json() if is_json else resp.content
        elif resp.status_code == 403:
            if self.__request_permission(resp.text):
                return self.__delete(url, is_json=is_json, **kwargs)
        return None

    def __refresh(self):
        resp = requests.post(f'{self.__app_url}user/refresh', json={
            'userId': self.__user_id,
            'refreshToken': self.__refresh_token,
        }, timeout=self.__timeout)

        if resp.status_code != 200:
            return False

        login_info = resp.json()
        self.__access_token = login_info['accessToken']

        return True

    def __request_permission(self, req):
        if req == 'token expired':
            return self.__refresh()

        perm_reqs = req.split('/')
        if perm_reqs[0] == '00000000000000000000000000000000' or perm_reqs[0] == '':
            return False

        tk = self.__space_tokens.get(perm_reqs[0])
        if tk is not None:
            return False

        perms = int(perm_reqs[1], 16)

        resp = self.__get(f'{self.__app_url}permission/{perm_reqs[0]}')
        if (perms & resp['perms']) != perms:
            return False

        self.__space_tokens[req] = resp

        return True

    def __get_headers(self, cached=False):
        return {
            'Authorization': f'Baerer {self.__access_token}',
            'x-vy-spaces': ','.join([v['token'] for (k, v) in self.__space_tokens.items()]),
            'x-vy-bypass-cache': '1' if cached else '0',
        }
