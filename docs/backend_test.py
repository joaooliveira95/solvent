# Backend test tutorial
# this python script shows how to use the backend APIs

import requests

base_url = "https://solventgpt-staging-r5i554wrlq-uc.a.run.app"

# this will execute an endpoint to get the jwt_token. This is temporary, the UI should call
# directly the supabase endpoint that is used for authentication

res = requests.post(base_url + "/test/login", json={"username": "user20@solvent.life", "password": "dslaxLSl49"})
jwt_token = res.json()["token"]

# building the header with the authorization token

headers={"Authorization": f"Bearer {jwt_token}"}



userplan = requests.get(base_url + "/v1/user/plan", headers=headers).json()
userplan

{'user_id': '3ede53c1-fb18-4bb8-8897-f9f819ef73ff',
 'email': '',
 'plan_type': 'free',
 'plan_limit': 5,
 'plan_usage': 0,
 'renew_at': '2024-05-23T00:00:00Z'}

# Start a conversation (this will generate a new conversation ID). Each
# time the user starts a new chat session a new id should be generated.

conv = requests.post(base_url + "/v1/conversation", headers=headers).json()
conv

{'conversation_id': '6c23239b-b5b3-4a7f-b80b-513dab06f643',
 'user_id': '3ede53c1-fb18-4bb8-8897-f9f819ef73ff',
 'created': '2024-05-22 16:12:25.531558',
 'title': '',
 'messages': []}


# Send first chat message

data = {
    "conversation_id": conv["conversation_id"],
    "user_id": conv["user_id"],
    "messages": [{"role": "user", "content": "What is the stock price for Nvidia?"}]
}
chat = requests.post(base_url + "/v1/agent/completion", json=data, headers=headers).json()
chat

{'conversation_id': '6c23239b-b5b3-4a7f-b80b-513dab06f643',
 'user_id': '3ede53c1-fb18-4bb8-8897-f9f819ef73ff',
 'created': '2024-05-22 16:25:11.964368',
 'message': {'role': 'assistant',
  'content': 'The current stock price for Nvidia (NVDA) is displayed in the interactive chart above. Here is the interactive chart.\n<iframe style="width: 100%; height: 425px" srcdoc=\'<!-- TradingView Widget BEGIN -->\n<html style="width: 100%; height: 100%; overflow: hidden"><body style="width: 100%; height: 100%; margin: 0; overflow: hidden">\n<style>.tradingview-widget-container .tradingview-widget-copyright {display: none;}</style>\n<div class="tradingview-widget-container" style="height:100%;width:100%">\n  <div class="tradingview-widget-container__widget" style="height:calc(100% - 10px);width:100%"></div>\n  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>\n  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>\n  {\n  "autosize": true,\n  "symbol": "NVDA",\n  "interval": "H",\n  "timezone": "Etc/UTC",\n  "theme": "dark",\n  "style": "1",\n  "locale": "en",\n  "enable_publishing": false,\n  "allow_symbol_change": true,\n  "calendar": false,\n  "support_host": ""\n}\n  </script>\n</div>\n</body></html>\n<!-- TradingView Widget END -->\'></iframe>'}}

# Check the conversation details from the user are correct in the database

convdetail = requests.get(base_url + "/v1/conversation", params={"conversation_id": conv["conversation_id"]}, headers=headers).json()
convdetail

{'conversation_id': '6c23239b-b5b3-4a7f-b80b-513dab06f643',
 'user_id': '3ede53c1-fb18-4bb8-8897-f9f819ef73ff',
 'created': '2024-05-22T16:12:25.531558',
 'title': '',
 'messages': [{'role': 'user        ',
   'content': 'What is the stock price for Nvidia?'},
  {'role': 'assistant   ',
   'content': 'The current stock price for Nvidia (NVDA) is displayed in the interactive chart above. Here is the interactive chart.\n<iframe style="width: 100%; height: 425px" srcdoc=\'<!-- TradingView Widget BEGIN -->\n<html style="width: 100%; height: 100%; overflow: hidden"><body style="width: 100%; height: 100%; margin: 0; overflow: hidden">\n<style>.tradingview-widget-container .tradingview-widget-copyright {display: none;}</style>\n<div class="tradingview-widget-container" style="height:100%;width:100%">\n  <div class="tradingview-widget-container__widget" style="height:calc(100% - 10px);width:100%"></div>\n  <div class="tradingview-widget-copyright"><a href="https://www.tradingview.com/" rel="noopener nofollow" target="_blank"><span class="blue-text">Track all markets on TradingView</span></a></div>\n  <script type="text/javascript" src="https://s3.tradingview.com/external-embedding/embed-widget-advanced-chart.js" async>\n  {\n  "autosize": true,\n  "symbol": "NVDA",\n  "interval": "H",\n  "timezone": "Etc/UTC",\n  "theme": "dark",\n  "style": "1",\n  "locale": "en",\n  "enable_publishing": false,\n  "allow_symbol_change": true,\n  "calendar": false,\n  "support_host": ""\n}\n  </script>\n</div>\n</body></html>\n<!-- TradingView Widget END -->\'></iframe>'}]}

# Check the plan was updated with usage

userplan = requests.get(base_url + "/v1/user/plan", headers=headers).json()
userplan

