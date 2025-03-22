# matching.py

def match_events(data_df, reference_df, column='year', tolerance=1):
    """
    Match years from data_df with reference_df based on a given tolerance window.
    Returns a boolean Series indicating matches.
    """
    match_years = set(reference_df[column])
    return data_df[column].apply(lambda y: any(abs(y - ry) <= tolerance for ry in match_years if pd.notnull(ry)))
