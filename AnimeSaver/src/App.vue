<template>
  <div id="app">
    <div class="container">
      <AnimeSearch />
    </div>
  </div>
</template>

<script>
import AnimeSearch from './components/AnimeSearch.vue';

export default {
  name: 'App',
  components: {
    AnimeSearch
  }
};
</script>

<style>
/* Full-page container for centering */
#app {
  width: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  margin: 0;
  margin-inline: auto;

}

/* Centered container styling */
.container {
  padding: 40px;
  width: 100%;
  max-width: 1200px;
  text-align: center;
}

/* Main heading style */
h1 {
  color: #5b22b6;
  margin-bottom: 20px;
  font-size: 2.5em;
  font-weight: 600;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

/* Improve readability for text */
body {
  margin: 0;
  padding: 0;
  color: #333;
  font-size: 16px;
}

/* Global styles for links */
a {
  color: #5b22b6;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
