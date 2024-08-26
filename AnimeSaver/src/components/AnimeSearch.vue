<template>
    <div class="anime-search-container">
        <h1>Anime Search</h1>
        <div class="search-bar">
            <input v-model="query" @keyup.enter="searchAnime" placeholder="Search for anime..." class="search-input" />
            <button @click="searchAnime" class="search-button">Search</button>
        </div>
        <div v-if="animeList.length > 0" class="anime-grid">
            <div v-for="anime in animeList" :key="anime.id" class="anime-card">
                <img :src="anime.main_picture?.medium" alt="Anime image" class="anime-image" />
                <div class="anime-details">
                    <h2 class="anime-title">{{ anime.title }}</h2>
                    <p class="anime-rating-text">{{ anime.mean ? anime.mean.toFixed(1) : 'N/A' }} / 10</p>
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
export default {
    data() {
        return {
            query: '',
            animeList: [],
            currentPage: 1,
            limit: 12
        };
    },
    methods: {
        async searchAnime() {
            this.currentPage = 1; // Reset to page 1 on new search
            await this.fetchAnimeData();
        },
        async fetchAnimeData() {
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
/* Styling for the container */
.anime-search-container {
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
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
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
.anime-image {
    width: 100%;
    height: 300px;
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
    overflow: hidden;
    text-overflow: ellipsis;
    display: -webkit-box;

    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    line-height: 1.2;
}

/* Rating text styling */
.anime-rating-text {
    font-size: 14px;
    color: #c2c2c2;
    margin: 0;
    margin-top: auto;
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

.pagination-controls {
    margin-top: 20px;
}

.page-number {
    margin: 0 15px;
}
</style>