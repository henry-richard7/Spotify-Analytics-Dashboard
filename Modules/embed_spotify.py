def embed_track(embed_type, spotify_id):
    """
    Embeds a Spotify track or playlist using an iframe.

    Parameters:
        embed_type (str): The type of content to embed, either "track" or "playlist".
        spotify_id (str): The unique identifier for the Spotify track or playlist.

    Returns:
        str: The HTML code for embedding the Spotify content using an iframe.
    """
    iframe = (
        f"<iframe style='border-radius:12px' "
        f"src='https://open.spotify.com/embed/{embed_type}/{spotify_id}"
        f"?utm_source=generator&theme=0' "
        f"width='100%' height='80' frameBorder='0' allowfullscreen='' "
        f"allow='autoplay; clipboard-write; encrypted-media; fullscreen; "
        f"picture-in-picture' loading='lazy'></iframe>"
    )
    return iframe
