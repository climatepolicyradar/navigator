"""Create CSV for the loader from an Excel file created from manual data entry."""

import os
from pathlib import Path
from html.parser import HTMLParser
from io import StringIO
import pandas as pd

from app.loaders.loader_cclw_v2.extract.main import csv_column_map
from app.loaders.loader_cclw_v1.extract.main import extract


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


def get_single_doc_actions_xlsx(single_doc_actions_path: Path) -> pd.DataFrame:
    return pd.read_excel(
        str(single_doc_actions_path), sheet_name="COMPLETED combined"
    ).rename(columns={"Type": "Category"})


class MLStripper(HTMLParser):
    """Strips HTML from strings."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.text = StringIO()

    def handle_data(self, d):  # noqa:D102
        self.text.write(d)

    def get_data(self):  # noqa:D102
        return self.text.getvalue()


def strip_tags(html: str) -> str:
    s = MLStripper()
    s.feed(html)
    return s.get_data()


if __name__ == "__main__":
    DATA_DIR = get_data_dir()
    MANUALLY_CREATED_DATA_PATH = DATA_DIR / "Master sheet completed.xlsx"
    SINGLE_DOC_ACTIONS_PATH = DATA_DIR / "Single doc action doc type fixes.xlsx"
    CCLW_V1_CSV = DATA_DIR / "laws_and_policies_16022022.csv"

    single_doc_actions_df = get_single_doc_actions_xlsx(SINGLE_DOC_ACTIONS_PATH)

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

    def process_data(
        df_documents, df_actions, df_cclw_v1_csv_with_single_url
    ) -> pd.DataFrame:
        # Rows without a value for these columns will be dropped
        columns_required_values = ["Title"]

        df_documents = df_documents.dropna(subset=columns_required_values)
        df_documents = process_documents_df(df_documents)
        df_merged = merge_document_and_action_dfs(df_documents, df_actions)
        df_merged = df_merged.rename(columns={"Type": "Category"})

        # 'Int64' is nullable int type, as some rows have no 'Year' value
        df_merged.loc[:, "Year"] = df_merged.loc[:, "Year"].astype("Int64")
        df_merged.loc[:, "Id"] = df_merged.loc[:, "Id"].astype(int)

        docs_and_actions_and_descriptions_from_v1_csv_merged = pd.merge(
            left=df_merged,
            right=df_cclw_v1_csv_with_single_url[["_url", "Description"]],
            on="_url",
        )
        docs_and_actions_and_descriptions_from_v1_csv_merged = (
            docs_and_actions_and_descriptions_from_v1_csv_merged[csv_column_map.keys()]
        )

        return docs_and_actions_and_descriptions_from_v1_csv_merged

    data_list = []

    # explode old CSV on URLs
    df_cclw_v1_csv = extract(CCLW_V1_CSV)
    df_cclw_v1_csv.dropna(subset=["document_list"], inplace=True)
    df_cclw_v1_csv_with_single_url = pd.DataFrame()
    for idx, row in df_cclw_v1_csv.iterrows():
        doc_list = row["document_list"]
        for parts in doc_list.split(";"):
            url = parts.split("|")[1]
            row["_url"] = url
            row["policy_description"] = strip_tags(row["policy_description"])
            df_cclw_v1_csv_with_single_url = pd.concat(
                [df_cclw_v1_csv_with_single_url, row.to_frame().T]
            )

    df_cclw_v1_csv_with_single_url = df_cclw_v1_csv_with_single_url.rename(
        columns={"policy_description": "Description"}
    )

    for person in person_names:
        print(f"Processing {person}")

        df_documents = pd.read_excel(
            str(MANUALLY_CREATED_DATA_PATH), sheet_name=f"{person} documents"
        )
        df_actions = pd.read_excel(
            str(MANUALLY_CREATED_DATA_PATH), sheet_name=f"{person} actions"
        )

        data_list.append(
            process_data(df_documents, df_actions, df_cclw_v1_csv_with_single_url)
        )

    all_manual_data = pd.concat(data_list, axis=0, ignore_index=True)
    print(f"Columns in manual data: {all_manual_data.columns}")
    print(f"Columns in single doc actions df: {single_doc_actions_df.columns}")
    data_final = pd.concat(
        [all_manual_data, single_doc_actions_df], axis=0, ignore_index=True
    )
    data_final.to_csv(str(DATA_DIR / "cclw_new_format_20220503.csv"), index=False)
