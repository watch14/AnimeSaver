<template>
    <div v-if="loading" class="loader">Searching...</div>

    <div v-if="!loading" class="search-container">
        <h1>Welcome Home</h1>
        <p>Upcoming Anime</p>
        <UpcomingAnime :initialRankingType="'upcoming'" />

    </div>
</template>

<script>
// Import the Ranking component
import UpcomingAnime from './UpcomingAnime.vue';
export default {
    components: {
        UpcomingAnime // Register the Ranking component
    },
    data() {
        return {
            query: '',
            loading: false // Loading state
        };
    },
    methods: {
        // Add any necessary methods here
    }
};
</script>

<style scoped>
/* Styling for the search container */
.search-container {
    text-align: center;
    padding: 20px;
}

/* Styling for the search bar */
.search-bar {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 20px;
}

.search-input {
    padding: 10px;
    font-size: 16px;
    border: 1px solid #5b22b6;
    border-radius: none;
    outline: none;
    width: 300px;
}

.search-button {
    padding: 10px 20px;
    font-size: 1em;
    background-color: #5b22b6;
    color: white;
    border: none;
    border-radius: 0 8px 8px 0;
    cursor: pointer;
    transition: background-color 0.3s ease;
}

.search-button:hover {
    background-color: #411d7a;
}

/* Loader Styles */
.loader {
    margin-top: 20px;
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
