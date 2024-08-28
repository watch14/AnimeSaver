<template>
    <div class="register-container">
        <h1>Register</h1>
        <form @submit.prevent="handleRegister">
            <div class="form-group">
                <label for="email">Email:</label>
                <input type="email" id="email" v-model="email" required />
            </div>
            <div class="form-group">
                <label for="username">Username:</label>
                <input type="text" id="username" v-model="username" required />
            </div>
            <div class="form-group">
                <label for="password">Password:</label>
                <input type="password" id="password" v-model="password" required />
            </div>
            <div class="form-group">
                <label for="confirmPassword">Confirm Password:</label>
                <input type="password" id="confirmPassword" v-model="confirmPassword" required />
            </div>

            <button type="submit">Register</button>
        </form>
    </div>
</template>

<script>
import axios from 'axios';

axios.defaults.baseURL = 'http://localhost:5000';

export default {
    data() {
        return {
            email: '',
            username: '',
            password: '',
            confirmPassword: '',
            isAdmin: false
        };
    },
    methods: {
        async handleRegister() {
            if (this.password !== this.confirmPassword) {
                alert('Passwords do not match!');
                return;
            }

            try {
                const response = await axios.post('/register', {
                    userEmail: this.email,
                    userName: this.username,
                    userPassword: this.password,
                    isAdmin: this.isAdmin
                });

                if (response.status === 200) {
                    alert('Registration successful!');
                    // Redirect to login page or another page after successful registration
                    this.$router.push('/login');
                } else {
                    alert('Registration failed: ' + response.data.message);
                }
            } catch (error) {
                if (error.response) {
                    alert('Registration failed: ' + (error.response.data.message || error.message));
                } else if (error.request) {
                    alert('Registration failed: No response from server.');
                } else {
                    alert('Registration failed: ' + error.message);
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

.register-container {
    max-width: 400px;
    width: 100%;
    margin: auto;
    padding: 20px;
    background-color: #f7f7f7;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

h1 {
    text-align: center;
    margin-bottom: 20px;
}

input[type="email"],
input[type="text"],
input[type="password"] {
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 16px;

}

button {
    width: 100%;
    padding: 10px;
    font-size: 16px;

    background-color: #5b22b6;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
}

button:hover {
    background-color: #411d7a;
}
</style>
