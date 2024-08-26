import { createRouter, createWebHistory } from "vue-router";
import AnimeSearch from "../components/AnimeSearch.vue";
import Login from "../components/Login.vue";
import Register from "@/components/Register.vue";
import AnimeDetail from "@/components/AnimeDetail.vue";

const routes = [
  { path: "/", component: AnimeSearch },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  {
    path: "/anime/:id",
    name: "AnimeDetail",
    component: AnimeDetail,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
