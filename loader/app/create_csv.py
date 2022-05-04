"""Create CSV for the loader from an Excel file created from manual data entry."""

import os
from pathlib import Path

import pandas as pd


def get_data_dir():
    data_dir = os.environ.get("DATA_DIR")
    if data_dir:
        data_dir = Path(data_dir).resolve()
    else:
        data_dir = Path(__file__).parent.resolve() / ".." / "data"
    return data_dir


def cleanup_title(title: str) -> str:
    """Replace newline characters with spaces and convert ALL UPPERCASE TITLES to Title Case.

    Args:
        title (str)

    Returns:
        str
    """
    if not isinstance(title, str):
        return title

    title_new = title.replace("\n", " ")

    if title.upper() == title:
        title_new = title_new.title()

    return title_new


def process_documents_df(df: pd.DataFrame) -> pd.DataFrame:
    """Clean up titles and replace non English language titles with their translations.

    Args:
        df (pd.DataFrame)

    Returns:
        pd.DataFrame
    """
    df_out = df.copy()

    df_out[["Title", "_translated_title"]] = df_out[
        ["Title", "_translated_title"]
    ].applymap(cleanup_title)

    # replace original language titles with English
    for idx, row in df_out.iterrows():
        if row["Language"] != "English":
            df_out.loc[idx, "Title"] = row["_translated_title"]

    return df_out


def merge_document_and_action_dfs(df_document_processed, df_actions) -> pd.DataFrame:
    """Merge the document and action dataframes."""
    columns_to_merge = [
        "Type",
        "Frameworks",
        "Responses",
        "Instruments",
        "Natural Hazards",
        "Keywords",
        "Sectors",
        "Events",
    ]

    return pd.merge(
        left=df_document_processed, right=df_actions[["Id"] + columns_to_merge], on="Id"
    )


def drop_missing_rows_from_merged_df(df_merged: pd.DataFrame) -> pd.DataFrame:
    """Drop rows without a title."""

    cols_required_values = [
        "Title",
    ]

    return df_merged.dropna(subset=cols_required_values)


if __name__ == "__main__":
    DATA_DIR = get_data_dir()
    DATA_PATH = DATA_DIR / "Master sheet completed.xlsx"

    # From Juan loader
    # TODO: can we import this from the loader code?
    csv_column_map = {
        "Id": "policy_id",  # for grouping related documents
        "Title": "document_name",
        "Geography ISO": "country_code",
        "Documents": "document_url",  # column is plural, but it will be only one document URL
        "Category": "policy_category",
        # metadata
        "Events": "events",
        "Sectors": "sectors",
        "Instruments": "instruments",
        "Frameworks": "frameworks",
        "Responses": "responses",
        "Natural Hazards": "hazards",
        "Document Type": "document_type",
        "Year": "document_year",
        "Language": "document_language",
        "Keywords": "keywords",
    }

    person_names = [
        "Callie",
        "Danny",
        "Ingemar",
        "Joel",
        "Juan",
        "Kalyan",
        "Marcus",
        "Michal",
        "Paula",
        "Stef",
    ]

    def process_data(df_documents, df_actions) -> pd.DataFrame:
        # Rows without a value for these columns will be dropped
        columns_required_values = ["Title"]

        df_documents = df_documents.dropna(subset=columns_required_values)
        df_documents = process_documents_df(df_documents)
        df_merged = merge_document_and_action_dfs(df_documents, df_actions)
        df_merged = df_merged.rename(columns={"Type": "Category"})

        # 'Int64' is nullable int type, as some rows have no 'Year' value
        df_merged.loc[:, ["Year", "Id"]] = df_merged.loc[:, ["Year", "Id"]].astype(
            "Int64"
        )

        return df_merged[csv_column_map.keys()]

    data_list = []

    for person in person_names:
        print(f"Processing {person}")

        df_documents = pd.read_excel(str(DATA_PATH), sheet_name=f"{person} documents")
        df_actions = pd.read_excel(str(DATA_PATH), sheet_name=f"{person} actions")

        data_list.append(process_data(df_documents, df_actions))

    data_final = pd.concat(data_list, axis=0, ignore_index=True)
    data_final.to_csv(str(DATA_DIR / "loader_data.csv"), index=False)
