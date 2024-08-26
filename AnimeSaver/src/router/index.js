import { createRouter, createWebHistory } from "vue-router";
import AnimeSearch from "../components/AnimeSearch.vue";
import Login from "../components/Login.vue";
import Register from "@/components/Register.vue";

const routes = [
  { path: "/", component: AnimeSearch },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