{'user_id': '3ede53c1-fb18-4bb8-8897-f9f819ef73ff',
 'email': '',
 'plan_type': 'free',
 'plan_limit': 5,
 'plan_usage': 1,
 'renew_at': '2024-05-23T00:00:00Z'}

# Now continue the conversation

history = convdetail["messages"]

data = {
    "conversation_id": conv["conversation_id"],
    "user_id": conv["user_id"],
    "messages": history + [{"role": "user", "content": "What is happening in the market today related to Nvidia?"}]
}
chat = requests.post(base_url + "/v1/agent/completion", json=data, headers=headers).json()
chat

{'conversation_id': '6c23239b-b5b3-4a7f-b80b-513dab06f643',
 'user_id': '3ede53c1-fb18-4bb8-8897-f9f819ef73ff',
 'created': '2024-05-22 16:41:55.742972',
 'message': {'role': 'assistant',
  'content': "On May 22, 2024, Nvidia (NVDA) stock price closed at $949.47. This information indicates the stock's performance on that specific day."}}

# After several calls the free quota limit is reached

userplan = requests.get(base_url + "/v1/user/plan", headers=headers).json()
userplan

{'user_id': '3ede53c1-fb18-4bb8-8897-f9f819ef73ff',
 'email': '',
 'plan_type': 'free',
 'plan_limit': 5,
 'plan_usage': 5,
 'renew_at': '2024-05-23T00:00:00Z'}

# The next call will raise an exception since the user reached the limit

data = {
    "conversation_id": conv["conversation_id"],
    "user_id": conv["user_id"],
    "messages": history + [{"role": "user", "content": "What is happening in the market today related to Apple?"}]
}
res = requests.post(base_url + "/v1/agent/completion", json=data, headers=headers)

res.status_code

403

res.json()

{'detail': 'Quota exceeded. No more calls are allowed before limit reset'}

# If the user goes to the upgrade this endpoint will generate the stripe session links

slinks = requests.get(base_url + "/v1/checkout-session", headers=headers).json()
slinks

{'pro': 'https://checkout.stripe.com/c/pay/cs_test_a10vZDsY8Lz4ZY0G4usbRNzqGh7xXdMGrmaT9lmPaHbbbRbJlyYSGNvo87#fid2cGd2ZndsdXFsamtQa2x0cGBrYHZ2QGtkZ2lgYSc%2FY2RpdmApJ2R1bE5gfCc%2FJ3VuWnFgdnFaMDRKdUZibE5Ib0R2XTc9XV1mNVdSZm1sU3J8MzZPfHNgVGNWSmd0SnFJNFZCf2w1b11mQjBxMVFOTnZVYFxnamxAUWFUT399aElsXWt8dT1MNWxsPGw0R0s1NTJENURgMkltJyknY3dqaFZgd3Ngdyc%2FcXdwYCknaWR8anBxUXx1YCc%2FJ3Zsa2JpYFpscWBoJyknYGtkZ2lgVWlkZmBtamlhYHd2Jz9xd3BgeCUl',
 'premium': 'https://checkout.stripe.com/c/pay/cs_test_a1PoHh7NJmbMl3o2eLR8Z6kgHSXQSHhX4YVgrA9BfyRHKIA0j5L9eOmssM#fid2cGd2ZndsdXFsamtQa2x0cGBrYHZ2QGtkZ2lgYSc%2FY2RpdmApJ2R1bE5gfCc%2FJ3VuWnFgdnFaMDRKdUZibE5Ib0R2XTc9XV1mNVdSZm1sU3J8MzZPfHNgVGNWSmd0SnFJNFZCf2w1b11mQjBxMVFOTnZVYFxnamxAUWFUT399aElsXWt8dT1MNWxsPGw0R0s1NTJENURgMkltJyknY3dqaFZgd3Ngdyc%2FcXdwYCknaWR8anBxUXx1YCc%2FJ3Zsa2JpYFpscWBoJyknYGtkZ2lgVWlkZmBtamlhYHd2Jz9xd3BgeCUl',
 'lifetime': 'https://checkout.stripe.com/c/pay/cs_test_a1FBl5umpATnfrAtMJJd534nHyfIu9IOL3TfGj5X65jWvQtf02XLTwDrEz#fidkdWxOYHwnPyd1blpxYHZxWjA0SnVGYmxOSG9Edl03PV1dZjVXUmZtbFNyfDM2T3xzYFRjVkpndEpxSTRWQn9sNW9dZkIwcTFRTk52VWBcZ2psQFFhVE9%2FfWhJbF1rfHU9TDVsbDxsNEdLNTUyRDVEYDJJbScpJ2N3amhWYHdzYHcnP3F3cGApJ2lkfGpwcVF8dWAnPyd2bGtiaWBabHFgaCcpJ2BrZGdpYFVpZGZgbWppYWB3dic%2FcXdwYHgl'}

# Following the first link (Pro) and then execute the payment and got the confirmation page. Now let's check the user plan.

userplan = requests.get(base_url + "/v1/user/plan", headers=headers).json()
userplan

{'user_id': '3ede53c1-fb18-4bb8-8897-f9f819ef73ff',
 'email': None,
 'plan_type': 'pro',
 'plan_limit': 50,
 'plan_usage': 5,
 'renew_at': '2024-05-23T00:00:00Z'}


