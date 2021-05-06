
def search(word):
    import requests
    url = "https://api.dictionaryapi.dev/api/v2/entries/en_US/"
    response = requests.request("GET", url+word)
    response = response.json()
    response = response[0]
    definition = response['meanings'][0]['definitions'][0]['definition']
    example = response['meanings'][0]['definitions'][0]['example']
    return definition,example