import { createRouter, createWebHistory } from "vue-router";
import AnimeSearch from "../components/AnimeSearch.vue";
import Login from "../components/Login.vue";

const routes = [
  { path: "/", component: AnimeSearch },
  { path: "/login", component: Login },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
