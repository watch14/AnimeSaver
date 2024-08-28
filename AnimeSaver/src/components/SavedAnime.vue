<template>
    <div class="saved-anime-container">
        <h1>Saved Anime</h1>

        <!-- Filter Buttons -->
        <div class="filter-controls">
            <button @click="filter = 'all'" :class="{ active: filter === 'all' }">All</button>
            <button @click="filter = 'watched'" :class="{ active: filter === 'watched' }">Watched</button>
            <button @click="filter = 'unwatched'" :class="{ active: filter === 'unwatched' }">Unwatched</button>

            <!-- Rating Filter -->
            <select v-model="ratingFilter" @change="applyFilter">
                <option value="">Score</option>
                <option v-for="rating in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" :key="rating" :value="rating">
                    {{ rating }} +
                </option>
            </select>
        </div>

        <div v-if="filteredAnimeList.length > 0" class="anime-grid">
            <div v-for="anime in filteredAnimeList" :key="anime.id" class="anime-card">
                <button @click="handleRemoveAnime(anime.id)" class="remove-button">X</button>
                <img @click="goToAnimePage(anime.id)" :src="anime.main_picture?.large" alt="Anime image"
                    class="anime-image" />
                <div class="anime-details">
                    <h2 class="anime-title" @click="goToAnimePage(anime.id)">{{ anime.title }}</h2>
                    <div class="rating-container">
                        <p class="anime-rating-text">{{ anime.mean ? anime.mean.toFixed(1) : 'N/A' }} / 10</p>
                        <button @click="toggleWatchedStatus(anime.id, anime.watched)"
                            :class="['status-button', { 'watched': anime.watched, 'unwatched': !anime.watched }]">
                            {{ anime.watched ? 'Watched' : 'Unwatched' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <div v-if="filteredAnimeList.length > 0" class="pagination-controls">
            <button @click="prevPage" :disabled="currentPage <= 1">Previous</button>
            <span class="page-number">Page {{ currentPage }} of {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage >= totalPages">Next</button>
        </div>

        <div v-else>
            <p>No saved anime found.</p>
        </div>
    </div>
</template>

<script>
import auth from '@/utils/auth';

export default {
    data() {
        return {
            animeList: [],
            filteredAnimeList: [],
            currentPage: 1,
            limit: 14,
            totalPages: 1,
            filter: 'all', // Default filter
            ratingFilter: '' // Default rating filter
        };
    },
    async created() {
        await this.fetchAnimeData();
    },
    watch: {
        filter() {
            this.applyFilter();
            this.updatePagination();
        },
        ratingFilter() {
            this.applyFilter();
            this.updatePagination();
        },
        currentPage() {
            this.updatePagination();
        }
    },
    methods: {
        async fetchAnimeData() {
            const offset = (this.currentPage - 1) * this.limit;
            try {
                const userAnimeObjects = await auth.getUserAnimeList();
                const userAnimeIds = userAnimeObjects.map(anime => anime.id.toString());

                if (userAnimeIds.length > 0) {
                    const requests = userAnimeIds.map(id =>
                        fetch(`http://localhost:5000/api/anime/${id}?fields=id,title,mean,num_episodes,genres,synopsis,start_date,end_date,status`)
                    );

                    const responses = await Promise.all(requests);
                    const results = await Promise.all(
                        responses.map(async response => {
                            if (!response.ok) {
                                throw new Error(`HTTP error! status: ${response.status}`);
                            }
                            return response.json();
                        })
                    );

                    this.animeList = results.map(data => ({
                        ...data,
                        watched: userAnimeObjects.find(anime => anime.id.toString() === data.id.toString()).watched
                    }));

                    this.applyFilter();
                    this.updatePagination();
                } else {
                    this.animeList = [];
                    this.filteredAnimeList = [];
                    this.totalPages = 1;
                }
            } catch (error) {
                console.error('Error fetching anime data:', error);
                this.animeList = [];
                this.filteredAnimeList = [];
                this.totalPages = 1;
            }
        },
        applyFilter() {
            let list = this.animeList;

            if (this.filter === 'watched') {
                list = list.filter(anime => anime.watched);
            } else if (this.filter === 'unwatched') {
                list = list.filter(anime => !anime.watched);
            }

            if (this.ratingFilter) {
                list = list.filter(anime => anime.mean && anime.mean >= this.ratingFilter);
            }

            this.filteredAnimeList = list;
            this.updatePagination();
        },
        updatePagination() {
            this.totalPages = Math.ceil(this.filteredAnimeList.length / this.limit);
            const offset = (this.currentPage - 1) * this.limit;
            this.filteredAnimeList = this.filteredAnimeList.slice(offset, offset + this.limit);
        },
        async handleRemoveAnime(animeId) {
            const loggedIn = await auth.isLoggedIn();
            if (loggedIn) {
                try {
                    await auth.removeAnimeFromUserList(animeId);
                    await this.fetchAnimeData();
                } catch (error) {
                    console.error('Error removing anime from user list:', error);
                }
            } else {
                alert('Please log in to remove anime from your list.');
            }
        },
        async toggleWatchedStatus(animeId, currentStatus) {
            const loggedIn = await auth.isLoggedIn();
            if (loggedIn) {
                try {
                    const newStatus = !currentStatus;
                    await auth.updateAnimeWatchedStatus(animeId, newStatus);
                    this.animeList = this.animeList.map(anime =>
                        anime.id.toString() === animeId.toString() ? { ...anime, watched: newStatus } : anime
                    );
                    this.applyFilter(); // Reapply filter after updating the status
                } catch (error) {
                    console.error('Error updating watched status:', error.response ? error.response.data : error.message);
                    alert('Error updating watched status. Please try again.');
                }
            } else {
                alert('Please log in to update the watched status.');
            }
        },
        goToAnimePage(animeId) {
            this.$router.push({ name: 'AnimeDetail', params: { id: animeId.toString() } });
        },
        prevPage() {
            if (this.currentPage > 1) {
                this.currentPage--;
                this.updatePagination();
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
                this.updatePagination();
            }
        }
    }
};
</script>


<style scoped>
.saved-anime-container {
    text-align: center;
    padding: 20px;
}

.filter-controls select {
    padding: 10px;
    font-size: 1em;
    background-color: #7a7681;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin: 0 5px;
    transition: background-color 0.3s ease;
}

.filter-controls select:hover {
    background-color: #411d7a;
}

.filter-controls {
    margin-bottom: 20px;
}

.filter-controls button {
    padding: 10px 20px;
    font-size: 1em;
    background-color: #7a7681;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    margin: 0 5px;
    transition: background-color 0.3s ease;
}

.filter-controls button.active {
    background-color: #411d7a;
}

.filter-controls button:hover {
    background-color: #411d7a;
}

.anime-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 16px;
    margin-top: 20px;
}

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
    max-width: 300px;
    margin: 0 auto;
    position: relative;
    /* Added for absolute positioning of the X button */
}

/* .anime-card:hover {
    transform: scale(1.02);
} */

.remove-button {
    position: absolute;
    top: 4px;
    right: 4px;
    background-color: #d84444;
    color: white;
    border: none;
    border-radius: 50%;
    width: 30px;
    height: 30px;
    display: flex;
    align-items: center;
    justify-content: center;
    cursor: pointer;
    font-size: 20px;
    font-weight: bold;
    transition: background-color 0.3s ease;
}

.remove-button:hover {
    background-color: #eb2d26;
}

img.anime-image {
    max-height: 600px;
    width: 100%;
    display: block;
    object-fit: cover;
}

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
    cursor: pointer;
}

.anime-title:hover {
    text-decoration: underline;
}

.anime-rating-text {
    font-size: 14px;
    font-weight: 600;
    color: #ffe600;
    margin: 0;
}

.rating-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
}

.status-button {
    padding: 10px 20px;
    font-size: 14px;
    font-weight: 600;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    transition: background-color 0.3s ease;
    margin-right: 10px;
}

.status-button.watched {
    background-color: #4caf50;
}

.status-button.watched:hover {
    background-color: #47c74b;
}

.status-button.unwatched {
    background-color: #f56c6c;
}

.status-button.unwatched:hover {
    background-color: #d43f3a;
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
</style>
