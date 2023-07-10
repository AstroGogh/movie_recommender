import os
import pandas as pd
import streamlit as st
import scipy.sparse as sparse

from PIL import Image
from modules.recommendations import get_recommendations

# Your Streamlit code goes here


def recommendations(title):
    df = pd.read_csv('data/movie.csv')

    file_path = os.path.join(os.path.dirname(__file__), 'sim_mat.npz')
    sim_mat = sparse.load_npz(file_path)

    # Get the recommendations
    title, df = get_recommendations(title, df, sim_mat)
    return title, df

#=== HEAD SECTION ===

fav_path = os.path.join(os.path.dirname(__file__), 'favicon.ico')
fav = Image.open(fav_path)
st.set_page_config(page_title = "Movie Recommender",
                   page_icon=fav)

st.title("Movie Recommender System 🎬")
st.write("""
            This is a simple movie recommendations systems built using **Content-Based Filtering** methodology, 
            **Recommendations** are based on **genre, director, cast, and movie description**.
            """)

st.markdown("""---""")

#=== BODY SECTION ===
title = st.text_input("What is your favourite movie?", "Toy Story")

if st.button("Generate"):
    res = recommendations(title)
    
    if res is not None:
        title, df = res
        st.markdown("""---""")
        st.markdown(f"Here are some recommendations for **{title}**:")
        
        # Display Each Movie Title
        num_columns = 4  # Number of columns to display the movie titles
        num_movies = len(df)
        
        # Create columns for displaying movie titles
        columns = st.columns(num_columns)
        for i, movie in enumerate(df.iterrows()):
            with columns[i % num_columns]:
                st.markdown(
                    f"""<p style="color: #000000; background-color: #FFFFFF; border-radius: 10px; padding: 10px; width: 100%;">
                        {movie[1]["title"]}</p>""",
                    unsafe_allow_html=True
                )
    else:
        st.write("No recommendations found.")

