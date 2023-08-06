# see: https://chainid.network/chains/
_netid_to_name = {
    137: "matic",
    80001: "mumbai",
    31337: "local"
}

_contract_addresses_proxy_v1 = {
    "mumbai": {
        "StableToken": "0x2E4c42aB89E8f928C74571Bb54C2DaA28605937B",
        "Manager": "0xc7Bf6E9a1EE40EB452712F219Ffd57D0feE0691c",
        "Amm_eth-usdc": "0x9fFeBA1A8cD88D0BDb996Cf75A993fdAfEE8f4f6",
        "Amm_btc-usdc": "0xec8c5521c4Df81be57436a5DC9e2Ac4C888E0054",
        "Amm_matic-usdc": "0x74456feE1Cf361787EA0545B7f075A72084a3965",
        "AmmReader": "0x314426488153C2867Dbb1FC1dee3B406F9E3c7B0"
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
        "Manager": "0x6D171813A179520Dc5f1F62a699940eC537730F4",
        "Amm_eth-usdc": "0x44ecda99159270f6e2a328d3ae03d0aa2e4c6e89",
        "Amm_btc-usdc": "0x017af3e292554580671c6cf51321d2eda64de862",
        "Amm_matic-usdc": "0x2b538e01c3686d4a0a38657106c0cf442c74979f",
        "Amm_sol-usdc": "0x355b5f5a394ca7058bb853879cce8e5b13167432",
        "Amm_dot-usdc": "0x26691b6e1cb0f908926149fa58326ad4966d0aa5",
        "AmmReader": "0xe3774bF2EAc6716e1ef67B77AEcd6eBB3A2f84Ca"
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