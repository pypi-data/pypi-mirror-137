import lyberry_api.channel

class LBRY_Comment():
    def __init__(self, raw_comment, LBRY_api, pub):
        self._LBRY_api = LBRY_api
        self.raw = raw_comment
        self.channel_url = raw_comment['channel_url']
        self.msg = raw_comment['comment']
        self.id = raw_comment['comment_id']
        self.timestamp = raw_comment['timestamp']
        self.replies_amt = raw_comment['replies'] if 'replies' in raw_comment else 0
        self.pub = pub
        self._replies = []
        self.got_replies = False


    def __str__(self):
        return f"LBRY_Comment({self.msg})"

    @property
    def channel(self):
        return self._LBRY_api.channel_from_uri(self.channel_url)

    def refresh_replies(self):
        raw_comments = self._LBRY_api.list_comments(
            claim = self.pub,
            parent = self,
        )
        self._replies = []
        if 'items' in raw_comments:
            for child in raw_comments['items']:
                self.__add_child(child)
        self.got_replies = True
        return self._replies

    def __add_child(self, child):
        self._replies.append(LBRY_Comment(child, self._LBRY_api, self.pub))

    @property
    def replies(self):
        if self.got_replies:
            return self._replies
        else:
            return self.refresh_replies()

    def create_reply(self, commenter, msg):
        self._LBRY_api.make_comment(commenter, msg, self.pub, parent = self)
