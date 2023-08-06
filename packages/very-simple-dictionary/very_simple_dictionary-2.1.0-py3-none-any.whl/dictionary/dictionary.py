import requests


def getDefinition(languageCode: str, word: str) -> str:
    """Returns the first definition of the given word in the given language.
    Returns None if the word does not exist.
    """
    url = f"https://api.dictionaryapi.dev/api/v2/entries/{languageCode}/{word}"
    response = requests.get(url, timeout=5)
    if response.status_code == 404:
        return None

    responseJson = response.json()
    return responseJson[0]["meanings"][0]["definitions"][0]["definition"]
