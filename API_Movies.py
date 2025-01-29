from API_Key import KEY
import requests


def api_request_data(title: str):
    """
    Fetches movie data from the OMDB API based on the provided movie title. (https://www.omdbapi.com/)

    Parameters:
        title (str): The title of the movie to search for.

    Returns:
        tuple: A tuple containing:
            - title (str): The movie's title.
            - year (str): The movie's release year.
            - rating (str): The movie's rating, or a default message if not available.
            - poster_url (str): The URL of the movie's poster.
        False: If there was an issue with the request, missing data, or invalid response, the function returns `False`.

    Exceptions:
        requests.exceptions.RequestException: Raised if there is a network-related error.
        KeyError: Raised if an expected key is missing in the API response.
    """
    try:
        title_request = "&t=" + "+".join(title.split(" "))
        api_response = requests.get(f"http://www.omdbapi.com/?apikey={KEY}{title_request}")
        if api_response.status_code == 200:
            movie_infos = api_response.json()
            if "Title" in movie_infos and "Year" in movie_infos and "Poster" in movie_infos:
                title = movie_infos["Title"]
                year = movie_infos["Year"]
                rating = movie_infos.get("Ratings", False)
                rating = rating[0]["Value"] if rating else None
                poster_url = movie_infos["Poster"]
                director = movie_infos["Director"] if "Director" in movie_infos else "No director available"
                return title, year, rating, poster_url, director
            else:
                print("Error: Missing expected data in the response")
                return False
        else:
            print(f"Error: Received a non-OK status code: {api_response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        return f"Network error occurred: {e}"
    except ValueError as e:
        return f"Error translation json response: {e}"
    except KeyError as e:
        return f"Key error, key nicht vorhanden: Missing {e} in the response"





