<template>
  <div id="app">
    <Header />
    <div class="container">
      <router-view />
    </div>
  </div>
</template>

<script>
import Header from './components/Header.vue'; // Import Header component

export default {
  name: 'App',
  components: {
    Header
  }
};
</script>

<style>
/* Full-page container for centering */
#app {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  min-height: 100vh;
  margin: 0;
  margin-inline: auto;

  background-color: #131212;
}

/* Centered container styling */
.container {
  width: 100vw;
  margin-inline: auto;
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
