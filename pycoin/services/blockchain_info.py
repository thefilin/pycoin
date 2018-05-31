import json

from .agent import urlopen

from pycoin.serialize import h2b, b2h_rev
from pycoin.tx.Tx import Spendable, Tx


class BlockchainInfoProvider(object):
    def __init__(self, netcode):
        if netcode != 'BTC':
            raise ValueError("BlockchainInfo only supports mainnet")

    def tx_for_tx_hash(self, tx_hash):
        "Get a Tx by its hash."
        URL = "https://blockchain.info/rawtx/%s?format=hex" % b2h_rev(tx_hash)
        tx = Tx.from_hex(urlopen(URL).read().decode("utf8"))
        return tx

    def payments_for_address(self, bitcoin_address):
        "return an array of (TX ids, net_payment)"
        URL = "https://blockchain.info/address/%s?format=json" % bitcoin_address
        d = urlopen(URL).read()
        json_response = json.loads(d.decode("utf8"))
        response = []
        for tx in json_response.get("txs", []):
            total_out = 0
            for tx_out in tx.get("out", []):
                if tx_out.get("addr") == bitcoin_address:
                    total_out += tx_out.get("value", 0)
            if total_out > 0:
                response.append((tx.get("hash"), total_out))
        return response

    def spendables_for_address(self, bitcoin_address):
        """
        Return a list of Spendable objects for the
        given bitcoin address.
        """
        URL = "https://blockchain.info/unspent?active=%s" % bitcoin_address
        r = json.loads(urlopen(URL).read().decode("utf8"))
        spendables = []
        for u in r["unspent_outputs"]:
            coin_value = u["value"]
            script = h2b(u["script"])
            previous_hash = h2b(u["tx_hash"])
            previous_index = u["tx_output_n"]
            spendables.append(Spendable(coin_value, script, previous_hash, previous_index))
        return spendables
