import axios from "axios";

axios.defaults.baseURL = "http://localhost:5000";

const auth = {
  /**
   * Check if the user is logged in by verifying the userId in localStorage
   * and validating it against the server.
   * @returns {Promise<boolean>} - Returns a promise that resolves to true if the user is logged in, false otherwise.
   */
  async isLoggedIn() {
    const userId = localStorage.getItem("userId");

    if (!userId) {
      return false;
    }

    try {
      const response = await axios.get(`/user/${userId}`);
      return response.status === 200 && response.data._id === userId;
    } catch (error) {
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

  /**
   * Add an anime to the user's saved list.
   * @param {string} animeId - The ID of the anime to add.
   * @returns {Promise<void>} - Returns a promise that resolves when the anime is added or if the user is prompted to log in.
   */
  async addAnimeToUserList(animeId) {
    const loggedIn = await this.isLoggedIn();

    if (!loggedIn) {
      alert("Please log in to add an anime to your list.");
      return;
    }

    const userId = localStorage.getItem("userId");

    try {
      await axios.post(`/user/${userId}/add_anime`, {
        anime_id: animeId,
        watched: false,
      });
      console.log(`Anime with ID ${animeId} added to the user's list.`);
    } catch (error) {
      console.error("Error adding anime to the user's list:", error);
    }
  },

  /**
   * Remove an anime from the user's saved list.
   * @param {string} animeId - The ID of the anime to remove.
   * @returns {Promise<void>} - Returns a promise that resolves when the anime is removed or if the user is prompted to log in.
   */
  async removeAnimeFromUserList(animeId) {
    const loggedIn = await this.isLoggedIn();

    if (!loggedIn) {
      alert("Please log in to remove an anime from your list.");
      return;
    }

    const userId = localStorage.getItem("userId");

    try {
      await axios.delete(`/user/${userId}/remove_anime`, {
        data: {
          anime_id: animeId,
        },
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
      });
      console.log(`Anime with ID ${animeId} removed from the user's list.`);
    } catch (error) {
      console.error("Error removing anime from the user's list:", error);
    }
  },

  /**
   * Fetch and print the user's data by their ID.
   * @param {string} id - The ID of the user to fetch.
   * @returns {Promise<void>} - Returns a promise that resolves when the user data is fetched and printed.
   */
  async getUserById(id) {
    if (!id) {
      console.error("No user ID provided.");
      return;
    }

    try {
      const response = await axios.get(`/user/${id}`);

      if (response.status === 200) {
        console.log("User data:", response.data);
      } else {
        console.log("Failed to fetch user data. Status code:", response.status);
      }
    } catch (error) {
      console.error("Error fetching user data:", error);
    }
  },

  /**
   * Fetch the list of anime IDs saved by the user.
   * @returns {Promise<string[]>} - Returns a promise that resolves to an array of anime IDs.
   */
  async getUserAnimeList() {
    const loggedIn = await this.isLoggedIn();

    if (!loggedIn) {
      alert("Please log in to view your anime list.");
      return [];
    }

    const userId = localStorage.getItem("userId");

    try {
      const response = await axios.get(`/user/${userId}`);
      console.log("User anime list:", response.data.savedList);
      return response.data.savedList || [];
    } catch (error) {
      console.error("Error fetching user anime list:", error);
      return [];
    }
  },

  /**
   * Update the watched status of an anime for the logged-in user.
   * @param {string} animeId - The ID of the anime to update.
   * @param {boolean} watchedStatus - The new watched status.
   * @returns {Promise<void>} - Returns a promise that resolves when the status is updated.
   */
  async updateAnimeWatchedStatus(animeId, watchedStatus) {
    const loggedIn = await this.isLoggedIn();

    if (!loggedIn) {
      alert("Please log in to update the watched status.");
      return;
    }

    const userId = localStorage.getItem("userId");

    try {
      const response = await axios.put(
        `/user/${userId}/update_anime`,
        {
          anime_id: animeId,
          watched: watchedStatus,
        },
        {
          headers: {
            Accept: "application/json",
            "Content-Type": "application/json",
          },
        }
      );

      if (response.status === 200) {
        console.log(
          `Anime with ID ${animeId} updated to watched status: ${watchedStatus}`
        );
      } else {
        console.error(`Unexpected status code: ${response.status}`);
        alert("Unexpected response from the server. Please try again.");
      }
    } catch (error) {
      console.error(
        "Error updating watched status:",
        error.response ? error.response.data : error.message
      );
      alert("Error updating watched status. Please try again.");
    }
  },
};

export default auth;
