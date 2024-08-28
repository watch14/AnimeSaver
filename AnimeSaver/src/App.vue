<template>
  <div id="app">
    <Header :loggedIn="isAuthenticated" :username="username" @logout="handleLogout" />
    <div class="container">
      <router-view @login="handleLogin" />
    </div>
    <Footer /> <!-- Add the Footer component here -->
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue'; // Import Footer component
import auth from '@/utils/auth'; // Import the auth module

export default {
  name: 'App',
  components: {
    Header,
    Footer
  },
  data() {
    return {
      isAuthenticated: false,
      username: ''
    };
  },
  methods: {
    async handleLogin() {
      this.isAuthenticated = await auth.isLoggedIn();
      if (this.isAuthenticated) {
        const userData = await auth.getUserById(localStorage.getItem('userId'));
        this.username = userData.userName; // Assume userData contains a userName field
      }
    },
    async handleLogout() {
      await auth.logout();
      this.isAuthenticated = false;
      this.username = '';
      this.$router.push('/login'); // Redirect to login page or homepage
    }
  },
  async created() {
    this.isAuthenticated = await auth.isLoggedIn();
    if (this.isAuthenticated) {
      const userData = await auth.getUserById(localStorage.getItem('userId'));
      this.username = userData.userName; // Assume userData contains a userName field
    }
  }
};
</script>


<style>
/* Full-page container for centering */
#app {
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  /* Push the footer to the bottom */
  min-height: 100vh;
  margin: 0;
  background-color: #131212;
}

/* Centered container styling */
.container {
  width: 100%;
  margin-inline: auto;
  /* Optional: Add padding to the container */
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

* {
  font-family: Helvetica, sans-serif;
}
</style>
