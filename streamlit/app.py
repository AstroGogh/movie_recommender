import pandas as pd
import streamlit as st
import scipy.sparse as sparse

import pathlib
import sys

sys.path.append(str(pathlib.Path().absolute().parent / 'modules'))
from recommendations import get_recommendations

# Your Streamlit code goes here


def recommendations(title):
    df = pd.read_csv('../data/movie.csv')
    sim_mat = sparse.load_npz('../data/npz/sim_mat.npz')

    # Get the recommendations
    title, df = get_recommendations(title, df, sim_mat)
    return title, df

#=== HEAD SECTION ===
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
                    f"""<p style="background-color: #F2F2F2; border-radius: 10px; padding: 10px; width: 100%;">
                        {movie[1]["title"]}</p>""",
                    unsafe_allow_html=True
                )
    else:
        st.write("No recommendations found.")

