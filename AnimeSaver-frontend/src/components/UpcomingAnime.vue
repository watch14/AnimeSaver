<template>
    <!-- Loader -->
    <div v-if="loading" class="loader"></div>

    <div v-if="!loading" class="anime-grid">
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
    </div>
</template>

<script>
import auth from '@/utils/auth'; // Adjust the path as needed

export default {
    props: {
        initialRankingType: {
            type: String,
            default: 'upcoming' // Default to 'upcoming' if not provided
        }
    },
    data() {
        return {
            animeList: [],
            limit: 21, // Adjust limit as needed
            userAnimeList: [], // User's saved anime IDs
            loading: false, // Loading state
            rankingType: this.initialRankingType, // Use the prop to initialize rankingType
        };
    },
    async created() {
        await this.loadUserAnimeList(); // Load the user's anime list when the component is created
        await this.fetchAnimeRanking(); // Fetch anime ranking data
    },
    methods: {
        async fetchAnimeRanking() {
            this.loading = true; // Show loader
            try {
                const response = await fetch(`https://animesaver-backend.onrender.com/api/anime/ranking?ranking_type=${this.rankingType}&limit=${this.limit}&fields=id,title,mean,num_episodes,main_picture`);
                const responseData = await response.json();

                // Check if the 'data' field is an array and map it
                if (Array.isArray(responseData.data)) {
                    this.animeList = responseData.data.map(item => item.node); // Access the 'node' property
                } else {
                    console.error('Data is not an array:', responseData);
                    this.animeList = [];
                }
            } catch (error) {
                console.error('Error fetching anime ranking data:', error);
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
        }
    }
};
</script>

<style scoped>
/* Styling for the grid container */
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
