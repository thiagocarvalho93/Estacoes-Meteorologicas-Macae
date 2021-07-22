import requests
import scrape
import pandas as pd
supabase_url = 'https://knuchygpvoaktotmwnxi.supabase.co/rest/v1'
api_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJyb2xlIjoic2VydmljZV9yb2xlIiwiaWF0IjoxNjI2ODkyNjg0LCJleHAiOjE5NDI0Njg2ODR9.fYz_ZGOQwHfcUkvS3gLNx7F1WLrQ04PyMwYKtlx4rSc'

supabase_headers = {
    'apikey': api_key,
    'Authorization': 'Bearer ' + api_key
}


response = requests.get(f'{supabase_url}/Station', headers = supabase_headers)
lista1 = response.json()
api_df = pd.DataFrame(lista1)
if __name__ == '__main__':
    print(api_df)
    #dataframe = pd.read_json(response.json()[0])



    #response = requests.post(f'{supabase_url}/Station?id=IMACA7', headers = supabase_headers, json = scrape.json)
    #print(response.text)







#'''
#curl -X POST 'https://knuchygpvoaktotmwnxi.supabase.co/rest/v1/Station' \
#-H "apikey: SUPABASE_KEY" \
#-H "Authorization: Bearer SUPABASE_KEY" \
#-H "Content-Type: application/json" \
#-H "Prefer: return=representation" \
#-d '{ "some_column": "someValue", "other_column": "otherValue" }'
