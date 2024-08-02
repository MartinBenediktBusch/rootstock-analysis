import os
import requests 
import pandas as pd

def load_secret(file_name):
    """
    Function to load a secret like an API key.
    """
    try:
        # Construct the absolute path to the file
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', file_name)
        with open(file_path, 'r') as file:
            secret = file.read().strip()
            return secret
    except Exception as e:
        print(f"Error reading secret file: {e}")
        return None

def query_data(api_key, card_id):
    """
    Function to query data from the Footprint API and return it as a pandas DataFrame.
    :param: api_key (str): The API key to authenticate the request. 
    :param: card_id (int): The card ID to query.
    """
    url = f"https://www.footprint.network/api/v1/dataApi/card/{card_id}/query"

    headers = {
        "accept": "application/json",
        "api-key": api_key,
        "content-type": "application/json"
    }

    try:
        response = requests.post(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        rows = data.get("data", {}).get("rows", [])

        df = pd.DataFrame(rows, columns=["timestamp", "value1", "value2", "value3"])
        return df

    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def save_df_to_csv(df, filename):
    """
    Saves a pandas DataFrame to a CSV file in the 'plots' folder.
    :param: df (pd.DataFrame): The DataFrame to save.
    :param: filename (str): The name of the CSV file (e.g., 'output.csv').
    """
    current_dir = os.getcwd()
    plots_dir = os.path.join(current_dir, 'data')

    # Create the 'plots' folder if it doesn't exist
    os.makedirs(plots_dir, exist_ok=True)

    # Full path to the CSV file and save 
    file_path = os.path.join(plots_dir, filename)
    df.to_csv(file_path, index=False)

    return f"Data saved here: {file_path}"

def load_csv_to_dataframe(file_name):
    """
    Load a CSV file from the 'data' folder into a pandas DataFrame.
    :param: file_name (str): The name of the CSV file to load (including extension).
    """
    file_path = os.path.join('data', file_name)
    
    try:
        df = pd.read_csv(file_path)
        print(f"DataFrame loaded successfully with {df.shape[0]} rows and {df.shape[1]} columns.")
        return df
    except Exception as e:
        print(f"An error occurred while loading the CSV file: {e}")
        return None
