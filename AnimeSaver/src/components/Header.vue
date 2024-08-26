<template>
    <header class="header">
        <div class="logo">
            <h1>Anime Finder</h1>
        </div>
        <nav>
            <router-link to="/">Home</router-link>
            <router-link to="/login">Login</router-link>
        </nav>
    </header>
</template>

<script>
export default {
    name: 'Header'
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
</style>