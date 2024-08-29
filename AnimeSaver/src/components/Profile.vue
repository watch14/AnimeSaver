<template>
    <div class="profile-container">
        <div v-if="loading" class="loader"></div>

        <div v-if="!loading && userData">
            <div class="user-info">
                <h2>Welcome, {{ userData.userName }}!</h2>
                <!-- <button @click="logout" class="logout-button">Log Out</button> -->
                <button @click="redirectToSavedAnime" class="redirect-button"> <router-link to="/saved-anime">Saved
                        Anime</router-link>
                </button>
            </div>

            <div v-if="animeList.length > 0" class="anime-stats">
                <h3>Stats</h3>
                <div class="stats-container">
                    <div class="stats-item">
                        <h4>Total Anime</h4>
                        <p>{{ totalAnimeCount }}</p>
                    </div>
                    <div class="stats-item-watched">
                        <h4>Watched Anime</h4>
                        <p>{{ watchedAnimeCount }}</p>
                    </div>
                    <div class="stats-item-unwatched">
                        <h4>Unwatched Anime</h4>
                        <p>{{ unwatchedAnimeCount }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>


<script>
import auth from '@/utils/auth'; // Adjust the path as needed
import SavedAnime from './SavedAnime.vue';

export default {
    components: {
        SavedAnime // Register the SavedAnime component
    },
    data() {
        return {
            userData: null,
            animeList: [],
            loading: true,
        };
    },
    async created() {
        await this.fetchUserData();
        await this.fetchUserAnimeList();
    },
    computed: {
        totalAnimeCount() {
            return this.animeList.length;
        },
        watchedAnimeCount() {
            return this.animeList.filter(anime => anime.watched).length;
        },
        unwatchedAnimeCount() {
            return this.animeList.filter(anime => !anime.watched).length;
        }
    },
    methods: {
        async fetchUserData() {
            const userId = localStorage.getItem('userId');
            if (userId) {
                try {
                    this.userData = await auth.getUserById(userId);
                } catch (error) {
                    console.error('Error fetching user data:', error);
                }
            } else {
                console.error('User ID not found in localStorage');
            }
        },
        async fetchUserAnimeList() {
            try {
                this.animeList = await auth.getUserAnimeList();
            } catch (error) {
                console.error('Error fetching user anime list:', error);
            } finally {
                this.loading = false; // Hide loader
            }
        },
        async updateWatchedStatus(animeId) {
            try {
                const watchedStatus = !this.isAnimeWatched(animeId);
                await auth.updateAnimeWatchedStatus(animeId, watchedStatus);
                await this.fetchUserAnimeList(); // Refresh the anime list
            } catch (error) {
                console.error('Error updating watched status:', error);
            }
        },
        isAnimeWatched(animeId) {
            const anime = this.animeList.find(item => item.id === animeId);
            return anime ? anime.watched : false;
        },
        logout() {
            auth.logout();
            this.$router.push({ name: 'Login' }); // Redirect to login page or home
        },
        goToAnimePage(animeId) {
            this.$router.push({ name: 'AnimeDetail', params: { id: animeId.toString() } });
        },
    },
};
</script>


<style scoped>
.profile-container {
    text-align: center;
    padding: 0 20px;
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

/* User Info Section */
.user-info {
    margin-bottom: 20px;
}

.logout-button {
    padding: 10px 20px;
    font-size: 16px;
    font-weight: 600;
    background-color: #f53b57;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.logout-button:hover {
    background-color: #e02e4f;
}

/* Anime Stats Section */


.anime-stats h3 {
    color: #561eaf;
    margin-bottom: 10px;
    font-size: 20px;
    font-weight: 600;
}

.stats-container {
    margin: ;
    display: flex;
    flex-direction: row;
    justify-content: center;
    flex-wrap: wrap;
    gap: 20px;
}

.stats-item,
.stats-item-watched,
.stats-item-unwatched {
    margin: 10px 0;
    background-color: #411d7a;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 200px;
}

.stats-item:hover,
.stats-item-watched:hover,
.stats-item-unwatched:hover {

    background-color: #551dad;
}


.stats-item h4,
.stats-item-watched h4,
.stats-item-unwatched h4 {
    margin: 0;
    font-size: 18px;
    padding-bottom: 10px;
    color: #b897ee;
}

.stats-item p,
.stats-item-watched p,
.stats-item-unwatched p {
    font-size: 36px;
    font-weight: 600;
    margin: 5px 0 0;
    color: #ffffff;
}

.redirect-button {
    padding: 12px 24px;
    font-size: 16px;
    background-color: #411d7a;
    color: white;
    border: none;
    border-radius: 8px;
    transition: background-color 0.3s ease;
    cursor: pointer;
}

.redirect-button:hover {
    background-color: #6d24e4;
}

.redirect-button a {
    color: #ffffff;
    text-decoration: none;
}
</style>
