import { createApp } from "vue";
import { createPinia } from "pinia";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import { usePersistAuthStore } from "./plugins/authPersistStore";

const app = createApp(App);
const pinia = createPinia();
pinia.use(usePersistAuthStore);
app.use(router);
app.use(pinia);
app.mount("#app");
