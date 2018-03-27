while :
do
	curl https://api.coinmarketcap.com/v1/ticker/?limit=100 >> data.json
	sleep 10
done