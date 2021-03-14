import pathlib

import streamlit as st
import pandas as pd

COLUMNS_TO_DISPLAY = [
    "Title",
    "year",
    "average",
    "player_count_min",
    "player_count_max",
    "player_count_best",
    "playing_time",
]

COLUMNS_TO_DISPLAY_NAME = {
    "Title": "Name",
    "year": "Erscheinungsjahr",
    "average": "BGG-Rating",
    "player_count_best": "Beste Spieleranzahl",
    "playing_time": "Spielzeit",
    "player_count_min": "Min. Spieler",
    "player_count_max": "Max. Spieler",
}

datapath = pathlib.Path("./data/")
csv_file = "inventory_bgg.csv"

df = pd.read_csv(datapath / csv_file, sep=";")
df = df.drop_duplicates()

player_count = st.number_input(
    label="Spieleranzahl",
    min_value=2,
    max_value=99,
    step=1,
)

player_count_best = st.selectbox(
    label="Beste Spieleranzahl",
    options=sorted(
        df["player_count_best"].unique(),
        key=lambda x: int(x.split("+")[0])
    ),
)

max_playing_time = st.number_input(
    label="Maximale Spielzeit (Minuten)",
    min_value=5,
    max_value=1440,
    step=10,
    value=60
)

df_filtered = df.query(
    f"{player_count} >= player_count_min & "
    f"{player_count} <= player_count_max & "
    f"'{player_count_best}' == player_count_best &"
    f"playing_time <= {max_playing_time}  "
)

st.dataframe(
    df_filtered[COLUMNS_TO_DISPLAY].rename(
        columns=COLUMNS_TO_DISPLAY_NAME
    )
)

