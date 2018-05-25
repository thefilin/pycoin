from pycoin.version import version

import requests

try:
    import urllib2 as request
    from urllib import urlencode  # noqa
except ImportError:
    from urllib import request
    from urllib.parse import urlencode  # noqa


PYCOIN_AGENT = 'pycoin/%s' % version


def urlopen(url, data=None):
    class Wrapper:
        def __init__(self, content):
            self.content = content.encode()

        def read(self):
            return self.content

    req = requests.get(url) if data is None else requests.post(url, data=data)
    return Wrapper(req.text)
