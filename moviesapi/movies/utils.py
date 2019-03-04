import requests

from django.conf import settings


def load_movie(title):
    url = "http://www.omdbapi.com/?t={}&apikey={}".format(
        title, settings.OMDBAPI_KEY)
    r = requests.get(url)
    if r.status_code == 200:
        response = r.json()
        if response['Response'] == 'True':
            return response
        else:
            raise LookupError("Movie not found.")
    else:
        raise LookupError("Wrong status code received.")


if __name__ == "__main__":
    settings.configure()
    print(load_movie("Shrek"))
    print(load_movie("I am sure that movie with this title does not exist"))