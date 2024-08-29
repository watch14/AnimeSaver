<template>
    <header class="header">
        <div class="logo">
            <router-link to="/">
                <h1>AnimeSaver</h1>
            </router-link>
        </div>
        <div class="search-bar">
            <input v-model="searchQuery" @keyup.enter="searchAnime" placeholder="Search for anime..."
                class="search-input" />
            <button @click="searchAnime" class="search-button">Search</button>
        </div>
        <nav>
            <!-- Conditional rendering based on login status -->
            <span v-if="loggedIn" class="username">Hello, {{ username }}</span>
            <router-link v-if="loggedIn" to="/">Home</router-link>
            <router-link v-if="loggedIn" to="/top-anime">Top Anime</router-link>
            <router-link v-if="loggedIn" to="/seasonal-anime">Seasonal Anime</router-link>
            <router-link v-if="loggedIn" to="/saved-anime">Saved Anime</router-link>
            <router-link v-if="!loggedIn" to="/login">Login</router-link>
            <router-link v-if="!loggedIn" to="/register">Register</router-link>
            <router-link v-if="loggedIn" to="/profile">Profile</router-link>
            <button v-if="loggedIn" @click="handleLogout">Logout</button>
        </nav>

    </header>
</template>

<script>
import auth from '../utils/auth.js'; // Adjust the import path based on your file structure

export default {
    name: 'Header',
    props: {
        loggedIn: {
            type: Boolean,
            required: true
        },
        username: {
            type: String,
            default: ''
        }
    },
    data() {
        return {
            searchQuery: ''
        };
    },
    methods: {
        async handleLogout() {
            await auth.logout();
            this.$emit('logout');
            this.$router.push('/'); // Redirect to home page
        },
        searchAnime() {
            if (this.searchQuery.trim()) {
                this.$router.push({ name: 'SearchResults', query: { q: this.searchQuery } });
            }
        }
    }
};
</script>

<style scoped>
.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 20px;
    background-color: #5b22b6;
}

.logo h1 {
    margin: 0;
    color: white;
    font-weight: 700;
}

nav a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
}

nav a:hover {
    text-decoration: underline;
}

button {
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    font-size: 16px;
}

button:hover {
    text-decoration: underline;
}

.username {
    color: rgb(192, 192, 192);
    margin: 0 10px;
}

/* Search bar styling */
.search-bar {
    display: flex;
    align-items: center;
}

.search-input {
    padding: 10px;
    font-size: 1em;
    border: none;
    border-radius: 8px 0 0 8px;
    outline: none;
    width: 200px;
}

.search-button {
    padding: 10px 20px;
    font-size: 1em;
    background-color: #5b22b6;
    color: white;
    border-radius: 0 8px 8px 0;
    cursor: pointer;
    transition: background-color 0.3s ease;
    border: none;
    box-shadow: inset 0 0 0 2px white;
    margin: 0;
}

.search-button:hover {
    background-color: #411d7a;
}
</style>
