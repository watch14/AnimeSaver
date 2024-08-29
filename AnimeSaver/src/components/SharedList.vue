<template>
    <!-- Loader -->
    <div v-if="loading" class="loader"></div>

    <!-- Main Content -->
    <div v-if="!loading" class="ranking-results-container">
        <h1>{{ username }}'s Saved List</h1>

        <!-- Anime List -->
        <div v-if="animeList.length > 0" class="anime-grid">
            <div v-for="anime in animeList" :key="anime.id" class="anime-card">
                <img @click="goToAnimePage(anime.id)" :src="anime.main_picture?.large" alt="Anime image"
                    class="anime-image" />
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
    methods: {
        async fetchSharedList() {
            const offset = (this.currentPage - 1) * this.limit;
            this.loading = true;
            try {
                const response = await fetch(`http://localhost:5000/api/shared-list/${this.link_id}?limit=${this.limit}&offset=${offset}`);
                const data = await response.json();

                // Ensure data is in expected format
                this.animeList = Array.isArray(data.animeList) ? data.animeList : [];
                const userId = data['userId'] || 'Unknown'; // Get username from the response
                this.username = await auth.getUserById(userId);
                this.username = this.username.userName;

            } catch (error) {
                console.error('Error fetching shared list data:', error);
                this.animeList = [];
                this.username = 'Unknown';
            } finally {
                this.loading = false;
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
        async handleSaveRemoveAnime(animeId) {
            const loggedIn = await auth.isLoggedIn();
            if (loggedIn) {
                try {
                    if (this.isAnimeInUserList(animeId)) {
                        await auth.removeAnimeFromUserList(animeId); // Remove anime from user list
                        this.userAnimeList = this.userAnimeList.filter(id => id !== animeId.toString());
                    } else {
                        await auth.addAnimeToUserList(animeId); // Add anime to user list
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
            // Fetch new data if there's a possibility of more results
            if (this.animeList.length === this.limit) {
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
    padding: 20px;
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
    justify-content: space-between;
    width: 100%;
    height: 100%;
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
    justify-content: flex-end;
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
