# AnimeSaver App

## Overview

This Vue.js application displays detailed information about anime, including ratings, episodes, genres, and synopses. Users can add or remove anime from their personal list and mark them as watched or unwatched.

## Features

- Display anime details including image, rating, episodes, genres, status, and synopsis.
- Add or remove anime from the user's list.
- Mark anime as watched or unwatched.
- Responsive and user-friendly interface.

## Technologies Used

- **Vue.js**: JavaScript framework for building user interfaces.
- **Axios**: For making HTTP requests (if needed).
- **CSS**: For styling the application.
- **Local API**: For fetching anime details and user data.

## Setup and Installation

### Prerequisites

- Node.js (v14 or later) installed on your machine.
- npm (Node Package Manager) or yarn for managing dependencies.

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/anime-detail-app.git
   ```

2. **Navigate into the project directory:**

   ```bash
   cd anime-detail-app
   ```

3. **Install the dependencies:**

   ```bash
   npm install
   ```

   or, if you prefer yarn:

   ```bash
   yarn install
   ```

4. **Set up environment variables:**

   Create a `.env` file in the root of the project and add your environment variables. Example:

   ```plaintext
   VUE_APP_API_URL=http://localhost:5000/api
   ```

5. **Run the development server:**

   ```bash
   npm run dev
   ```

   or, if you prefer yarn:

   ```bash
   yarn dev
   ```

6. **Open your browser and go to:**

   ```
   http://localhost:5173
   ```

## Usage

1. **View Anime Details:** Navigate to the anime detail page to view detailed information about the selected anime.

2. **Add/Remove Anime:** Click the "Add to List" or "Remove from List" button to manage the anime in your personal list.

3. **Mark as Watched/Unwatched:** Click the "Watched" or "Unwatched" button to toggle the watched status of the anime.

## API Endpoints

- **GET /api/anime/:id**: Fetch detailed information about a specific anime.
- **POST /api/user/anime/:id**: Add an anime to the user's list.
- **DELETE /api/user/anime/:id**: Remove an anime from the user's list.
- **PATCH /api/user/anime/:id**: Update the watched status of an anime.

## Contributing

We welcome contributions to improve the app! If you'd like to contribute, please follow these steps:

1. **Fork the repository** on GitHub.
2. **Create a new branch** for your feature or fix.
3. **Make your changes** and commit them with descriptive messages.
4. **Push your changes** to your forked repository.
5. **Open a pull request** to the main repository.

## Contact

For any questions or issues, please contact:

- **Email:** chebbimaamoun@gmail.com
- **GitHub:** [watch14](https://github.com/watch14)

---

Thank you for using the AnimeSaver App! We hope you find it useful and enjoyable.
