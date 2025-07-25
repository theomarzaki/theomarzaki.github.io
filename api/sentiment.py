from pysenticrypt import SentiCryptAPI
import pandas as pd


def fetchSentiment():

    api = SentiCryptAPI()
    sent_data = api.get_all_data()

    # Convert to DataFrame
    sent_df = pd.DataFrame(sent_data)
    sent_df['date'] = pd.to_datetime(sent_df['date'])
    sent_df.set_index('date', inplace=True)

    # Optional: just keep the 'mean' score
    sent_df = sent_df[['mean']]
    sent_df.rename(columns={'mean': 'sentiment'}, inplace=True)

    return sent_df
