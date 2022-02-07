import pandas as pd
import utility_rating as ur
import rating_adapter as ra

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.options.mode.chained_assignment = None  # default='warn'


def weighted_rating(v, m, R, C):
    """
    Calculate the weighted rating

    Args:
    v -> average rating for each item (float)
    m -> minimum votes required to be classified as popular (float)
    R -> average rating for the item (pd.Series)
    C -> average rating for the whole dataset (pd.Series)

    Returns:
    pd.Series
    """
    return ((v / (v + m)) * R) + ((m / (v + m)) * C)


# vogliamo caricare il dataset dei film e delle reviews
movies_df = pd.read_csv('..\\input\\movieLens\\movies.csv')
rating_df = pd.read_csv('..\\input\\movieLens\\ratings.csv')

# rendiamo un attimo più generici i dataframe in modo che sia più facile lavorarci
ra.itemIdAdapter(movies_df, 'movieId')
ra.itemIdAdapter(rating_df, 'movieId')


# conto quante recensioni ha ogni film
movies_df = ur.count_rating(movies_df, rating_df)

# minimo numero votazioni
m = ur.min_vote(movies_df, 0.9)
# voto medio in generale
C = rating_df['rating'].mean()
print("il voto medio è: " + str(C))

# threshold per il numero di recensioni
percentage = 0.9
q_movies = ur.enough_rated(movies_df, percentage)  # nuovo dataframe con solo i film che hanno abbastanza recensioni

# calcoliamo il voto medio per ogni q_movie
q_movies = ur.average_rating(q_movies, rating_df)
q_movies.sort_values(by=['vote_avr'], ascending=False, inplace=True)

# calcoliamo il voto pesato
wr = ur.weighted_rating(q_movies['vote_count'], m, q_movies['vote_avr'], C)
q_movies['weighted_rating'] = wr
q_movies.sort_values(by=['weighted_rating'], ascending=False, inplace=True)
print(q_movies)

# salviamo su un nuovo file
q_movies.to_csv('..\\input\\movieLens\\q_movie.csv')
