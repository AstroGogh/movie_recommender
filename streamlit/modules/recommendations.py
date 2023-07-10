from fuzzywuzzy import fuzz
import numpy as np
import pandas as pd

# Get Title Similarity Score
def title_matching_score(title_a, title_b):
    return fuzz.ratio(title_a, title_b)

def get_title_from_index(index, df):
    return df[df.index == index]['title'].values[0]

def get_index_from_title(title, df):
    return df[df.title == title].index.values[0]

# Get Closest Title
def get_closest_title(title, df):
    scores = list(enumerate(df['title'].apply(lambda x: title_matching_score(title, x))))
    scores = sorted(scores, key=lambda x: x[1], reverse=True)
    
    #get the title of the closest match
    closest_title = get_title_from_index(scores[0][0], df)
    score = scores[0][1]

    return closest_title, score

def get_recommendations(title, df, sim_mat):
    closest_title, distance_score = get_closest_title(title, df)

    if distance_score != 100:
        print("Did you mean " + closest_title + "?")

    title_index = get_index_from_title(closest_title, df)
    movies_similar = sim_mat[title_index].toarray().flatten()

    #Get top 10 similar movies recommendation
    movie_indices = np.argsort(-movies_similar)[1: 11]


    df_recommendations = df.iloc[movie_indices]
    return closest_title, df_recommendations