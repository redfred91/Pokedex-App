import pokemontcgsdk
import sqlite3
from tqdm import tqdm
import time
from urllib.error import URLError, HTTPError
from time import sleep

# Set up your API key
API_KEY = '9f330df3-229b-4e32-8862-2ef0fc1147d8'
pokemontcgsdk.config.API_KEY = API_KEY


def create_database():
    conn = sqlite3.connect('pokemon_cards.db')
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS cards (
            id TEXT PRIMARY KEY,
            name TEXT,
            set_name TEXT,
            rarity TEXT,
            artist TEXT,
            image_url TEXT
        )
    ''')
    conn.commit()
    conn.close()


def fetch_and_store_cards():
    conn = sqlite3.connect('pokemon_cards.db')
    c = conn.cursor()

    # Set up pagination
    page_size = 250
    page = 1
    total_cards = 0
    cards_fetched = []

    while True:
        attempts = 5
        for attempt in range(attempts):
            try:
                print(f"Fetching page {page}...")  # Debugging output
                response = pokemontcgsdk.Card.where(page=page).where(pageSize=page_size).all()
                print(f"Fetched {len(response)} cards on page {page}.")  # Debugging output
                cards_fetched.extend(response)
                total_cards += len(response)
                break
            except (HTTPError, URLError) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt < attempts - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
            except Exception as e:
                print(f"Rate limit hit or other error: {e}")
                sleep(60)  # Wait for 60 seconds before retrying

        if len(response) < page_size:
            # Last page, no more data to fetch
            break

        page += 1

        # Rate limiting: delay to avoid hitting the rate limit
        sleep(2)  # Sleep for 2 seconds between each page fetch to avoid rate limiting

    # Check if cards were fetched
    if not cards_fetched:
        print("No cards fetched.")
        return

    # Set up the progress bar
    for card in tqdm(cards_fetched, desc="Fetching and storing cards"):
        c.execute('''
            INSERT OR REPLACE INTO cards (id, name, set_name, rarity, artist, image_url)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (card.id, card.name, card.set.name, card.rarity, card.artist, card.images.small))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    create_database()
    fetch_and_store_cards()
    print("Database populated with Pokémon card data.")
