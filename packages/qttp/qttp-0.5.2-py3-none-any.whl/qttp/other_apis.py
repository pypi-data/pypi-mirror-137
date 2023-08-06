from newsapi import NewsApiClient

my_api_key = 'ffece0e11b3c460183b53610914a4c7e'
newsapi = NewsApiClient(api_key=my_api_key)
data = newsapi.get_everything(q='가상화폐', page_size=20,)
print(data.keys())
