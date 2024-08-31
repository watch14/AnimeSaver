<template>
    <div class="profile-container">
        <div v-if="loading" class="loader"></div>

        <div v-if="!loading && userData">

            <div v-if="animeList.length > 0" class="anime-stats">
                <div class="user-info">
                    <h2>Welcome, {{ userData.userName }}!</h2>
                    <!-- <button @click="logout" class="logout-button">Log Out</button> -->

                </div>
                <p>Your Personal Anime Stats</p>

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
                <button @click="redirectToSavedAnime" class="redirect-button">
                    <router-link to="/saved-anime">Visit your saved anime</router-link>
                </button>
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
    margin: 0;
    margin-bottom: 40px;
    color: #dddddd;
    font-size: 24px;
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
.anime-stats {
    border: rgb(148, 148, 148) 1px solid;
    border-radius: 24px;
    padding: 60px 20px;
    margin: 20px 20px 40px;
    width: auto;
    margin-inline: auto;
}

.anime-stats p {
    color: #6e6e6e;
    margin: 0;
    margin-bottom: 10px;
    font-size: 20px;
    font-weight: 600;
}

.stats-container {
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
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 200px;
    transition: scale 0.5s ease;
}

.stats-item-watched {
    background-color: #4caf50;
}

.stats-item-unwatched {
    background-color: #f56c6c;
}


.stats-item:hover,
.stats-item-watched:hover,
.stats-item-unwatched:hover {

    scale: 1.01;

}


.stats-item h4,
.stats-item-watched h4,
.stats-item-unwatched h4 {
    margin: 0;
    font-size: 18px;
    padding-bottom: 10px;
    color: #ffffff;
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
    padding: 16px 0;
    font-size: 18px;
    font-weight: 600;
    background-color: #411d7a;
    color: white;
    border: none;
    border-radius: 8px;
    transition: background-color 0.3s ease;
    cursor: pointer;
    width: 250px;
    margin: 60px 0 0;
    border: transparent 1px solid;
}

.redirect-button:hover {
    background-color: #6d24e4;
    border: #dddddd 1px solid;
}

.redirect-button a {
    color: #ffffff;
    text-decoration: none;
}
</style>
