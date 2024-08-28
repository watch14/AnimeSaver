<template>
    <div>
        <h1>Shared List</h1>
        <div v-if="animeList">
            <ul>
                <li v-for="anime in animeList" :key="anime.id">
                    {{ anime.title }}
                </li>
            </ul>
        </div>
        <div v-else>
            <p>Loading...</p>
        </div>
    </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import axios from 'axios';

export default {
    props: ['link_id'],
    setup(props) {
        const animeList = ref(null);

        onMounted(async () => {
            try {
                const response = await axios.get(`http://localhost:5000/api/shared-list/${props.link_id}`);
                animeList.value = response.data.animeList;
            } catch (error) {
                console.error('Error fetching shared list:', error);
            }
        });

        return { animeList };
    }
};
</script>