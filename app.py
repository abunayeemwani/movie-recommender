import streamlit as st
import pickle
import pandas as pd
import requests

similarity = pickle.load(open('./similarity.pkl', 'rb'))
movies_dict = pickle.load(open('./movies.pkl', 'rb'))
movies_df = pd.DataFrame(movies_dict)

def fetch_data(id):
    # url = f'https://api.themoviedb.org/3/movie/{id}?api_key=0cc7f1cc7477b88d1d8560dc5241e4c6&language=en-US'
    url = f'https://api.themoviedb.org/3/movie/{id}?language=en-US'
    
    proxies = {
        "http": "http://23.137.248.197:8888",
    }
    headers = {
        'Authorization':'Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIwY2M3ZjFjYzc0NzdiODhkMWQ4NTYwZGM1MjQxZTRjNiIsIm5iZiI6MTcyMjMzMTIxOS43OTY0MDUsInN1YiI6IjY2YTg5ZjFkODY0YTFlYTc2OThjYzc3ZCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.rt3xcviktBbsOa4HubtDG52imJUTtH_dFqF64oavldo',
        'accept': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()
        data = response.json()
        
        return {
            "title": data['title'],
            "overview": data['overview'],
            "poster_path": "https://image.tmdb.org/t/p/original" + data['poster_path'],
            "release_date": data['release_date'],
            "languages": [item['name'] for item in data['spoken_languages']],
            "genres": [item['name'] for item in data['genres']],
        }
        
    except requests.exceptions.ConnectionError as e:
        print(f"Error: Unable to connect to the API. Details: {e}")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP error occurred: {e}")
    except requests.exceptions.Timeout as e:
        print(f"Request timed out: {e}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

def recommend(movie):
    movie_index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommend_movies = []
    for i in movies_list:
        recommend_movies.append(fetch_data(movies_df.iloc[i[0]]['movie_id']))
        # recommend_movies.append(movies_df.iloc[i[0]]['title'])
        
    return recommend_movies

st.title('Movie Recommender System')

selected_movie = st.selectbox(
    "Please select the movie",
    movies_df['title'].values,
)

if st.button('Recommend'):
    movies = recommend(selected_movie)
    
    col1, col2, col3 ,col4, col5 = st.columns(5)

    with col1:
        st.image(movies[0]['poster_path'])
        st.markdown(movies[0]['title'])

    with col2:
        st.image(movies[1]['poster_path'])
        st.markdown(movies[1]['title'])

    with col3:
        st.image(movies[2]['poster_path'])
        st.markdown(movies[2]['title'])
        
    with col4:
        st.image(movies[3]['poster_path'])
        st.markdown(movies[3]['title'])
        
    with col5:
        st.image(movies[4]['poster_path'])
        st.markdown(movies[4]['title'])
