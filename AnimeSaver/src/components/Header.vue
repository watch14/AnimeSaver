<template>
    <header class="header">
        <div class="logo">

            <router-link to="/">
                <h1>AnimeSaver</h1>
            </router-link>
        </div>
        <nav>
            <!-- Conditional rendering based on login status -->
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
    data() {
        return {
            loggedIn: false
        };
    },
    async created() {
        // Check if the user is logged in when the component is created
        this.loggedIn = await auth.isLoggedIn();
    },
    methods: {
        async handleLogout() {
            await auth.logout();
            this.loggedIn = false;
            // Optionally, redirect to home or login page
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
</style>
