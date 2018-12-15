import os
import pickle


def load_db(DB_NAME):
    """
    Loads the database from the path given
    If the path doesnt exists, create a new database
    """
    if os.path.exists(DB_NAME):
        with open(DB_NAME, 'rb') as rfp:
            return pickle.load(rfp)
    else: 
        with open(DB_NAME, "wb") as wfp:
            pickle.dump({}, wfp)
            return {}


def save_db(DB_NAME, data):
    """
    Saves the data into the database
    """
    with open(DB_NAME,'wb') as wfp:
        pickle.dump(data, wfp)

