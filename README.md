# Crypto Text Trader	
[Hackathon submission](https://devpost.com/software/crypto-phone-trader)  

Trade crypto from your phone, quickly, easily, seemlessly, using binance and twilio  

## How to use
Create a binance account, and get the apikey and apisecret. Sign up using the following command:
`curl -X POST https://<localhost or server>  
   -H 'Content-Type: application/json'  
   -d '{"number":"<mynumber>","apikey":"<api_key>", "apisecret", "<api_secret>"}'`  

Execute trades with the following commands:  
- Buy coin: `BUY <coin> <amount> `
- Sell coin: `SELL <coin> <amount> `
- Get current price of coin (in USDT): `GET <coin>  `
- Get current balance (in USDT): `BALANCE <coin>  `

