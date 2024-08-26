<template>
    <div class="search-results-container">
        <h1>Search</h1>
        <div class="search-bar">
            <input v-model="query" @keyup.enter="searchAnime" placeholder="Search for anime..." class="search-input" />
            <button @click="searchAnime" class="search-button">Search</button>
        </div>
        <div v-if="animeList.length > 0" class="anime-grid">
            <div v-for="anime in animeList" :key="anime.id" class="anime-card">
                <img @click="goToAnimePage(anime.id)" :src="anime.main_picture?.large" alt="Anime image"
                    class="anime-image" />
                <div class="anime-details">
                    <h2 class="anime-title">{{ anime.title }}</h2>
                    <div class="rating-container">
                        <p class="anime-rating-text">{{ anime.mean ? anime.mean.toFixed(1) : 'N/A' }} / 10</p>
                        <button @click="handleAddAnime(anime.id)" class="log-button">
                            {{ isAnimeInUserList(anime.id) ? 'Remove from List' : 'Add to List' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="animeList.length > 0" class="pagination-controls">
            <button @click="prevPage" :disabled="currentPage <= 1">Previous</button>
            <span class="page-number">Page {{ currentPage }}</span>
            <button @click="nextPage" :disabled="animeList.length < limit">Next</button>
        </div>
    </div>
</template>

<script>
import auth from '@/utils/auth'; // Adjust the path as needed

export default {
    data() {
        return {
            query: this.$route.query.q || '',
            animeList: [],
            currentPage: 1,
            limit: 14,
            userAnimeList: [] // This will hold the IDs of the anime saved by the user
        };
    },
    async created() {
        await this.loadUserAnimeList(); // Load the user's anime list when the component is created
        await this.fetchAnimeData(); // Fetch anime data based on the initial query
    },
    watch: {
        '$route.query.q': 'fetchAnimeData' // Watch for changes in the query parameter and fetch new data
    },
    methods: {
        async searchAnime() {
            this.currentPage = 1;
            this.$router.push({ name: 'SearchResults', query: { q: this.query } });
        },
        async fetchAnimeData() {
            this.query = this.$route.query.q || ''; // Update the query from the route
            const offset = (this.currentPage - 1) * this.limit;
            try {
                const response = await fetch(`http://localhost:5000/api/anime/search?q=${this.query}&limit=${this.limit}&offset=${offset}&fields=id,title,mean,num_episodes,genres,synopsis,start_date,end_date,status`);
                const data = await response.json();
                if (Array.isArray(data.data)) {
                    this.animeList = data.data.map(item => item.node);
                } else {
                    console.error('Data is not an array:', data);
                    this.animeList = [];
                }
            } catch (error) {
                console.error('Error fetching anime data:', error);
                this.animeList = [];
            }
        },
        async loadUserAnimeList() {
            try {
                const userAnimeObjects = await auth.getUserAnimeList();
                this.userAnimeList = userAnimeObjects.map(anime => anime.id.toString()); // Extract only the IDs and convert them to strings
            } catch (error) {
                console.error('Error fetching user anime list:', error);
                this.userAnimeList = [];
            }
        },
        isAnimeInUserList(animeId) {
            return this.userAnimeList.includes(animeId.toString()); // Check if the anime ID is in the user's list
        },
        async handleAddAnime(animeId) {
            const loggedIn = await auth.isLoggedIn();
            if (loggedIn) {
                try {
                    if (this.isAnimeInUserList(animeId)) {
                        await auth.removeAnimeFromUserList(animeId); // Remove anime from the user's list
                        this.userAnimeList = this.userAnimeList.filter(id => id !== animeId.toString());
                    } else {
                        await auth.addAnimeToUserList(animeId); // Add anime to the user's list
                        this.userAnimeList.push(animeId.toString());
                    }
                } catch (error) {
                    console.error('Error updating user anime list:', error);
                }
            } else {
                alert('Please log in to add or remove anime from your list.');
            }
        },
        goToAnimePage(animeId) {
            this.$router.push({ name: 'AnimeDetail', params: { id: animeId.toString() } });
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.fetchAnimeData();
            }
        },
        nextPage() {
            if (this.animeList.length === this.limit) {
                this.currentPage++;
                this.fetchAnimeData();
            }
        }
    }
};
</script>

<style scoped>
/* Reuse styles from the previous search results page */
/* Styling for the container */
.search-results-container {
    text-align: center;
    padding: 20px;
}

/* Styling for the search bar */
.search-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}

.search-input {
    padding: 10px;
    font-size: 1em;
    border: 1px solid #5b22b6;
    border-radius: 8px 0 0 8px;
    outline: none;
    width: 300px;
}

.search-button {
    padding: 10px 20px;
    font-size: 1em;
    background-color: #5b22b6;
    color: white;
    border: none;
    border-radius: 0 8px 8px 0;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.search-button:hover {
    background-color: #411d7a;
}

/* Styling for the grid container */
.anime-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
    margin-top: 20px;
}

/* Styling for each anime card */
.anime-card {
    border: 1px solid #5b22b6;
    border-radius: 8px;
    overflow: hidden;
    background-color: #411d7a;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s ease;
    display: flex;
    flex-direction: column;
    width: 100%;
    height: 100%;
}

.anime-card:hover {
    transform: scale(1.02);
}

/* Styling for the image */
img.anime-image {
    max-height: 600px;
    width: 100%;
    display: block;
    object-fit: cover;
}

/* Styling for the details section */
.anime-details {
    height: 100%;
    padding: 16px;
    color: white;
    text-align: left;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.anime-title {
    font-size: 20px;
    margin: 0;
    margin-bottom: 8px;
    font-weight: 600;
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-clamp: 2;
}

/* Rating text styling */
.anime-rating-text {
    font-size: 14px;
    font-weight: 600;
    color: #ffe600;
    margin: 0;
}

/* Container for rating and buttons */
.rating-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Heart icon styling */
.heart-icon {
    font-size: 24px;
    margin-right: 10px;
    cursor: pointer;
}

.hearted {
    color: red;
}

.log-button {
    padding: 10px 30px;
    font-size: 16px;
    font-weight: 600;
    background-color: #7a2cf8;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.log-button:hover {
    background-color: #e6be10;
}

/* Styling for pagination controls */
.pagination-controls {
    margin-top: 20px;
}

.pagination-controls button {
    padding: 10px 20px;
    font-size: 1em;
    background-color: #5b22b6;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin: 0 10px;
    transition: background-color 0.3s ease;
}

.pagination-controls button:hover {
    background-color: #411d7a;
}

.pagination-controls button:disabled {
    background-color: #d6d6d6;
    cursor: not-allowed;
}

.page-number {
    margin: 0 15px;
}
</style>
