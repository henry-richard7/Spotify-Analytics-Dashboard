import plotly.express as px
import plotly.graph_objects as go
from Modules import milliseconds_duration, decades, artist_meta, embed_spotify
import streamlit as st
from pandas import Categorical, DataFrame


def get(recently_played_df_):

    weekly_df = recently_played_df_
    weekly_df["week_number"] = weekly_df["played_at"].dt.isocalendar().week
    weekly_df["day_type"] = weekly_df["played_at"].apply(
        lambda x: "weekday" if x.weekday() < 5 else "weekend"
    )

    years = weekly_df["played_at"].dt.year.unique().tolist()

    year_value = st.selectbox("Select Year", years)

    yearly_filtered_df = weekly_df[weekly_df["played_at"].dt.year == year_value]
    week_min = int(yearly_filtered_df["week_number"].min())
    week_max = int(yearly_filtered_df["week_number"].max())

    week_value = st.slider(
        "Select Week",
        min_value=week_min,
        max_value=week_max,
        value=week_max,
    )

    recently_played_df = yearly_filtered_df[
        yearly_filtered_df["week_number"] == week_value
    ]

    total_duration = recently_played_df["duration"].sum()
    total_duration = milliseconds_duration.get(total_duration)

    st.title(f"Spotify Report for {year_value} - WEEK {week_value}")
    st.header(f"Total Time Spent: {total_duration}")

    col1, col2 = st.columns(2)
    # Top 10 Songs Calculations ------>
    song_df = recently_played_df.groupby("song")["duration"].sum().reset_index()
    song_df["duration"] = round(song_df["duration"] / 60000, 2)

    song_df = song_df.sort_values("duration", ascending=False).head(10)
    song_fig = (
        px.bar(
            song_df,
            x="song",
            y="duration",
            text="duration",
        )
        .update_layout(
            xaxis_title="Songs",
            yaxis_title="Duration (Minutes)",
            showlegend=False,
            height=600,
            width=600,
        )
        .update_traces(marker_color="green")
    )

    col1.header("Top 10 Songs")
    col1.write(song_fig)

    unique_count_songs = len(recently_played_df["song"].unique())

    songs = song_df["song"].tolist()[0]
    song_duration = song_df["duration"].tolist()[0]

    song_duration = (
        f"{song_duration} Minutes"
        if song_duration < 60
        else f"{round(song_duration/60,2)}"
    )

    song_description = f"""
    You have listened <b>{unique_count_songs} songs</b> out of which you liked <b><u>{songs}</u></b> the most as you spent <b>{song_duration}</b>.
    """
    col1.markdown(song_description, unsafe_allow_html=True)
    # End of Top 10 Songs Calculations ------>

    # Top 10 Artists Calculations ----->
    artist_df = (
        recently_played_df.groupby("artist")
        .agg({"duration": "sum", "artist_image": "first"})
        .sort_values("duration", ascending=False)
        .reset_index()
    )
    artist_df["duration"] = round(artist_df["duration"] / 60000, 2)
    artist_df = artist_df.sort_values("duration", ascending=False).head(10)

    artist_fig = (
        px.bar(artist_df, x="artist", y="duration", text="duration")
        .update_layout(
            xaxis_title="Artists",
            yaxis_title="Duration (Minutes)",
            showlegend=False,
            height=600,
            width=600,
        )
        .update_traces(marker_color="green")
    )

    col2.header("Top 10 Artists")
    col2.write(artist_fig)

    unique_count_artists = len(recently_played_df["artist"].unique())
    artists = artist_df["artist"].tolist()
    artists_durations = artist_df["duration"].tolist()
    artists_description = f"You have listened <b>{unique_count_artists} artists</b> out of which you liked <b><u>{artists[0]}</u></b> the most as you spent <b>{str(round(artists_durations[0])) +' Minutes' if round(artists_durations[0]) < 60 else str(round(artists_durations[0]/60)) +' Hours'}.</b>"
    col2.markdown(artists_description, unsafe_allow_html=True)

    # End Of Top 10 Artists Calculations ----->

    # Top 10 Albums Calculations ----->
    album_df = recently_played_df.groupby("album_name")["duration"].sum().reset_index()
    album_df["duration"] = round(album_df["duration"] / 60000, 2)
    album_df = album_df.sort_values("duration", ascending=False).head(10)

    album_fig = (
        px.bar(album_df, x="album_name", y="duration", text="duration")
        .update_layout(
            xaxis_title="Albums",
            yaxis_title="Duration (Minutes)",
            showlegend=False,
            height=600,
            width=600,
        )
        .update_traces(marker_color="green")
    )

    col1.header("Top 10 Albums")
    col1.write(album_fig)

    unique_count_albums = len(recently_played_df["album_name"].unique())
    albums = album_df["album_name"].tolist()[0]
    album_duration = album_df["duration"].tolist()[0]

    album_duration = (
        f"{album_duration} Minutes"
        if album_duration < 60
        else f"{round(album_duration/60,2)} Hours"
    )

    album_description = f"You have listened <b>{unique_count_albums} albums</b> out of which you liked <b><u>{albums}</u></b> the most as you spent <b>{album_duration}.</b>"
    col1.write(album_description, unsafe_allow_html=True)
    # End Top 10 Albums Calculations ----->

    explicit_df = recently_played_df.groupby("explicit")["duration"].sum().reset_index()
    explicit_df["duration"] = round(explicit_df["duration"] / 60000, 2)

    explicit_fig = go.Figure(
        data=[
            go.Pie(
                labels=explicit_df["explicit"],
                values=explicit_df["duration"],
                pull=[0.2, 0, 0, 0],
            ),
        ]
    ).update_traces(marker=dict(colors=["red", "green"]))
    explicit_fig.update_layout(height=600, width=600)

    col2.header("Explicit vs Non Explicit Content")
    col2.write(explicit_fig)

    top_explicit_df = recently_played_df[
        recently_played_df["explicit"] == "Explicit Content"
    ]
    top_explicit_df = top_explicit_df.groupby("song")["duration"].sum().reset_index()
    top_explicit_df["duration"] = round(top_explicit_df["duration"] / 60000, 2)
    top_explicit_df = top_explicit_df.sort_values("duration", ascending=False)

    top_non_explicit_df = recently_played_df[
        recently_played_df["explicit"] == "Non Explicit Content"
    ]
    top_non_explicit_df = (
        top_non_explicit_df.groupby("song")["duration"].sum().reset_index()
    )
    top_non_explicit_df["duration"] = round(top_non_explicit_df["duration"] / 60000, 2)
    top_non_explicit_df = top_non_explicit_df.sort_values("duration", ascending=False)

    unique_explicit_count = len(top_explicit_df["song"].unique())
    unique_non_explicit_count = len(top_non_explicit_df["song"].unique())

    print(unique_explicit_count)
    top_explicit_song = (
        top_explicit_df["song"].tolist()[0] if unique_explicit_count else None
    )
    top_explicit_song_duration = (
        top_explicit_df["duration"].tolist()[0] if unique_explicit_count else None
    )

    if top_explicit_song_duration:
        top_explicit_song_duration = (
            f"{top_explicit_song_duration} Minutes"
            if top_explicit_song_duration < 60
            else f"{round(top_explicit_song_duration/60,2)} Hours"
        )

    top_non_explicit_song = (
        top_non_explicit_df["song"].tolist()[0] if unique_non_explicit_count else None
    )
    top_non_explicit_song_duration = (
        top_non_explicit_df["duration"].tolist()[0]
        if unique_non_explicit_count
        else None
    )

    if top_non_explicit_song_duration:
        top_non_explicit_song_duration = (
            f"{top_non_explicit_song_duration} Minutes"
            if top_non_explicit_song_duration < 60
            else f"{round(top_non_explicit_song_duration/60,2)} Hours"
        )
    if top_explicit_song_duration:
        col2.write(
            f"You have listened <b>{unique_explicit_count} Explicit Content Songs</b> out of which you liked <b><u>{top_explicit_song}</u></b> the most as you spent <b>{top_explicit_song_duration}</b>.",
            unsafe_allow_html=True,
        )
    if top_non_explicit_song_duration:
        col2.write(
            f"You have listened <b>{unique_non_explicit_count} Non Explicit Content Songs</b> out of which you liked <b><u>{top_non_explicit_song}</u></b> the most as you spent <b>{top_non_explicit_song_duration}</b>.",
            unsafe_allow_html=True,
        )

    # Streams By Weekday
    col1.header("Streams Per Week Day")
    weekday_df = (
        recently_played_df.groupby(recently_played_df["played_at"].dt.strftime("%A"))[
            "duration"
        ]
        .sum()
        .reset_index()
    )
    weekday_df["duration"] = round(weekday_df["duration"] / 60000, 2)
    weekday_df["played_at"] = Categorical(
        weekday_df["played_at"],
        categories=[
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ],
        ordered=True,
    )
    weekday_df = weekday_df.sort_values("played_at")

    weekday_fig = (
        px.bar(weekday_df, x="played_at", y="duration", text="duration")
        .update_layout(
            xaxis_title="Day Of Week",
            yaxis_title="Duration (Minutes)",
            showlegend=False,
            height=600,
            width=600,
        )
        .update_traces(marker_color="green")
    )
    col1.write(weekday_fig)

    weekday_names = weekday_df["played_at"].tolist()
    weekday_durations = weekday_df["duration"].tolist()

    max_duration = max(weekday_durations)
    max_weekday_name = weekday_names[weekday_durations.index(max_duration)]

    max_duration_describtion = (
        f"{max_duration} Minutes"
        if max_duration < 60
        else f"{round(max_duration/60,2)} Hours"
    )

    col1.markdown(
        f"On **{max_weekday_name}** You Have Spent **{max_duration_describtion}**."
    )
    # Weekday vs Weekend
    col2.header("Weekends vs Weekdays")
    weekday_end_df = (
        recently_played_df.groupby("day_type")["duration"].sum().reset_index()
    )
    weekday_end_df["duration"] = round(weekday_end_df["duration"] / 60000, 2)

    weekday_end_fig = px.bar(
        weekday_end_df, x="day_type", y="duration", text="duration", color="day_type"
    ).update_layout(
        xaxis_title="Weekday/Weekend",
        yaxis_title="Duration (Minutes)",
        showlegend=False,
        height=600,
        width=600,
    )

    weekday_end_names = weekday_end_df["day_type"].tolist()[0]
    weekday_end_duration = weekday_end_df["duration"].tolist()[0]
    weekday_end_duration = (
        f"{weekday_end_duration} Minutes"
        if weekday_end_duration < 60
        else f"{round(weekday_end_duration/60,2)} Hours."
    )

    col2.write(weekday_end_fig)
    col2.markdown(
        f"You spend most of your time listening to songs in **{weekday_end_names}s** with a duration of **{weekday_end_duration}**"
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Top Decades
    decades_df = recently_played_df
    decades_df["decade"] = decades_df["release_date"].apply(decades.get_decade)
    decades_df = decades_df.groupby("decade")["duration"].sum().reset_index()
    decades_df["duration"] = round(decades_df["duration"] / 60000, 2)
    decades_df = decades_df.sort_values("duration", ascending=False)

    decades_name = decades_df["decade"].tolist()[0]
    decades_duration = (
        f"{round(decades_df['duration'].tolist()[0]/60)} Hours"
        if decades_df["duration"].tolist()[0] > 60
        else f"{decades_df['duration'].tolist()[0]} Minutes"
    )

    decades_fig = (
        px.bar(decades_df, x="decade", y="duration", text="duration")
        .update_layout(
            xaxis_title="Decades",
            yaxis_title="Duration (Minutes)",
            showlegend=False,
            height=600,
            width=600,
        )
        .update_traces(marker_color="green")
    )

    col2.header("Top Decades")
    col2.write(decades_fig)
    col2.markdown(
        f"You Liked Listening To **{decades_name}** songs as you have spent **{decades_duration}**"
    )

    # Top 5 Genres
    genres_df = (
        recently_played_df[recently_played_df["genres"] != ""]
        .groupby("genres")["duration"]
        .sum()
        .reset_index()
    )
    genres_df["duration"] = round(genres_df["duration"] / 60000, 2)
    genres_df = genres_df.sort_values("duration", ascending=False).head(5)

    genres_fig = go.Figure(
        data=[
            go.Pie(
                labels=genres_df["genres"],
                values=genres_df["duration"],
                pull=[0.2, 0, 0, 0],
            ),
        ]
    )

    genres_fig.update_layout(height=600, width=600)

    col1.header("Top 5 Genres")
    col1.write(genres_fig)
    genres = genres_df["genres"].tolist()[0]
    genres_durations = genres_df["duration"].tolist()[0]
    col1.markdown(
        f"You mostly like to listen to **{genres}** as you have spent **{str(genres_durations)+' Minutes' if genres_durations < 60 else str(round(genres_durations/60,2))+' Hours'}** !!"
    )

    st.header("Audio Features")

    kpis = [
        "danceability",
        "energy",
        "valence",
        "loudness",
        "acousticness",
        "speechiness",
        "instrumentalness",
    ]

    # Calculate the mean value for each audio feature
    means = recently_played_df[kpis].mean()

    # Create a DataFrame containing the means
    df = DataFrame({"kpi": kpis, "value": means})
    audio_feature_graph, audio_feature_data = st.columns(2)
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(visible=True),
        ),
        showlegend=False,
    )

    trace = go.Scatterpolar(r=df["value"], theta=df["kpi"], fill="toself")
    fig = go.Figure(data=[trace], layout=layout)
    audio_feature_graph.write(fig)

    df_2 = df.sort_values(by="value", ascending=False)
    features = df_2["kpi"].tolist()[0]

    energy = df[df["kpi"] == "energy"]["value"].tolist()[0]
    danceability = df[df["kpi"] == "danceability"]["value"].tolist()[0]
    valence = df[df["kpi"] == "valence"]["value"].tolist()[0]
    loudness = df[df["kpi"] == "loudness"]["value"].tolist()[0]
    acousticness = df[df["kpi"] == "acousticness"]["value"].tolist()[0]
    speechiness = df[df["kpi"] == "speechiness"]["value"].tolist()[0]
    instrumentalness = df[df["kpi"] == "instrumentalness"]["value"].tolist()[0]

    feature_info = {
        "energy": "enjoy energetic, fast-paced music.",
        "danceability": "enjoy dancing or upbeat music",
        "valence": "enjoy upbeat, positive music",
        "loudness": "enjoy loud, high-energy music",
        "acousticness": "enjoy acoustic or stripped-down music",
        "speechiness": "enjoy Rap Songs",
        "instrumentalness": "enjoy instrumental or ambient music",
    }

    audio_feature_data.markdown("### From Analyzing audio features pattern")
    audio_feature_data.markdown(f"You {feature_info[features]}")

    fav_artist_df = recently_played_df[recently_played_df["artist"] == artists[0]]
    fav_artist_img = fav_artist_df["artist_image"].unique().tolist()[0]
    fav_artist_name = fav_artist_df["artist"].unique().tolist()[0]
    fav_artist_duration = fav_artist_df["duration"].sum()
    fav_artist_id = fav_artist_df["artist_id"].unique().tolist()[0]

    suggested_songs = artist_meta.get_recommendations(
        fav_artist_id,
        energy,
        danceability,
        valence,
        loudness,
        acousticness,
        speechiness,
        instrumentalness,
    )

    with audio_feature_data.expander("Recommended Songs"):
        st.header("Songs you might like!")
        for data in suggested_songs:
            st.markdown(
                embed_spotify.embed_track("track", data["trackId"]),
                unsafe_allow_html=True,
            )

    artist_data = artist_meta.get_artist_meta(fav_artist_id)

    st.header("Your Favorite Artist")
    artist_col1, artist_col2 = st.columns(2)

    try:
        artist_col1.image(fav_artist_img, width=300)
    except:
        artist_col1.image(
            "https://img.icons8.com/?size=400&id=65342&format=png", width=300
        )
    artist_col2.markdown(f"## {fav_artist_name}")
    artist_col2.markdown(
        f"You have spent: **{milliseconds_duration.get(fav_artist_duration)}**"
    )
    artist_col1.markdown(f"Total Followers: **{artist_data['followers']:,}**")

    st.header(f"Similar Artists You may like: ")
    similar_artists = artist_meta.releated_artist(fav_artist_id)[:5]

    if similar_artists:
        similar_artists_cols = st.columns(len(similar_artists))

        for i, col in enumerate(similar_artists_cols):
            col.image(similar_artists[i]["image"])
            col.markdown(f"**{similar_artists[i]['name']}**")
            col.markdown(f"Followers: **{similar_artists[i]['followers']:,}**")
            col.markdown(f"Genres: **{similar_artists[i]['genres']}**")
    else:
        st.markdown(f"No Similar Artists Found based on your favorite artist.")

    # st.markdown(f"Your an **{genres}** Fan! ")
