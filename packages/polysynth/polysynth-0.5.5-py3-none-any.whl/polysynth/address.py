from typing import Dict

from web3 import Web3
from web3.types import ChecksumAddress


address_mumbai: Dict[str, ChecksumAddress] = {
    k: Web3.toChecksumAddress(v)
    for k, v in {
        "StableToken": "0x27f43eF37bc44120eDD91626f40C6DFa8908300C",
        "Manager": "0x25074928fA2cDd06Fb9f0902d710f7EDB494dbe2",
        "Amm_eth-usdc": "0x9e7225628bB6f9F437F123287602f59d705c8AA1",
        "Amm_btc-usdc": "0x40Ff56e22D26B41F13f79D61311e7DA605C0c4c2",
        "Amm_matic-usdc": "0xaB0BcF1F2f24145EcB2EAF3A11B8E1A25A839de7",
        "AmmReader": "0x410325f7A08FD56374a822db318E2593c9e5F5C8"
    }.items()
}
}

address_mumbai: Dict[str, ChecksumAddress] = {
    k: Web3.toChecksumAddress(v)
    for k, v in {
        "StableToken": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",            
        "Manager": "0x84B056EB1107f8F8B127a57De0222A8A211C1e42",
        "Amm_eth-usdc": "0x80081DD1EEedbc8631c3077D4204bEa7270de891",
        "Amm_btc-usdc": "0xAE6dFb1923052890a077A135498F2B34A40F69Cc",
        "Amm_matic-usdc": "0x07429D7fDd2651d2712D87fd434669B1908dd5DA",
        "Amm_sol-usdc": "0xa23Ac746740cfE9013d94e62f7b0f1376EdCa759",
        "Amm_dot-usdc": "0x6F88D5D707908e961228C4708D19a6252B546e13",
        "AmmReader": "0x3e33b0FefD9C1886bd07C3308212f0f4a7c4A38d"
    }.items()
}
}