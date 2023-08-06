# see: https://chainid.network/chains/
_netid_to_name = {
    137: "matic",
    80001: "mumbai",
    31337: "local"
}

_contract_addresses_proxy_v1 = {
    "mumbai": {
        "StableToken": "0x27f43eF37bc44120eDD91626f40C6DFa8908300C",
        "Manager": "0x25074928fA2cDd06Fb9f0902d710f7EDB494dbe2",
        "Amm_eth-usdc": "0x9e7225628bB6f9F437F123287602f59d705c8AA1",
        "Amm_btc-usdc": "0x40Ff56e22D26B41F13f79D61311e7DA605C0c4c2",
        "Amm_matic-usdc": "0xaB0BcF1F2f24145EcB2EAF3A11B8E1A25A839de7",
        "AmmReader": "0x410325f7A08FD56374a822db318E2593c9e5F5C8"
    },
    "local": {
        "StableToken": "0x5FbDB2315678afecb367f032d93F642f64180aa3",
        "Manager": "0x5FC8d32690cc91D4c39d9d3abcBD16989F875707",
        "Amm_eth-usdc": "0x0DCd1Bf9A1b36cE34237eEaFef220932846BCD82",
        "Amm_btc-usdc": "0x9A9f2CCfdE556A7E9Ff0848998Aa4a0CFD8863AE",
        "Amm_matic-usdc": "0x59b670e9fA9D0A427751Af201D676719a970857b",
        "AmmReader": "0xB7f8BC63BbcaD18155201308C8f3540b07f84F5e"
    },
    "matic": {
        "StableToken": "0x2791bca1f2de4661ed88a30c99a7a9449aa84174",            
        "Manager": "0x84B056EB1107f8F8B127a57De0222A8A211C1e42",
        "Amm_eth-usdc": "0x80081DD1EEedbc8631c3077D4204bEa7270de891",
        "Amm_btc-usdc": "0xAE6dFb1923052890a077A135498F2B34A40F69Cc",
        "Amm_matic-usdc": "0x07429D7fDd2651d2712D87fd434669B1908dd5DA",
        "Amm_sol-usdc": "0xa23Ac746740cfE9013d94e62f7b0f1376EdCa759",
        "Amm_dot-usdc": "0x6F88D5D707908e961228C4708D19a6252B546e13",
        "AmmReader": "0x3e33b0FefD9C1886bd07C3308212f0f4a7c4A38d"
    }
}

_contract_addresses_oracle = {
    "mumbai": {
        "eth-usdc": "0x0715A7794a1dc8e42615F059dD6e406A6594651A",
        "btc-usdc": "0x007A22900a3B98143368Bd5906f8E17e9867581b",
        "matic-usdc": "0xd0D5e3DB44DE05E9F294BB0a3bEEaF030DE24Ada",
    },
    "local": {
        "eth-usdc": "0x0715A7794a1dc8e42615F059dD6e406A6594651A",
        "btc-usdc": "0x007A22900a3B98143368Bd5906f8E17e9867581b",
        "matic-usdc": "0xd0D5e3DB44DE05E9F294BB0a3bEEaF030DE24Ada",
    },
    "matic": {
        "eth-usdc": "0xF9680D99D6C9589e2a93a78A04A279e509205945",
        "btc-usdc": "0xc907E116054Ad103354f2D350FD2514433D57F6f",
        "matic-usdc": "0xAB594600376Ec9fD91F8e885dADF0CE036862dE0",
        "sol-usdc": "0x10C8264C0935b3B9870013e057f330Ff3e9C56dC",
        "dot-usdc": "0xacb51F1a83922632ca02B25a8164c10748001BdE",
    }
}