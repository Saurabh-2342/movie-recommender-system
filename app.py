import pickle
import streamlit as st
import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry


# Function to fetch movie details including poster, IMDb ID, and genres with retry logic
def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjN2RkMzYzYzQwOWYyOWU3ZTg4YjMzNWM5ZGJlN2VmNiIsIm5iZiI6MTczMDY0NDAyNC4wODc5NjIyLCJzdWIiOiI2NzI1Y2M5ZmUzNWQ1YTUzZmU3MmM4ZDIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.811opgp7LLNAyzdStj4K9CK8veS8wQE83W5c8ecVsvk"
    }

    session = requests.Session()
    retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
    session.mount('https://', HTTPAdapter(max_retries=retries))

    try:
        response = session.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        poster_path = data.get('poster_path')
        imdb_id = data.get('imdb_id')
        genres = [genre['name'] for genre in data.get('genres', [])]

        if poster_path:
            poster_url = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            poster_url = None

        return {
            'poster_url': poster_url,
            'imdb_id': imdb_id,
            'genres': genres
        }

    except requests.exceptions.RequestException as e:
        print(f"Error fetching movie details: {e}")
        return {'poster_url': None, 'imdb_id': None, 'genres': []}


# Function to fetch a trailer link for a movie
def fetch_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?language=en-US"
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJjN2RkMzYzYzQwOWYyOWU3ZTg4YjMzNWM5ZGJlN2VmNiIsIm5iZiI6MTczMDY0NDAyNC4wODc5NjIyLCJzdWIiOiI2NzI1Y2M5ZmUzNWQ1YTUzZmU3MmM4ZDIiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.811opgp7LLNAyzdStj4K9CK8veS8wQE83W5c8ecVsvk"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Debug print for response structure
        print("Trailer data:", data)

        for video in data.get('results', []):
            if video.get('type') == 'Trailer' and video.get('site') == 'YouTube':
                return f"https://www.youtube.com/watch?v={video.get('key')}"

        # Print if no trailer was found
        print("No trailer found for movie ID:", movie_id)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching trailer: {e}")

    return None


# Recommendation function
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_links = []
    recommended_movie_genres = []
    recommended_movie_trailers = []

    for i in distances[1:5]:
        movie_id = movies.iloc[i[0]].movie_id
        details = fetch_movie_details(movie_id)
        recommended_movie_posters.append(details['poster_url'])
        recommended_movie_links.append(
            f"https://www.imdb.com/title/{details['imdb_id']}" if details['imdb_id'] else None)
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_genres.append(", ".join(details['genres']))
        recommended_movie_trailers.append(fetch_trailer(movie_id))

    return recommended_movie_names, recommended_movie_posters, recommended_movie_links, recommended_movie_genres, recommended_movie_trailers


# Streamlit app code
st.header('Movie Recommender System')

# Load the movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown", movie_list)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_links, recommended_movie_genres, recommended_movie_trailers = recommend(
        selected_movie)

    cols = st.columns(4)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.caption(recommended_movie_genres[idx])
            if recommended_movie_posters[idx]:
                if recommended_movie_links[idx]:
                    st.markdown(
                        f'<a href="{recommended_movie_links[idx]}" target="_blank"><img src="{recommended_movie_posters[idx]}" width="100%"></a>',
                        unsafe_allow_html=True)
                else:
                    st.image(recommended_movie_posters[idx])
            else:
                st.image("path/to/fallback_image.jpg")  # Replace with a placeholder image path
                st.text("Poster not available")

            if recommended_movie_trailers[idx]:
                st.markdown(f"[Watch Trailer]({recommended_movie_trailers[idx]})", unsafe_allow_html=True)
            else:
                st.text("Trailer not available")
