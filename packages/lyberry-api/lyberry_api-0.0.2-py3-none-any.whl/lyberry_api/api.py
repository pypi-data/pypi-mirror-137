import requests
import time
import json
import re
import lyberry_api.channel
import lyberry_api.pub

class LBRY_Api():
    def __init__(self,
            comment_api = 'https://comments.odysee.com/api/v2',
            lbrynet_api = 'http://localhost:5279'
            ):
        self.comment_api = comment_api
        self.lbrynet_api = lbrynet_api

    def connect(self, dur = 10):
        print('connecting to lbrynet')
        attempts = 0
        while attempts < dur:
            try:
                status = self.request("status")
            except ConnectionError:
                print('cannot connect to lbrynet')
                attempts += 1
                time.sleep(1)
                continue

            if status['is_running'] if 'is_running' in status else False:
                print("LBRY connection established!")
                return
            print('lbrynet initiating')
            time.sleep(1)
        raise ConnectionError('Could not connect to lbrynet')

    def online(self):
        try:
            status = self.request("status")
            return status[ 'is_running' ]
        except:
            return False

    def request(self, method, params = {}):
        try:
            res = requests.post(self.lbrynet_api, json={"method": method, "params": params})
        except requests.exceptions.ConnectionError:
            raise ConnectionError('cannot reach lbrynet')
        if not res.ok:
            raise ConnectionError(res.text)
        res_data = res.json()
        if not 'result' in res_data:
            raise ValueError('LBRYnet returned no result')
        return res_data['result']

    def channels_feed_raw(self, ids, page = 1, page_size = 20):
        return self.request('claim_search', {
            "page": page,
            "page_size": page_size,
            "order_by": "release_time",
            "channel_ids": ids
        })

    def id_from_url(self, lbry_url):
        match = re.match(r'lbry://@.*?[:#]([a-f0-9]*)$', lbry_url);
        if match == None:
            raise ValueError(f'could not find id in lbry url: {lbry_url}')
        return match.group(1)

    def get(self, uri):
        if type(uri) != str:
            raise TypeError('Tried to get a URI that was not a string')
        return self.request('get', {'uri': uri})

    def resolve_raw(self, uri):
        res = self.request('resolve', {'urls': uri})[uri]
        if 'error' in res:
            error = res['error']
            raise ValueError(f"lbrynet returned an error:\n{error}")
        return res

    def subs_urls(self):
        prefs_raw = self.request('preference_get')
        return prefs_raw['shared']['value']['subscriptions']

    def subs_ids(self):
        return [self.id_from_url(url) for url in self.subs_urls()]

    def sub_feed(self, page_size = 20):
        return self.channels_feed(self.subs_ids(), page_size)

    def channels_feed(self, ids, page_size = 20):
        page = 1
        while True:
            latest_raw = self.channels_feed_raw(ids, page, page_size)
            if len(latest_raw['items']) == 0:
                break
            for item in latest_raw['items']:
                yield lyberry_api.pub.LBRY_Pub(item, self)
            page += 1

    def list_comments(self, claim, parent = None, page = 1, page_size = 20, sort_by = 3):
        params = {
            "claim_id": claim.id,
            "page": page,
            "page_size": page_size,
            "sort_by": sort_by,
            "top_level": True,
        }
        if parent:
            params["parent_id"] = parent.id
            params["top_level"] = False

        res = requests.post(
            self.comment_api,
            json={
                "method": "comment.List",
                "id": 1,
                "jsonrpc":"2.0",
                "params": params
            }
        ).json()
        return res['result']

    def sign(self, channel, string):
        data = string.encode('utf-8')
        return self.request("channel_sign", {
            "channel_name": channel.name, 
            "hexdata": data.hex(),
            })

    def make_comment(self, commenter, comment, claim, parent = None):
        params = {
            "channel_id": commenter.id,
            "channel_name": commenter.name,
            "claim_id": claim.id,
            "comment": comment,
        }
        params.update(self.sign(commenter, comment))

        if parent:
            params["parent_id"] = parent.id

        try:
            res = requests.post(self.comment_api, json={"method": "comment.Create", "id": 1, "jsonrpc":"2.0", "params": params}).json()
            return res['result']
        except:
            raise Exception(res)

    def channel_from_uri(self, uri):
        raw_claim = self.resolve_raw(uri)
        if 'error' in raw_claim:
            error = raw_claim['error']
            print(f"lbrynet returned an error:\n{error['name']}: {error['text']}")
            return lyberry_api.channel.LBRY_Channel_Err()
        else:
            channel = lyberry_api.channel.LBRY_Channel(raw_claim, self)
            return channel

    def pub_from_uri(self, uri):
        raw_claim = self.resolve_raw(uri)
        return lyberry_api.pub.LBRY_Pub(raw_claim, self)

    def resolve(self, uri):
        raw_claim = self.resolve_raw(uri)
        if raw_claim['value_type'] == 'channel':
            return lyberry_api.channel.LBRY_Channel(raw_claim, self)
        elif raw_claim['value_type'] == 'stream':
            return lyberry_api.pub.LBRY_Pub(raw_claim, self)

    def my_channels(self):
        raw_channels = self.request("channel_list")["items"]
        channels = []
        for raw_channel in raw_channels:
            channels.append(lyberry_api.channel.LBRY_Channel(raw_channel, self))
        return list(channels)
