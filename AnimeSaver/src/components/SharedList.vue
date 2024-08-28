<template>
    <div class="anime-grid-container">
        <h1>Shared List</h1>

        <!-- Loader -->
        <div v-if="loading" class="loader">Loading...</div>

        <!-- Anime List -->
        <div v-if="!loading && animeList.length > 0" class="anime-grid">
            <div v-for="anime in animeList" :key="anime.id" class="anime-card">
                <img @click="goToAnimePage(anime.id)" :src="anime.main_picture?.large" alt="Anime image"
                    class="anime-image" />
                <div class="anime-details">
                    <h2 @click="goToAnimePage(anime.id)" class="anime-title">{{ anime.title }}</h2>
                    <div class="rating-container">
                        <p class="anime-rating-text">{{ anime.mean ? anime.mean.toFixed(1) : 'N/A' }} / 10</p>
                    </div>
                </div>
            </div>
        </div>
        <div v-else-if="!loading">
            <p>No anime found in the shared list.</p>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
    props: ['link_id'],
    setup(props) {
        const animeList = ref([]);
        const loading = ref(true); // Loading state
        const router = useRouter();

        onMounted(async () => {
            try {
                const response = await axios.get(`http://localhost:5000/api/shared-list/${props.link_id}`);
                animeList.value = response.data.animeList || [];
            } catch (error) {
                console.error('Error fetching shared list:', error);
                animeList.value = [];
            } finally {
                loading.value = false; // Hide loader
            }
        });

        const goToAnimePage = (animeId) => {
            router.push({ name: 'AnimeDetail', params: { id: animeId.toString() } });
            console.log('Go to anime page with ID:', animeId.toString());
        };

        return { animeList, loading, goToAnimePage };
    }
};
</script>

<style scoped>
.anime-grid-container {
    text-align: center;
    padding: 20px;
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
}

@keyframes spin {
    0% {
        transform: rotate(0deg);
    }

    100% {
        transform: rotate(360deg);
    }
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
}

.anime-card:hover {
    transform: scale(1.02);
}

.anime-image {
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
</style>
