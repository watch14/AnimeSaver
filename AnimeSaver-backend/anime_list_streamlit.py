import streamlit as st
import requests
import json
import os

# API configuration using your credentials
CLIENT_ID = 'dfe48b7bb1e8af63efd5cd846dee89db'

WATCHLIST_FILE = 'watchlist.json'

# Function to fetch anime search results from MyAnimeList API
def search_anime(query):
    try:
        url = f'https://api.myanimelist.net/v2/anime?q={query}&limit=10&fields=id,title,main_picture,synopsis,mean,num_episodes,start_date,end_date,genres,status'
        headers = {
            'X-MAL-CLIENT-ID': CLIENT_ID
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()['data']
    except requests.RequestException as e:
        st.error(f"API request failed: {e}")
        return []

# Function to load watchlist from JSON file
def load_watchlist():
    if os.path.exists(WATCHLIST_FILE):
        with open(WATCHLIST_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save watchlist to JSON file
def save_watchlist(anime_list):
    with open(WATCHLIST_FILE, 'w') as f:
        json.dump(anime_list, f, indent=4)

# Function to add anime to watchlist
def add_to_watchlist(anime_data, anime_list):
    print(f"Attempting to add: {anime_data}")
    if not any(anime['id'] == anime_data['id'] for anime in anime_list):
        anime_list.append(anime_data)
        save_watchlist(anime_list)
        st.success(f"{anime_data['title']} added to watchlist!")
    else:
        st.warning("This anime is already in your watchlist.")
    print(f"Watchlist updated: {anime_list}")


# Function to remove anime from watchlist
def remove_from_watchlist(anime_id, anime_list):
    updated_list = [anime for anime in anime_list if anime['id'] != anime_id]
    save_watchlist(updated_list)
    return updated_list

# Streamlit app layout
def main():
    st.title("Anime Watchlist")

    anime_list = load_watchlist()

    # Search for anime
    st.header("Search for Anime")
    anime_name = st.text_input("Enter the name of an anime to search:", key="anime_search_input")

    if st.button("Search", key="search_button"):
        search_results = search_anime(anime_name)
        if search_results:
            st.subheader("Search Results")
            for result in search_results:
                anime_data = result['node']
                
                # Create two columns
                col1, col2 = st.columns([1, 2])

                # Left column: Anime title and picture
                with col1:
                    st.image(anime_data['main_picture']['large'])
                    st.subheader(anime_data['title'])
                
                # Right column: Anime details
                with col2:
                    st.write(f"**Score:** {anime_data.get('mean', 'N/A')}")
                    st.write(f"**Episodes:** {anime_data.get('num_episodes', 'N/A')}")
                    st.write(f"**Status:** {anime_data.get('status', 'N/A')}")
                    st.write(f"**Start Date:** {anime_data.get('start_date', 'N/A')}")
                    st.write(f"**End Date:** {anime_data.get('end_date', 'N/A')}")
                    genres = ', '.join([genre['name'] for genre in anime_data.get('genres', [])])
                    st.write(f"**Genres:** {genres}")
                    st.write(f"**Synopsis:** {anime_data.get('synopsis', 'No synopsis available.')}")
                
                # Debug print for button keys
                add_button_key = f"add_{anime_data['id']}"

                # Add to Watchlist button
                if st.button(f"Add {anime_data['title']} to Watchlist", key=add_button_key):
                    st.write(f"Button clicked for: {anime_data['title']}")
                    print(f"Button clicked for: {anime_data['title']}")
                    add_to_watchlist(anime_data, anime_list)
                    st.experimental_rerun()
                else:
                    st.write(f"Button not clicked for: {anime_data['title']}")

    # Display the watchlist
    st.header("Your Watchlist")
    search_query = st.text_input("Search in your watchlist:", key="watchlist_search_input")

    if search_query:
        filtered_list = [anime for anime in anime_list if search_query.lower() in anime['title'].lower()]
    else:
        filtered_list = anime_list

    if filtered_list:
        for anime in filtered_list:
            col1, col2 = st.columns([1, 2])

            # Left column: Anime title and picture
            with col1:
                st.image(anime['main_picture']['large'])
                st.subheader(anime['title'])

            # Right column: Anime details
            with col2:
                st.write(f"**Score:** {anime.get('mean', 'N/A')}")
                st.write(f"**Episodes:** {anime.get('num_episodes', 'N/A')}")
                st.write(f"**Status:** {anime.get('status', 'N/A')}")
                st.write(f"**Start Date:** {anime.get('start_date', 'N/A')}")
                st.write(f"**End Date:** {anime.get('end_date', 'N/A')}")
                genres = ', '.join([genre['name'] for genre in anime.get('genres', [])])
                st.write(f"**Genres:** {genres}")
                st.write(f"**Synopsis:** {anime.get('synopsis', 'No synopsis available.')}")
                
                # Debug print for button keys
                remove_button_key = f"remove_{anime['id']}"
                print(f"Remove button key: {remove_button_key}")

                if st.button(f"Remove {anime['title']}", key=remove_button_key):
                    print(f"Removing from watchlist: {anime['title']}")
                    anime_list = remove_from_watchlist(anime['id'], anime_list)
                    st.experimental_rerun()
    else:
        st.write("No anime found in your watchlist.")

if __name__ == "__main__":
    main()
