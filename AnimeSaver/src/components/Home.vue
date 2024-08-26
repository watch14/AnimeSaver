<template>
    <div class="search-container">
        <h1>Search</h1>
        <div class="search-bar">
            <input v-model="query" @keyup.enter="searchAnime" placeholder="Search for anime..." class="search-input" />
            <button @click="searchAnime" class="search-button">Search</button>
        </div>
    </div>
</template>

<script>
export default {
    data() {
        return {
            query: ''
        };
    },
    methods: {
        searchAnime() {
            if (this.query.trim()) {
                this.$router.push({ name: 'SearchResults', query: { q: this.query } });
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
</style>
