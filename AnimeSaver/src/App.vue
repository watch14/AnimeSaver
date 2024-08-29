<template>
  <div id="app">
    <Header :loggedIn="isAuthenticated" :username="username" @logout="handleLogout" />
    <div class="container">
      <router-view />
    </div>
    <Footer />
  </div>
</template>

<script>
import Header from './components/Header.vue';
import Footer from './components/Footer.vue';
import auth from '@/utils/auth';

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
        const userId = localStorage.getItem('userId');
        if (userId) {
          const userData = await auth.getUserById(userId);
          if (userData) {
            this.username = userData.userName;
          } else {
            console.error('User data not found.');
            this.username = 'Guest';
          }
        } else {
          console.error('No userId found in localStorage.');
        }
      }
    },
    async handleLogout() {
      await auth.logout();
      this.isAuthenticated = false;
      this.username = '';
      this.$router.push('/login');
    }
  },
  async created() {
    this.isAuthenticated = await auth.isLoggedIn();
    if (this.isAuthenticated) {
      const userId = localStorage.getItem('userId');
      if (userId) {
        const userData = await auth.getUserById(userId);
        if (userData) {
          this.username = userData.userName;
        } else {
          console.error('User data not found.');
          this.username = 'Guest';
        }
      } else {
        console.error('No userId found in localStorage.');
      }
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
  gap: 40px;
  min-height: 100vh;
  margin: 0;
  background-color: #131212;
}

/* Centered container styling */
.container {
  width: 100%;
  margin-inline: auto;
}

/* Main heading style */
h1 {
  margin: 0;
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
