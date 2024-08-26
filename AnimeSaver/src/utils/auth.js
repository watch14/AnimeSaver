import axios from "axios";

axios.defaults.baseURL = "http://localhost:5000";

const auth = {
  /**
   * Check if the user is logged in by verifying the userId in localStorage
   * and validating it against the server.
   * @returns {Promise<boolean>} - Returns a promise that resolves to true if the user is logged in, false otherwise.
   */
  async isLoggedIn() {
    // Get the userId from localStorage
    const userId = localStorage.getItem("userId");

    // If there's no userId in localStorage, the user is not logged in
    if (!userId) {
      return false;
    }

    try {
      // Make a GET request to check if the user exists in the database
      const response = await axios.get(`/user/${userId}`);

      // If the request is successful and the user exists, return true
      console.log("Login status:", response.data._id);
      return response.status === 200 && response.data._id === userId;
    } catch (error) {
      // If there was an error, log it and return false (user is not logged in)
      console.error("Error checking login status:", error);
      return false;
    }
  },

  /**
   * Log the user out by removing their userId from localStorage.
   */
  logout() {
    localStorage.removeItem("userId");
  },
};

export default auth;
