# Python Bot

```shell
cd /home/discord/MMBot
git reset --hard HEAD && git pull
ps ax | grep bot.py
kill 9 <process_id>
nohup python3 bot.py prod > output.log &
```

# Golang Bot
```shell
wget https://github.com/rssnyder/discord-stock-ticker/releases/download/v3.3.0/discord-stock-ticker-v3.3.0-linux-amd64.tar.gz
tar zxf discord-stock-ticker-v3.3.0-linux-amd64.tar.gz
mkdir -p /etc/discord-stock-ticker
mv discord-stock-ticker /etc/discord-stock-ticker/
wget https://raw.githubusercontent.com/rssnyder/discord-stock-ticker/master/discord-stock-ticker.service
mv discord-stock-ticker.service /etc/systemd/system/
systemctl daemon-reload
systemctl start discord-stock-ticker.service
```
