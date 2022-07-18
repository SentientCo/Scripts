This bot is based off of the Infinity Grid Bot. Instead of buying/selling the difference
it will buy/sell all the crypto in the wallet. High Risk/High Reward

Will need environment variables set.
Env Variables: CB_API_KEY;CB_API_SECRET;CB_API_PASS

API URLS:
URL for general account info: "https://api.pro.coinbase.com/"
URL for a coins price info: "https://api.coinbase.com/v2/"
<--------Requires the trailing "/"------------>

Upon a trade being executed, the logs from the trade will be available in it's own file in
the './cblogs/' folder and in the './logs/' folder.