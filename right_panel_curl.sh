curl -X POST -H "Content-Type: application/json" --data '{
  "name": "bitcoin",
  "crypto": true,
  "set_nickname": true,
  "frequency": 10,
  "discord_bot_token": "BOT_TOKEN"
}' localhost:8080/ticker

curl -X POST -H "Content-Type: application/json" --data '{
  "name": "ethereum",
  "crypto": true,
  "set_nickname": true,
  "frequency": 10,
  "discord_bot_token": "BOT_TOKEN"
}' localhost:8080/ticker

curl -X POST -H "Content-Type: application/json" --data '{
  "name": "Cryptos",
  "crypto": true,
  "items": ["dogecoin", "monero", "litecoin", "ripple", "polkadot", "cardano", "chainlink", "stellar", "iota",  "algorand", "tezos", "binancecoin", "ecomi", "aave", "uniswap", "tron", "vechain", "cosmos", "zilliqa", "matic-network", "basic-attention-token", "shiba-inu", "pancakeswap-token", "solana", "safemoon", "ftx-token", "enjincoin", "decentraland", "fantom", "sushi", "kusama", "eos", "terra-luna", "theta-token", "tether", "axie-infinity", "harmony"],
  "set_color": false,
  "arrows": false,
  "set_nickname": true,
  "frequency": 5,
  "discord_bot_token": "BOT_TOKEN"
}' localhost:8080/tickerboard


curl -X POST -H "Content-Type: application/json" --data '{
  "network": "polygon",
  "name": "MM",
  "contract": "0x5647Fe4281F8F6F01E84BCE775AD4b828A7b8927",
  "frequency": 3,
  "set_nickname": true,
  "discord_bot_token": "BOT_TOKEN"
}' localhost:8080/token



curl -X POST -H "Content-Type: application/json" --data '{
  "network": "polygon",
  "address": "0x5647Fe4281F8F6F01E84BCE775AD4b828A7b8927",
  "activity": "polygon",
  "set_nickname": true,
  "frequency": 10,
  "discord_bot_token": "BOT_TOKEN"
}' localhost:8080/holders
