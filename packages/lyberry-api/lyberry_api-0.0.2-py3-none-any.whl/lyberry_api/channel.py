class LBRY_Channel():
    def __init__(self,claim,LBRY_api):
        self._LBRY_api = LBRY_api
        self.raw = claim
        error_occured = False
        try:
            self.id = claim['claim_id']
        except KeyError:
            print('Error parsing channel claim, claim_id not found')
            error_occured = True

        try:
            self.name = claim['name']
        except KeyError as err:
            print('Error parsing channel claim, name not found')
            error_occured = True
            self.name = 'Anonymous'

        if 'canonical_url' in claim:
            self.url = claim['canonical_url']
        elif 'permanent_url' in claim:
            self.url = claim['permanent_url']
        else:
            print('Error finding url in channel claim:')
            error_occured = True
            self.url = ''

        if 'value' in claim:
            self.title = claim['value']['title'] if 'title' in claim['value'] else ''
            self.description = claim['value']['description'] if 'description' in claim['value'] else ''
        else:
            self.title = ''
            self.description = ''

        if error_occured:
            print(claim)

        self.pubs_feed = self.get_pubs_feed()

    def __str__(self):
        return f"LBRY_Channel({self.name})"
    
    def get_pubs_feed(self):
        return self._LBRY_api.channels_feed([self.id])

    def refresh_feed(self):
        self.pubs_feed = self.get_pubs_feed()

class LBRY_Channel_Err(LBRY_Channel):
    def __init__(self):
        self.name = 'Error'
        self.id = '0'
        self.url = ''
        self.description = ''
        self.pubs = []
        self.pubs_feed = iter([])

