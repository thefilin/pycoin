import json
from .agent import urlopen

from pycoin.serialize import b2h_rev
from pycoin.tx.Tx import Tx


class BlockExplorerProvider(object):
    def __init__(self, netcode):
        url_stub = {"BTC": "blockexplorer.com", "XTN": "testnet.blockexplorer.com"}.get(netcode)
        if url_stub is None:
            raise ValueError("unsupported netcode %s" % netcode)
        self.url = "https://%s/api" % url_stub

    def tx_for_tx_hash(self, tx_hash):
        """
        Get a Tx by its hash.
        """
        url = "%s/rawtx/%s" % (self.url, b2h_rev(tx_hash))
        d = urlopen(url).read()
        j = json.loads(d.decode("utf8"))
        tx = Tx.from_hex(j.get("rawtx", ""))
        if tx.hash() == tx_hash:
            return tx

    def get_balance(self, address):
        url = self.url + "/addr/%s/balance" % address
        result = json.loads(urlopen(url).read().decode("utf8"))
        return result

    def broadcast_tx(self, tx):
        """
        broadcast a transaction to the network
        """
        if type(tx) is str:
            tx_hex = tx
        else:
            tx_hex = tx.as_hex()

        url = self.url + "/tx/send"
        data = {"rawtx": tx_hex}
        result = json.loads(urlopen(url, data=data).read().decode("utf8"))
        return result['txid']
