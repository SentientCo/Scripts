This bot is based off of the Infinity Grid Bot. Instead of buying/selling the difference
it will buy/sell all the crypto in the wallet. High Risk/High Reward

	<=======NEEDS TESTED TO ENSURE PROFITABILITY. USE AT YOUR OWN RISK.=======>

Will need environment variables set.
Env Variables: CB_API_KEY;CB_API_SECRET;CB_API_PASS

This bot only requires the Trade/View options in coinbase! You are responsible for your API Key
access. If anything beyond the scope(Trading and Viewing accounts) of this bot happens YOU are
responsible for your funds.

This bot currently only trade Algorand(ALGO). Going to add more coins at a later date.

API URLS:
URL for general account info: "https://api.pro.coinbase.com/"
URL for a coins price info: "https://api.coinbase.com/v2/"
<--------Requires the trailing "/"------------>

To start this program use powershell or cmd.
1. Open up command prompt or powershell
2. Change directory to "C:/YourFilePath/HighLow/" (cd C:/YourFilePath/HighLow)
3. Collect coin ID pairs with 'python3 coinid.py'
-. Steps added here once user input is implemented.
4. Start program with the python3 command. (python3 start.py)
5. ???
6. profit hopefully.
KEEP IN MIND THIS BOT WILL DRAIN THE USD IN YOUR COINBASE PRO PORTFOLIO TO USE FOR TRADING!
IF THERE ARE FUNDS YOU WANT TO NOT TRADE WITH, MOVE TO A DIFFERENT PORTFOLIO OR TO COINBASE.
IF THIS HAPPENS AND YOU DON'T WANT IT TO THEN IMMEDIATELY SELL THE BOUGHT CRYPTO.
YOU WILL BE AT A LOSS DUE TO TRADING FEES. MISTAKES HAPPEN.

Upon a trade being executed, the logs from the trade will be available in it's own file in
the './cblogs/' folder and in the './logs/' folder.

TODO:
Add all coins available on Coinbase Pro
x--Change the initial buy in to Grid().--x
Shouldn't buy if the market is already up.
Change any GET requests to the WebSocket Feed that Coinbase Pro has avaiable. Will help with any throttling issues. 
 - Try threading to accomplish this. 
 - Should be able to change any check for the spot price to his and possibly account checks.

8/18/2022:
Switched trading to it's own function HL() in hl.py
Added script 'coinid.py' that grabs all crypto and fiat IDs to check accounts with
 - Dumps to a json file as such
	{ crypto1:id1,
	  crypto2:id2
	}

Changed how prices are grabbed from coinbase pro
 - Uses Price(crypto, fiat) in grab_price.py
   - Must supply crypto type and fiat currently trading, returns spot price

Changed how account data is grabbed to retrieve crypto and fiat balances
 - Uses grabAccountData(data) in grab_account_data.py
   - Must supply coin ID that is grabbed from the script 'coinid.py'

9/1/2022: Various bug fixes

