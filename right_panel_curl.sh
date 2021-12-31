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
  "network": "polygon",
  "address": "0x5647Fe4281F8F6F01E84BCE775AD4b828A7b8927",
  "activity": "polygon",
  "set_nickname": true,
  "frequency": 10,
  "discord_bot_token": "BOT_TOKEN"
}' localhost:8080/holders
