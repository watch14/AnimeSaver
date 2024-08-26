<template>
    <div class="anime-detail-container">
        <div class="anime-image-left">
            <img :src="anime.main_picture?.large" alt="Anime image" class="anime-image" />
        </div>
        <div class="anime-info-right">
            <h1 class="anime-title">{{ anime.title }}</h1>
            <p class="anime-detail-text"><strong>Rating:</strong> {{ anime.mean ? anime.mean.toFixed(1) : 'N/A' }} / 10
            </p>
            <p class="anime-detail-text"><strong>Episodes:</strong> {{ anime.num_episodes }}</p>
            <p class="anime-date-text">{{ formatDates(anime.start_date, anime.end_date) }}</p>

            <p class="anime-detail-text"><strong>Genres:</strong> {{ anime.genres?.map(genre => genre.name).join(', ')
                }}</p>
            <p class="anime-detail-text"><strong>Synopsis:</strong> {{ anime.synopsis || 'No synopsis available.' }}</p>
            <p class="anime-detail-text"><strong>Status:</strong> {{ formatStatus(anime.status) }}</p>
        </div>
    </div>
</template>

<script>
export default {
    props: {
        id: {
            type: String,
            required: true
        }
    },
    data() {
        return {
            anime: {}
        };
    },
    async created() {
        await this.fetchAnimeDetail();
    },
    methods: {
        async fetchAnimeDetail() {
            if (!this.id) {
                console.error("No anime ID provided.");
                return;
            }
            try {
                const response = await fetch(`http://localhost:5000/api/anime/${this.id}?fields=title,mean,num_episodes,genres,synopsis,start_date,end_date,status`);
                const data = await response.json();
                this.anime = data;
            } catch (error) {
                console.error("Error fetching anime detail:", error);
            }
        },
        formatDates(start, end) {
            if (!start || !end) return "Unknown";
            const startYear = new Date(start).getFullYear();
            const endYear = new Date(end).getFullYear();
            return `${startYear} - ${endYear}`;
        },
        formatStatus(status) {
            switch (status) {
                case 'finished_airing':
                    return 'Finished Airing';
                case 'currently_airing':
                    return 'Currently Airing';
                case 'not_yet_aired':
                    return 'Not Yet Aired';
                default:
                    return 'Unknown Status';
            }
        }
    }
};
</script>

<style scoped>
.anime-detail-container {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    gap: 20px;
    /* grid-template-columns: 1fr 2fr; */
    gap: 20px;
    padding: 60px;
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    max-width: 1440px;
    margin-inline: auto;
}



.anime-image {
    border-radius: 8px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    width: 100%;
}

.anime-date-text {
    color: white;
    font-size: 16px;
    font-weight: 500;
    margin: 0;
}

.anime-info-right {
    display: flex;
    flex-direction: column;
    gap: 20px;
    color: white;
    width: 100%;
    margin: 0;
}

.anime-title {
    font-size: 36px;
    font-weight: 600;
    margin: 0;

}

.anime-detail-text {
    font-size: 16px;
    line-height: 1.5;
    font-weight: 500;
    margin: 0;
    width: 100%;
}
</style>
