#/bin/sh
echo "killing running processes..."
pkill -9 -f bot_

echo "fetching latest code..."
git reset --hard HEAD && git pull

echo "running bot_data.py"
nohup python3 bot_data.py prod > output_data.log &

echo "running bot_reactions.py"
nohup python3 bot_reactions.py prod > output_reactions.log &

echo "running bot_welcome_goodbye.py"
nohup python3 bot_welcome_goodbye.py prod > output_welcome_goodbye.log &

echo "printing processes..."
ps ax | grep "python3 bot_*"
