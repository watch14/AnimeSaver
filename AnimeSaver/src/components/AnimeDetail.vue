<template>
    <!-- Loader -->
    <div v-if="loading" class="loader"></div>

    <div v-if="!loading" class="anime-detail-container">
        <div class="anime-image-left">
            <img :src="anime.main_picture?.large" alt="Anime image" class="anime-image" />

            <div class="buttonss">
                <!-- Add/Remove Button -->
                <button @click="handleAddRemoveAnime" class="log-button">
                    {{ isAnimeInUserList ? 'Remove' : 'Save' }}
                </button>

                <!-- Watched/Unwatched Button -->
                <button v-if="isAnimeInUserList" @click="handleWatchedStatus"
                    :class="['watched-button', { 'watched': isAnimeWatched, 'unwatched': !isAnimeWatched }]">
                    {{ isAnimeWatched ? 'Watched' : 'Unwatched' }}
                </button>
            </div>
        </div>

        <div class="anime-info-right">
            <h1 class="anime-title">{{ anime.title }} {{ isAnimeWatched ? '(Watched)' : '(Unwatched)' }}</h1>
            <p class="anime-detail-text"><strong>Rating:</strong> {{ anime.mean ? anime.mean.toFixed(1) : 'N/A' }} / 10
            </p>
            <p class="anime-detail-text"><strong>Episodes:</strong> {{ anime.num_episodes }}</p>
            <p class="anime-date-text">{{ formatDates(anime.start_date, anime.end_date) }}</p>
            <p class="anime-detail-text"><strong>Genres:</strong> {{ anime.genres?.map(genre => genre.name).join(', ')
                }}</p>
            <p class="anime-detail-text"><strong>Status:</strong> {{ formatStatus(anime.status) }}</p>
            <p class="anime-detail-text"><strong>Synopsis:</strong> {{ anime.synopsis || 'No synopsis available.' }}</p>
        </div>
    </div>
</template>

<script>
import auth from '@/utils/auth'; // Adjust the path as needed

export default {
    props: {
        id: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            anime: {},
            isAnimeInUserList: false,
            isAnimeWatched: false,
            loading: true
        };
    },
    async created() {
        this.numericId = Number(this.id);
        await this.fetchAnimeDetail();
        await Promise.all([this.checkIfAnimeInUserList(), this.checkIfAnimeWatched()]);
        this.loading = false;
    },
    methods: {
        async fetchAnimeDetail() {
            try {
                const response = await fetch(`http://localhost:5000/api/anime/${this.numericId}?fields=title,mean,num_episodes,genres,synopsis,start_date,end_date,status`);
                const data = await response.json();
                this.anime = data;
            } catch (error) {
                console.error("Error fetching anime detail:", error);
            }
        },
        async checkIfAnimeInUserList() {
            try {
                const userAnimeObjects = await auth.getUserAnimeList();
                const userAnimeList = userAnimeObjects.map(anime => anime.id);
                this.isAnimeInUserList = userAnimeList.includes(this.numericId); // Compare as numbers
            } catch (error) {
                console.error('Error fetching user anime list:', error);
                this.isAnimeInUserList = false;
            }
        },
        async checkIfAnimeWatched() {
            if (this.isAnimeInUserList) {
                try {
                    const userAnimeObjects = await auth.getUserAnimeList();
                    const animeObject = userAnimeObjects.find(anime => anime.id === this.numericId); // Compare as numbers
                    this.isAnimeWatched = animeObject ? animeObject.watched : false;
                } catch (error) {
                    console.error('Error fetching watched status:', error);
                    this.isAnimeWatched = false;
                }
            }
        },
        async handleAddRemoveAnime() {
            const loggedIn = await auth.isLoggedIn();
            if (!loggedIn) {
                alert('Please log in to add or remove anime from your list.');
                return;
            }

            try {
                if (this.isAnimeInUserList) {
                    await auth.removeAnimeFromUserList(this.numericId);
                    this.isAnimeInUserList = false;
                    this.isAnimeWatched = false; // Reset watched status when removed
                } else {
                    await auth.addAnimeToUserList(this.numericId);
                    this.isAnimeInUserList = true;
                }
            } catch (error) {
                console.error('Error updating user anime list:', error);
                alert('Error updating anime list. Please try again.');
            }
        },
        async handleWatchedStatus() {
            const loggedIn = await auth.isLoggedIn();
            if (!loggedIn) {
                alert('Please log in to mark anime as watched or unwatched.');
                return;
            }

            try {
                const newStatus = !this.isAnimeWatched;
                await auth.updateAnimeWatchedStatus(this.numericId, newStatus);
                this.isAnimeWatched = newStatus;
            } catch (error) {
                console.error('Error updating watched status:', error);
                alert('Error updating watched status. Please try again.');
            }
        },
        formatDates(start, end) {
            if (!start || !end) return "Unknown";
            const startYear = new Date(start).getFullYear();
            const endYear = new Date(end).getFullYear();
            return `${startYear} - ${endYear}`;
        },
        formatStatus(status) {
            switch (status) {
                case 'finished_airing':
                    return 'Finished Airing';
                case 'currently_airing':
                    return 'Currently Airing';
                case 'not_yet_aired':
                    return 'Not Yet Aired';
                default:
                    return 'Unknown Status';
            }
        }
    }
};
</script>

<style scoped>
.anime-detail-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 40px;
    padding: 60px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 1440px;
    margin-inline: auto;
}

.anime-image {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    min-width: 300px;
    height: auto;
}

.buttonss {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 20px;
}

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
    width: 100%;
    margin-top: 20px;
}

.log-button:hover {
    background-color: #6c15f8;
}

.watched-button {
    padding: 10px 30px;
    font-size: 16px;
    font-weight: 600;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    width: 100%;
    margin-top: 20px;
}

.watched-button.watched {
    background-color: #4caf50;
}

.watched-button.watched:hover {
    background-color: #47c74b;
}

.watched-button.unwatched {
    background-color: #f56c6c;
}

.watched-button.unwatched:hover {
    background-color: #d43f3a;
}

.anime-date-text {
    color: white;
    font-size: 16px;
    font-weight: 500;
    margin: 0;
}

.anime-info-right {
    display: flex;
    flex-direction: column;
    gap: 20px;
    color: white;
    width: 100%;
    margin: 0;
}

.anime-title {
    font-size: 36px;
    font-weight: 600;
    margin: 0;
}

.anime-detail-text {
    font-size: 16px;
    line-height: 1.5;
    font-weight: 500;
    margin: 0;
    width: 100%;
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

.anime-details-content {
    display: flex;
    flex-direction: row;
    width: 100%;
}
</style>