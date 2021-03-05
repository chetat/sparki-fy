import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *
from datetime import datetime
import numpy as np


def process_song_file(cur, filepath):
    """
    This fuction reads data from provided json file,extracts and transforms
    songs and artists data, and loads them into the artists and songs table

    cur (obj): Database cursor
    filepath (str): File path that contains data json files.
    """
    # open song file
    df = pd.DataFrame(pd.read_json(filepath, lines=True))

    # insert song record
    song_data = list(
        df[["song_id", "title", "artist_id", "year", "duration"]].values[0]
    )
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = list(
        df[
            [
                "artist_id",
                "artist_name",
                "artist_location",
                "artist_latitude",
                "artist_longitude",
            ]
        ].values[0]
    )
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """
    This fuction reads logs data from provided json file, extracts and transforms the data
    by converting timestamp to a valid datetime object, then loads processed
    data into users, songplays, and time tables.

    cur (obj): Database cursor
    filepath (str): File path that contains logs data json files.
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[(df.page == "NextSong")]

    # convert timestamp column to datetime
    t = df[["ts"]].ts.apply(lambda x: datetime.fromtimestamp(x / 1000))

    # insert time data records
    timestamp = t.values.astype(np.int64) // 10 ** 6
    hour, day, week_of_year, month, year, weekday = (
        t.dt.hour,
        t.dt.day,
        t.dt.isocalendar().week,
        t.dt.month,
        t.dt.year,
        t.dt.weekday,
    )

    time_data = [timestamp, hour, day, week_of_year, month, year, weekday]
    column_labels = [
        "timestamp",
        "hour",
        "day",
        "week_of_year",
        "month",
        "year",
        "weekday",
    ]

    data_dict = {
        column_labels[0]: time_data[0],
        column_labels[1]: time_data[1],
        column_labels[2]: time_data[2],
        column_labels[3]: time_data[3],
        column_labels[4]: time_data[4],
        column_labels[5]: time_data[5],
        column_labels[6]: time_data[6],
    }

    time_df = pd.DataFrame(data_dict)

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[["userId", "firstName", "lastName", "gender", "level"]]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()

        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (
            index,
            row.ts,
            row.userId,
            row.level,
            songid,
            artistid,
            row.sessionId,
            row.location,
            row.userAgent,
        )
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Process data provided from logs and songs.
    
    cur (obj):  Database Cursor
    conn (obj): Database connection objection
    filepath (str): Filepath for data files
    func (func): Function that handles data extration and transformation
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root, "*.json"))
        for f in files:
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print("{} files found in {}".format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print("{}/{} files processed.".format(i, num_files))


def main():
    """
    Main function that execute the program
    """
    conn = psycopg2.connect(
        "host=127.0.0.1 dbname=sparkifydb user=wilfred password=weezybaby"
    )
    cur = conn.cursor()

    process_data(cur, conn, filepath="data/song_data", func=process_song_file)
    process_data(cur, conn, filepath="data/log_data", func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
