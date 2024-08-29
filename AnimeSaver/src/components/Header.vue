<template>
    <header class="header">
        <div class="logo">
            <router-link to="/">
                <h1>AnimeSaver</h1>
            </router-link>
        </div>
        <nav>
            <!-- Conditional rendering based on login status -->
            <span v-if="loggedIn" class="username">Hello, {{ username }}</span>
            <router-link v-if="loggedIn" to="/top-anime">Top Anime</router-link>
            <router-link v-if="loggedIn" to="/saved-anime">Saved Anime</router-link>
            <router-link v-if="!loggedIn" to="/login">Login</router-link>
            <router-link v-if="!loggedIn" to="/register">Register</router-link>
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
    methods: {
        async handleLogout() {
            await auth.logout();
            this.$emit('logout');
            this.$router.push('/'); // Redirect to home page
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
</style>