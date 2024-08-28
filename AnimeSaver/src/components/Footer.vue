<template>
    <footer class="footer">
        <p>&copy; 2024 AnimeSaver. All rights reserved.</p>
        <nav>
            <router-link to="/">Home</router-link>
            <router-link to="/search">Search</router-link>
            <router-link to="/saved-anime">Saved Anime</router-link>
            <router-link to="/contact">Contact Us</router-link> <!-- Optional -->
        </nav>
    </footer>
</template>

<style scoped>
.footer {
    background-color: #5b22b6;
    color: white;
    padding: 20px 0;
    text-align: center;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 12px;
    /* Ensure the footer is not fixed and naturally flows with the content */
}

.footer p {
    margin: 0;
}

.footer nav {
    margin-top: 10px;
}

.footer nav a {
    color: white;
    text-decoration: none;
    margin: 0 10px;
}

.footer nav a:hover {
    text-decoration: underline;
}
</style>