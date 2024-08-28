<template>
    <div class="search-container">
        <h1>Search</h1>
        <div class="search-bar">
            <input v-model="query" @keyup.enter="searchAnime" placeholder="Search for anime..." class="search-input" />
            <button @click="searchAnime" class="search-button">Search</button>
        </div>

        <!-- Loader -->
        <div v-if="loading" class="loader">Searching...</div>

        <!-- Display results (optional) -->
        <!-- Add logic here to display search results if needed -->
    </div>
</template>

<script>
import { ref } from 'vue';

export default {
    data() {
        return {
            query: '',
            loading: ref(false) // Loading state
        };
    },
    methods: {
        async searchAnime() {
            if (this.query.trim()) {
                this.loading = true; // Show loader
                try {
                    // Perform the search and navigate
                    this.$router.push({ name: 'SearchResults', query: { q: this.query } });
                } catch (error) {
                    console.error('Search error:', error);
                } finally {
                    this.loading = false; // Hide loader
                }
            }
        }
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
    font-size: 1em;
    border: 1px solid #5b22b6;
    border-radius: 8px 0 0 8px;
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
