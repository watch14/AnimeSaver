<template>
    <!-- Loader -->
    <div v-if="loading" class="loader"></div>

    <!-- Main Content -->
    <div v-if="!loading" class="ranking-results-container">
        <h1>{{ username }}'s Saved List</h1>

        <!-- Anime List -->
        <div v-if="animeList.length > 0" class="anime-grid">
            <div v-for="anime in animeList" :key="anime.id" class="anime-card">
                <div class="anime-image-container">
                    <img @click="goToAnimePage(anime.id)" :src="anime.main_picture?.large" alt="Anime image"
                        class="anime-image" />
                </div>
                <div class="anime-details">
                    <h2 @click="goToAnimePage(anime.id)" class="anime-title">{{ anime.title }}</h2>
                    <div class="name-reate">
                        <p class="anime-episodes">Episodes: {{ anime.num_episodes || 'N/A' }}</p>
                        <p class="anime-rating-text">{{ anime.mean ? anime.mean.toFixed(1) : 'N/A' }}</p>
                    </div>
                    <button @click="handleSaveRemoveAnime(anime.id)" class="log-button">
                        {{ isAnimeInUserList(anime.id) ? 'Remove' : 'Save' }}
                    </button>
                </div>
            </div>
        </div>

        <!-- Pagination Controls -->
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
    props: {
        link_id: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            animeList: [],
            currentPage: 1,
            limit: 21, // Number of items per page
            userAnimeList: [], // User's saved anime IDs
            loading: false, // Loading state
            username: '', // Username of the person sharing the list
        };
    },
    async created() {
        await this.loadUserAnimeList(); // Load the user's anime list
        await this.fetchSharedList(); // Fetch shared list data
    },
    watch: {
        currentPage() {
            this.fetchSharedList(); // Re-fetch the data whenever the current page changes
        }
    },
    methods: {
        async fetchSharedList() {
            const offset = (this.currentPage - 1) * this.limit;
            this.loading = true;
            try {
                const response = await fetch(`https://animesaver-backend.onrender.com/api/shared-list/${this.link_id}`);
                const data = await response.json();

                // Ensure the 'animeList' is an array
                if (Array.isArray(data.animeList)) {
                    // Slice the data according to the current page and limit
                    this.animeList = data.animeList.slice(offset, offset + this.limit);
                } else {
                    console.error('animeList is not an array:', data);
                    this.animeList = [];
                }

                // Get the username of the list owner
                const userId = data.userId || 'Unknown';
                const userInfo = await auth.getUserById(userId);
                this.username = userInfo.userName || 'Unknown';

                console.log(`Page: ${this.currentPage}, Offset: ${offset}, Limit: ${this.limit}`);
                console.log('Displayed animeList:', this.animeList);


            } catch (error) {
                console.error('Error fetching shared list data:', error);
                this.animeList = [];
                this.username = 'Unknown';
            } finally {
                this.loading = false;
            }
        }

        ,

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

        async handleSaveRemoveAnime(animeId) {
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
                this.fetchSharedList();
            }
        },

        nextPage() {
            if (this.animeList.length === this.limit) { // Only navigate forward if the current page is full
                this.currentPage++;
                this.fetchSharedList();
            }
        },
    },
};
</script>


<style scoped>
/* Similar styles as your ranking results page */
.ranking-results-container {
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
