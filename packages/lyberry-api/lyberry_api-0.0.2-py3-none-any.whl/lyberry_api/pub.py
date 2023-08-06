import lyberry_api.channel
import lyberry_api.comment

class LBRY_Pub():
    def __init__(self, claim, LBRY_api, channel = {}):
        self._LBRY_api = LBRY_api
        self.comments_feed = self.get_comments_feed()

        self.raw = claim
        if claim["value_type"] == "channel":
            raise ValueError('This is a channel, not a publication')

        if claim["value_type"] == "repost":
            claim = claim["reposted_claim"]

        self._channel = channel
        if not channel:
            self._channel_claim = claim['signing_channel']

        self.id = claim['claim_id']
        self.timestamp = claim['timestamp']
        try:
            self.title = claim['value']['title']
        except:
            self.title = claim['name']
        self.url = claim['canonical_url'] or claim['short_url'] or claim['permanent_url']
        self.media_type = claim['value']['source']['media_type'] if 'source' in claim['value'] else 'video'
        self.license = claim['value']['license'] if 'license' in claim['value'] else 'Undefined'
        self.description = claim['value']['description'] if 'description' in claim['value'] else 'No Description'

        try:
            self.thumbnail = claim['value']['thumbnail']['url']
        except KeyError:
            self.thumbnail = ''

    def __str__(self):
        return f"LBRY_Pub({self.title})"

    @property
    def channel(self):
        if self._channel:
            return self._channel
        else:
            self._channel = lyberry_api.channel.LBRY_Channel(self._channel_claim, self._LBRY_api)
            return self._channel

    def get_content(self):
        self.raw = self._LBRY_api.get(self.url)
        return self.raw

    @property
    def streaming_url(self):
        self.get_content()
        return self.raw['streaming_url']

    def refresh_comments_feed(self):
        self.comments_feed = self.get_comments_feed()

    def get_comments_feed(self):
        page = 1
        self._comments = []
        while True:
            raw_comments = self._LBRY_api.list_comments(self, page=page)
            if not 'items' in raw_comments:
                break
            new_comments = []
            for raw_comment in raw_comments["items"]:
                new_comments.append(lyberry_api.comment.LBRY_Comment(raw_comment, self._LBRY_api, self))
            self._comments.extend(new_comments)
            for comment in new_comments:
                yield comment
            page += 1

    def create_comment(self, commenter, msg):
        self._LBRY_api.make_comment(commenter, msg, self)

