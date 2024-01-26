# imports
import pandas as pd
import pickle
from src.utils.embeddings_utils import (
    get_embedding,
    distances_from_embeddings,
    indices_of_nearest_neighbors_from_distances,
)

# constants
EMBEDDING_MODEL = "text-embedding-ada-002"

embedding_cache_path = "src/cache/recommendations_embeddings_cache.pkl"

try:
    embedding_cache = pd.read_pickle(embedding_cache_path)
except FileNotFoundError:
    embedding_cache = {}
with open(embedding_cache_path, "wb") as embedding_cache_file:
    pickle.dump(embedding_cache, embedding_cache_file)

def embedding_from_string(
    string: str,
    model: str = EMBEDDING_MODEL,
    embedding_cache=embedding_cache
) -> list:
    """Return embedding of given string, using a cache to avoid recomputing."""
    if (string, model) not in embedding_cache.keys():
        embedding_cache[(string, model)] = get_embedding(string, model)
        with open(embedding_cache_path, "wb") as embedding_cache_file:
            pickle.dump(embedding_cache, embedding_cache_file)
    return embedding_cache[(string, model)]


test = ['Natural Language: it never happens that the sensor retrieves data or the manager handles requests or the elevator falls', 'Natural Language: it will not happen that tRdcOEMYfkvOyC', 'Natural Language: never, brDJByV or yQoNUAYsCjQo or bBiiqLBJe', 'Natural Language: it never happens that either a car stops, the manager collect claims or a train has been launched', 'Natural Language: at any time either the brake is released, the train has been launched or a train is crossing', 'Natural Language: eternally, VYfRmSkzKfgu and together VARATe and eQazD', 'Natural Language: every time either the sensor captures data or the train is crossing then under no condition both the bar has to be repaired and the engine stops', 'Natural Language: every time both the escalator is blocked and the semaphore is yellow then absolutely never, the car stops and a constructor instantiate objects', 'Natural Language: at no time BfIzuqN after ZzxhFAzuhkovM', 'Natural Language: always a house is open or the manager collect claims implies that at no time either the elevator is blocked or an elevator falls', 'Natural Language: after both the motorbike falls down and the engine starts, it never happens that both the semaphore is red and the bar is up', 'Natural Language: after xVwrrMwqBGrmTzj, in any case VdSBhstrx', 'Natural Language: each time the escalator moves then whenever a table is old then finally, the train derails', 'Natural Language: _eFfsGdhZRpmkp and, as a consequence, if IiFaHJNZsO then finally, fYwil', 'Natural Language: the engine starts implies that at a certain moment a motorbike has stopped after the motorbike catches fire', 'Natural Language: the car enters involves that every time the house is built then at some point the engine starts', 'Natural Language: when the motorbike has stopped then as the elevator is open, at a certain moment a train derails afterwards', 'Natural Language: iJjNRSfjPsy involves that always when FxBbOuFiZWVd then finally, WSwTZ', 'Natural Language: when NnoqrGoJ then as xphINIJCDo, it is going to happen that pfYKhFn afterwards', 'Natural Language: each time the elevator falls then if a house is built then in the future a car enters', 'Natural Language: the engine starts and, as a consequence, if the elevator rises then sooner or later the bar has to be repaired', 'Natural Language: when the table is brown then always when a semaphore is red then it is going to happen that a car enters afterwards', 'Natural Language: each time the train stops then every time an elevator is blocked then sooner or later the table is old', 'Natural Language: a house is built involves that as a semaphore is yellow, in the future the constructor instantiate objects', 'Natural Language: eventually, the bar has to be repaired or the engine breaks after either the bar is down or the manager collect claims', 'Natural Language: as qnECRoCbqy, finally, BPYMUeFe', 'Natural Language: always when a motorbike has stopped and a constructor creates instances then sooner or later both the bar is up and the manager collect claims', 'Natural Language: every time the brake is released or a house collapses then it will happen that the escalator speeds up and the bar is up', 'Natural Language: if either hdBES_ or MNqG_GqR then at a certain moment Hjelv and d_WfjcacGugs_', 'Natural Language: if both the constructor instantiate objects and a semaphore is red then finally, a semaphore is yellow and the table has been moved', 'Natural Language: after a motorbike has stopped and the train is crossing, at some point in time the elevator falls or a house is open', 'Natural Language: at a certain moment either an elevator is open or the semaphore is green after a table has been moved and the engine breaks', 'Natural Language: sooner or later the escalator speeds up and a motorbike falls down after either the motorbike has stopped or a house is built', 'Natural Language: eventually, the bar has to be repaired or the engine breaks after either the bar is down or the manager collect claims', 'Natural Language: as either aqOxNFSwJ or deJMdBHk, eventually, both ySKbfcmTFFywFvw and xhoiWeiv', 'Natural Language: as aRxslSoeWOjQ or vilJTegYsXbeR, at some point in time SoLGzNlk', 'Natural Language: if TVpyLL then it is going to happen that zwPpFufrO or XAhdxWWgoxuqaf', 'Natural Language: it never happens that a semaphore is red and the bar is up after both the bar is up and the car starts', 'Natural Language: if ISwGkuvxY and cBWLoGwjXZjH then it will not happen that k_SEyHiY', 'Natural Language: if a table is brown or the escalator speeds up then at any time either a semaphore is yellow or the engine breaks', 'Natural Language: every time either the escalator speeds up or a sensor gathers information then in any case the table has been moved and a motorbike has stopped', 'Natural Language: every time the train stops and the sensor gathers information after either the car starts or the bar is closing', 'Natural Language: first, at some point in time both a train stops and the brake is pressed, and then, at a certain moment a train has arrived', 'Natural Language: it is going to happen that kYGWJw and, at some point DzeUQwLc_ODQUm afterwards', 'Natural Language: finally, a car enters or the bar has to be repaired and, in the future either the bar has to be repaired or a table is old afterwards', 'Natural Language: eventually, a table is old or the constructor creates instances and, it is going to happen that either the engine stops or an elevator is open afterwards', 'Natural Language: in the future a train has been launched and the escalator is blocked and, it will happen that the train is crossing or a manager collect claims afterwards', 'Natural Language: at a certain moment VxJKDCCePtAstWC and, it is going to happen that both dObFap and mjEpqPJZphsuau afterwards', 'Natural Language: in the future AJUdpDtzfEUVl or FskjzkFKm_KZPl and, sooner or later ESlKDJiMc_mWeun and BhKPGbOypRdr afterwards', 'Natural Language: first, at some point in time a semaphore is red and an elevator falls, and then, finally, both a table is brown and a house is built', 'Natural Language: first, finally, _TSoAFnLFFKH, and then, at some point JcPDkuUdwgfrk', 'Natural Language: at a certain moment either a train derails or a house collapses and, sooner or later both the elevator is blocked and the train derails afterwards', 'Natural Language: each time the escalator moves then whenever a table is old then finally, the train derails', 'Natural Language: _eFfsGdhZRpmkp and, as a consequence, if IiFaHJNZsO then finally, fYwil', 'Natural Language: the engine starts implies that at a certain moment a motorbike has stopped after the motorbike catches fire', 'Natural Language: the car enters involves that every time the house is built then at some point the engine starts', 'Natural Language: when the motorbike has stopped then as the elevator is open, at a certain moment a train derails afterwards', 'Natural Language: iJjNRSfjPsy involves that always when FxBbOuFiZWVd then finally, WSwTZ', 'Natural Language: when NnoqrGoJ then as xphINIJCDo, it is going to happen that pfYKhFn afterwards', 'Natural Language: each time the elevator falls then if a house is built then in the future a car enters', 'Natural Language: the engine starts and, as a consequence, if the elevator rises then sooner or later the bar has to be repaired', 'Natural Language: when the table is brown then always when a semaphore is red then it is going to happen that a car enters afterwards', 'Natural Language: a train stops and, as a consequence, whenever a table has been moved then eventually, the elevator is blocked']


def get_recommendations_from_strings(
    nl_string: str,
    strings: list[str],
    k_nearest_neighbors: int = 10,
    model=EMBEDDING_MODEL,
) -> list[int]:
    """Print out the k nearest neighbors of a given string."""
    # get embeddings for all strings

    embeddings = [embedding_from_string(string, model=model) for string in strings]
    # get the embedding of the source string
    query_embedding = embedding_from_string(nl_string, model=model)
    # get distances between the source embedding and other embeddings (function from utils.embeddings_utils.py)
    distances = distances_from_embeddings(query_embedding, embeddings, distance_metric="cosine")
    # get indices of nearest neighbors (function from utils.utils.embeddings_utils.py)
    indices_of_nearest_neighbors = indices_of_nearest_neighbors_from_distances(distances).tolist()
    # print out its k nearest neighbors
    if len(indices_of_nearest_neighbors) >= k_nearest_neighbors:
        result = indices_of_nearest_neighbors[:k_nearest_neighbors]
    else:
        result = indices_of_nearest_neighbors
    return result

    



