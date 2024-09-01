<template>
    <!-- Loader -->
    <div v-if="loading" class="loader"></div>
    <div v-if="!loading" class="saved-anime-container">
        <h1>Saved Anime</h1>

        <!-- Filter Controls -->
        <div class="filter-controls">
            <button @click="generateShareableLink" class="share-button">Share</button>

            <!-- Filter Dropdown -->
            <select v-model="filter" @change="applyFilter" class="filter-dropdown">
                <option value="all">All</option>
                <option value="watched">Watched</option>
                <option value="unwatched">Unwatched</option>
            </select>

            <!-- Rating Filter -->
            <select v-model="ratingFilter" @change="applyFilter" class="rating-dropdown">
                <option value="">Score</option>
                <option v-for="rating in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]" :key="rating" :value="rating">
                    {{ rating }} +
                </option>
            </select>

            <!-- Sort Buttons -->
            <select v-model="sortOrder" @change="applyFilter" class="sort-dropdown">
                <option value="all">All</option>

                <option value="desc">Desc</option>
                <option value="asc">Asc</option>
            </select>

            <div v-if="shareableLink" class="share-link">
                <p>Share Your List: <a :href="shareableLink" target="_blank">{{ shareableLink }}</a></p>
            </div>
        </div>

        <!-- Anime List -->
        <div v-if="!loading && filteredAnimeList.length > 0" class="anime-grid">
            <div v-for="anime in filteredAnimeList" :key="anime.id" class="anime-card">
                <button @click="handleRemoveAnime(anime.id)" class="remove-button">X</button>
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
                    <button @click="toggleWatchedStatus(anime.id, anime.watched)"
                        :class="['status-button', { 'watched': anime.watched, 'unwatched': !anime.watched }]">
                        {{ anime.watched ? 'Watched' : 'Unwatched' }}
                    </button>
                </div>
            </div>
        </div>
        <div v-if="!loading && filteredAnimeList.length > 0" class="pagination-controls">
            <button @click="prevPage" :disabled="currentPage <= 1">Previous</button>
            <span class="page-number">Page {{ currentPage }} of {{ totalPages }}</span>
            <button @click="nextPage" :disabled="currentPage >= totalPages">Next</button>
        </div>

        <div v-if="!loading && filteredAnimeList.length === 0">
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
            limit: 18,
            totalPages: 1,
            filter: 'all', // Default filter
            ratingFilter: '', // Default rating filter
            sortOrder: 'asc', // Default sort order
            shareableLink: '', // Store the generated link
            userId: null, // Initialize userId
            loading: false // Loading state
        };
    },
    async created() {
        this.userId = localStorage.getItem("userId"); // Set userId on component creation
        await this.fetchAnimeData();
    },
    watch: {
        filter() {
            this.applyFilter();
        },

        ratingFilter() {
            this.applyFilter();
        },
        currentPage() {
            this.fetchAnimeData(); // Fetch data based on updated page number
        }
    },
    methods: {
        async fetchAnimeData() {
            this.loading = true; // Show loader
            const offset = (this.currentPage - 1) * this.limit;
            try {
                const userAnimeObjects = await auth.getUserAnimeList();
                // console.log('User Anime Objects:', userAnimeObjects); // Debugging line
                const userAnimeIds = userAnimeObjects.map(anime => anime.id.toString());

                if (userAnimeIds.length > 0) {
                    const requests = userAnimeIds.map(id =>
                        fetch(`https://animesaver-backend.onrender.com/api/anime/${id}?fields=id,title,mean,num_episodes,genres,synopsis,start_date,end_date,status`)
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

                    // console.log('Fetched Anime Data:', results); // Debugging line

                    this.animeList = results.map(data => ({
                        ...data,
                        watched: userAnimeObjects.find(anime => anime.id.toString() === data.id.toString()).watched
                    }));

                    // console.log('Processed Anime List:', this.animeList); // Debugging line

                    this.applyFilter();
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
            } finally {
                this.loading = false; // Hide loader
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

            // Apply sorting
            list.sort((a, b) => {
                if (this.sortOrder === 'asc') {
                    return (a.mean || 0) - (b.mean || 0);
                } else {
                    return (b.mean || 0) - (a.mean || 0);
                }
            });

            this.filteredAnimeList = list;
            this.totalPages = Math.ceil(this.filteredAnimeList.length / this.limit);
            this.updatePagination();
        },
        updatePagination() {
            const offset = (this.currentPage - 1) * this.limit;
            this.filteredAnimeList = this.filteredAnimeList.slice(offset, offset + this.limit);
        },
        async handleRemoveAnime(animeId) {
            const loggedIn = await auth.isLoggedIn();
            if (loggedIn) {
                try {
                    await auth.removeAnimeFromUserList(animeId);

                    // Update the local list by filtering out the removed anime
                    this.animeList = this.animeList.filter(anime => anime.id !== animeId);

                    // Reapply filter to update the displayed list
                    this.applyFilter();
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
            }
        },
        nextPage() {
            if (this.currentPage < this.totalPages) {
                this.currentPage++;
            }
        },
        async generateShareableLink() {
            const loggedIn = await auth.isLoggedIn();
            if (loggedIn && this.userId) {
                try {
                    const response = await fetch('https://animesaver-backend.onrender.com/api/share-list', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({
                            userId: this.userId,
                            animeList: this.animeList
                        })
                    });

                    const data = await response.json();
                    if (response.ok) {
                        this.shareableLink = data.link;

                        // Copy to clipboard
                        navigator.clipboard.writeText(this.shareableLink)
                            .then(() => {
                                // console.log('Link copied to clipboard!');
                                alert('Link copied to clipboard!');
                            })
                            .catch(err => {
                                console.error('Failed to copy link: ', err);
                            });
                    } else {
                        console.error('Error generating shareable link:', data);
                    }
                } catch (error) {
                    console.error('Error generating shareable link:', error);
                }
            } else {
                alert('Please log in to generate a shareable link.');
            }
        },
        sortBy(order) {
            this.sortOrder = order;
            this.applyFilter(); // Reapply filter to sort the list
        }
    }
};
</script>


<style scoped>
.saved-anime-container {
    text-align: center;
    padding: 20px 40px;
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
    grid-template-columns: repeat(auto-fit, minmax(270px, 1fr));
    gap: 28px;
    margin-top: 20px;
}

/* Styling for each anime card */
.anime-card {
    position: relative;
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

/* .anime-card:hover {
    transform: scale(1.02);
} */

.remove-button {
    position: absolute;
    top: 4px;
    right: 4px;
    background-color: #6004d8;
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
    border: #d6d6d6 2px solid;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);
}

.remove-button:hover {
    background-color: #eb2d26;
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
