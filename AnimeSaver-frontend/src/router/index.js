import { createRouter, createWebHistory } from "vue-router";
import Login from "../components/Login.vue";
import Register from "@/components/Register.vue";
import AnimeDetail from "@/components/AnimeDetail.vue";
import SearchResults from "@/components/SearchResults.vue";
import Home from "../components/Home.vue";
import SavedAnime from "@/components/SavedAnime.vue";
import SharedList from "@/components/SharedList.vue";
import TopAnime from "@/components/TopAnime.vue";
import SeasonalAnime from "@/components/SeasonalAnime.vue";
import Profile from "@/components/Profile.vue";

const routes = [
  { path: "/", component: Home },
  { path: "/login", component: Login },
  { path: "/register", component: Register },
  {
    path: "/search",
    name: "SearchResults",
    component: SearchResults,
  },
  {
    path: "/anime/:id",
    name: "AnimeDetail",
    component: AnimeDetail,
    props: true,
  },
  {
    path: "/saved-anime",
    name: "SavedAnime",
    component: SavedAnime,
    props: true,
  },
  {
    path: "/shared-list/:link_id",
    name: "SharedList",
    component: SharedList,
    props: true,
  },
  {
    path: "/top-anime",
    name: "ToipAnime",
    component: TopAnime,
    props: true,
  },
  {
    path: "/seasonal-anime",
    name: "SeasonalAnime",
    component: SeasonalAnime,
    props: true,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
