<template>
    <!-- Loader -->
    <div v-if="loading" class="loader"></div>

    <div v-if="!loading" class="season-results-container">
        <h1>Anime by Season</h1>

        <!-- Season, Year, and Rating Filter -->
        <div class="filter-container">
            <label for="year">Select Year:</label>
            <select id="year" v-model="year" @change="fetchAnimeBySeason">
                <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
            </select>
            <label for="season">Select Season:</label>
            <select id="season" v-model="season" @change="fetchAnimeBySeason">
                <option value="winter">Winter</option>
                <option value="spring">Spring</option>
                <option value="summer">Summer</option>
                <option value="fall">Fall</option>
            </select>
            <label for="rating-min">Min:</label>
            <select id="rating-min" v-model="ratingMin" @change="fetchAnimeBySeason">
                <option v-for="r in ratingOptions" :key="r" :value="r">{{ r }}</option>
            </select>
            <label for="rating-max">Max:</label>
            <select id="rating-max" v-model="ratingMax" @change="fetchAnimeBySeason">
                <option v-for="r in ratingOptions" :key="r" :value="r">{{ r }}</option>
            </select>
            <label for="sort-order">Sort:</label>
            <select id="sort-order" v-model="sortOrder" @change="fetchAnimeBySeason">
                <option value="asc">asce</option>
                <option value="desc">desc</option>
            </select>
        </div>

        <!-- Anime List -->
        <div v-if="animeList.length > 0" class="anime-grid">
            <div v-for="anime in animeList" :key="anime.id" class="anime-card">
                <div class="anime-image-container">
                    <img @click="goToAnimePage(anime.id)" :src="anime.main_picture?.large" alt="Anime image"
                        class="anime-image" />
                </div>
                <div class="anime-details">
                    <h2 class="anime-title">{{ anime.title }}</h2>
                    <div class="name-reate">
                        <p class="anime-episodes">Episodes: {{ anime.num_episodes || 'N/A' }}</p>
                        <p class="anime-rating-text">{{ anime.mean ? anime.mean.toFixed(1) : 'N/A' }}</p>
                    </div>
                    <button @click="handleAddAnime(anime.id)" class="log-button">
                        {{ isAnimeInUserList(anime.id) ? 'Remove' : 'Save' }}
                    </button>
                </div>
            </div>
        </div>

        <!-- Pagination Controls -->
        <div v-if="!loading && animeList.length > 0" class="pagination-controls">
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
            animeList: [],
            currentPage: 1,
            limit: 21, // Adjust limit as needed
            userAnimeList: [], // User's saved anime IDs
            loading: false, // Loading state
            season: '', // Will be set dynamically
            year: new Date().getFullYear(), // Default to the current year
            years: Array.from({ length: 20 }, (_, i) => new Date().getFullYear() - i), // Last 20 years
            ratingMin: 0, // Minimum rating filter
            ratingMax: 10, // Maximum rating filter
            ratingOptions: Array.from({ length: 11 }, (_, i) => i), // Rating options from 0 to 10
            sortOrder: 'desc' // Default to descending order
        };
    },
    async created() {
        this.season = this.getCurrentSeason(); // Set the current season
        await this.loadUserAnimeList(); // Load the user's anime list when the component is created
        await this.fetchAnimeBySeason(); // Fetch anime by season and year
    },
    methods: {
        getCurrentSeason() {
            const month = new Date().getMonth() + 1; // getMonth() returns 0-11, so add 1
            if (month >= 12 || month <= 2) return 'winter';
            if (month >= 3 && month <= 5) return 'spring';
            if (month >= 6 && month <= 8) return 'summer';
            if (month >= 9 && month <= 11) return 'fall';
        },
        async fetchAnimeBySeason() {
            const offset = (this.currentPage - 1) * this.limit;
            this.loading = true; // Show loader
            console.log(`Fetching with ratings: ${this.ratingMin} to ${this.ratingMax}, sort order: ${this.sortOrder}`); // Debugging log
            try {
                const response = await fetch(
                    `https://animesaver-backend.onrender.com/api/anime/season/${this.year}/${this.season}?sort=mean&sort_order=${this.sortOrder}&limit=${this.limit}&offset=${offset}&min_rating=${this.ratingMin}&max_rating=${this.ratingMax}&fields=id,title,mean,num_episodes,genres,status,main_picture`
                );
                const responseData = await response.json();

                if (Array.isArray(responseData.data)) {
                    this.animeList = responseData.data.map(item => item.node);
                } else {
                    console.error('Data is not an array:', responseData);
                    this.animeList = [];
                }
            } catch (error) {
                console.error('Error fetching anime by season:', error);
                this.animeList = [];
            } finally {
                this.loading = false; // Hide loader
            }
        },
        async loadUserAnimeList() {
            try {
                const userAnimeObjects = await auth.getUserAnimeList();
                this.userAnimeList = userAnimeObjects.map(anime => anime.id.toString());
            } catch (error) {
                console.error('Error fetching user anime list:', error);
                this.userAnimeList = [];
            }
        },
        isAnimeInUserList(animeId) {
            return this.userAnimeList.includes(animeId.toString());
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
                this.fetchAnimeBySeason();
            }
        },
        nextPage() {
            if (this.animeList.length === this.limit) {
                this.currentPage++;
                this.fetchAnimeBySeason();
            }
        }
    }
};
</script>




<style scoped>
/* Similar styles as your ranking results page */
.season-results-container {
    text-align: center;
    padding: 20px 40px;
}

/* Styling for the filter container */
.filter-container {
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    justify-content: center;
}

.filter-container label {
    margin: 0 8px 0 24px;
    font-size: 14px;
    font-weight: 700;
    color: rgb(153, 153, 153);

}

.filter-container select {
    padding: 6px 12px;
    font-size: 16px;
    font-weight: 700;

    border-radius: 8px;
    border: none;
    color: white;
    background-color: #411d7a;


}

.anime-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
    gap: 28px;
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
    justify-content: space-between;
    width: 100%;
    height: 100%;
}

.anime-image-container {
    width: 100%;
    /* Set your desired width */
    height: 100%;
    max-height: 400px;
    /* Set your desired height */
    overflow: hidden;
    /* Hide overflow to crop the image */
    display: flex;
    justify-content: center;
    align-items: center;
    /* Ensure positioning for absolute elements */
}

/* Styling for the image */
img.anime-image {
    width: 100%;
    height: 100%;
    object-fit: cover;

}

/* Styling for the details section */
.anime-details {
    height: 120px;
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
    white-space: nowrap;
    cursor: pointer;
}

.anime-title:hover {
    text-decoration: underline;
}

.name-reate {
    display: flex;
    justify-content: space-between;
    align-items: center;

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

/* Button styling */
.log-button {
    padding: 10px 30px;
    font-size: 16px;
    font-weight: 600;
    background-color: #7a2cf8;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.log-button:hover {
    background-color: #6b23e0;
}

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

/* Loader Styles */
.loader {
    margin: 20px;
    padding: 20px;
    font-size: 1.5em;
    color: #7a7681;
    border: 4px solid #f3f3f3;
    border-radius: 50%;
    border-top: 4px solid #411d7a;
    width: 60px;
    height: 60px;
    animation: spin 1s linear infinite;
    margin-inline: auto;
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
}
</style>
