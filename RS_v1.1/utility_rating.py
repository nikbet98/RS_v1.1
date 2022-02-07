import pandas as pd


# funzione per selezionare solo i film con almeno un tot di recensioni
# ritorna un dataframe con solo i film con abbastanza votazioni
def enough_rated(items, percentage):
    m = items['vote_count'].quantile(percentage)
    filt = (items['vote_count'] >= m)
    return items[filt]
# volendo si può fare anche
# q_movie = movie_df.copy().loc[movie_df['vote_count'] >= m]
# questo perchè a loc puoi passare anche un array di true/false, che è quello che facciamo praticamente nelle sue []


# funzione per contare quante recensioni ha un film
# ritorna il dataframe in cui è stata aggiunta la colonna del numero di votazioni totali
def count_rating(items, rating):
    counted = rating['itemId'].value_counts()
    counted.sort_index(inplace=True)
    items['vote_count'] = counted.reset_index(drop=True)
    return items


# funzione per calcolare il voto medio dei film
# ritorna il dataframe in cui sono stati calcolati anche i voti medi
def average_rating(items, rating):
    avr = []
    for x in items['itemId']:
        movie_filt = (rating['itemId'] == x)
        selected_item = rating[movie_filt]
        avr.append(selected_item['rating'].mean())
    items.reset_index(inplace=True)
    items['vote_avr'] = avr
    items.dropna(inplace=True)
    return items


def min_vote(items, percentile):
    return items['vote_count'].quantile(percentile)


def weighted_rating(v, m, R, C):
    """
    calcola il voto medio pesato
    Args:
    v -> numero di voti per ogni item
    m -> numero minimo di voti che un film deve avere
    R -> voto medio semplice per ogni item (pd.Series)
    C -> voto medio dell'intera collezione di votazioni

    Returns:
    pd.Series
    """
    return ((v / (v + m)) * R) + ((m / (v + m)) * C)
