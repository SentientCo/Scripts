This bot is based off of the Infinity Grid Bot.

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

9/7/2022: Overhaul of the code for security and ease of use. Used the scripts made when 
	  writing the High/Low Trading Bot.
	  
	  
Please feel free to donate it will be appreciated! Thank you in advance!
ALGO: 2WTX3VOXMPEA2TXVD7NN4PQHSJZY7AJS66BQA5WTMW5LX2B6SWYNSPXABM
ETH: 0xB893D5c9EbF9478539632442700E334316C0F9b3
BTC: 3NCpNd1TgbD7jYFfUThywuqaMANgsBcS8F
