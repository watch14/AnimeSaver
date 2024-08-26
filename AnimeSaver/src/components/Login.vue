<template>
    <div class="login-container">
        <h1>Login</h1>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="username">Email:</label>
                <input type="text" id="username" v-model="email" required /> <!-- Changed 'username' to 'email' -->
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <button type="submit">Login</button>
        </form>
    </div>
</template>


<script>
import axios from 'axios';

// Set the base URL for axios
axios.defaults.baseURL = 'http://localhost:5000';

export default {
    data() {
        return {
            email: '',
            password: ''
        };
    },
    methods: {
        async handleLogin() {
            try {
                const response = await axios.post('/login', {
                    userEmail: this.email,
                    userPassword: this.password
                });

                if (response.status === 200) {
                    const userId = response.data.userId;
                    console.log('User ID:', userId);
                    // Save userId to localStorage
                    localStorage.setItem('userId', userId);
                    // Optionally, redirect to another page or update UI
                } else {
                    console.error('Login failed:', response.data.message);
                }
            } catch (error) {
                if (error.response) {
                    console.error('Response error:', error.response.data.message || error.message);
                } else if (error.request) {
                    console.error('Request error:', error.request);
                } else {
                    console.error('Setup error:', error.message);
                }
            }
        }
    }
};
</script>

<style scoped>
form {
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    gap: 10px;
    width: 100%;
}

.form-group {
    width: 100%;
    display: flex;
    flex-direction: column;
    gap: 10px;
    margin-bottom: 20px;
}

.login-container {
    max-width: 400px;
    width: 100%;
    margin: 0 auto;
    padding: 20px;
    background-color: #f7f7f7;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);


}

h1 {
    text-align: center;
    margin-bottom: 20px;
}


input {
    width: 100%;
    padding: 10px 0;
    border: 1px solid #ddd;
    border-radius: 4px;
}

button {
    width: 100%;
    padding: 10px;
    background-color: #5b22b6;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
}

button:hover {
    background-color: #411d7a;
}

;
</style>;