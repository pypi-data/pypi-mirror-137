from blockapi.v2.api.covalenth.ethereum import EthCovalentApi
from blockapi.v2.api.covalenth.klaytn import KlaytnCovalentApi
from blockapi.v2.api.covalenth.palm import PalmCovalentApi
from blockapi.v2.api.covalenth.polygon import PolygonCovalentApi
from blockapi.v2.api.covalenth.avalanche import AvalancheCovalentApi
from blockapi.v2.api.covalenth.astar import AstarCovalentApi

if __name__ == "__main__":
    # balances = EthCovalentApi(api_key="ckey_fa6ccdb000d048b79382f2fb9ef").get_balance("0x739c65cbc2c702b72d12e7a829cdb637fa922015")
    # print(str(list(balances)))

    balances = PalmCovalentApi(api_key="ckey_fa6ccdb000d048b79382f2fb9ef").get_balance(
        "0xfc43f5f9dd45258b3aff31bdbe6561d97e8b71de")
    print(str(list(balances)))