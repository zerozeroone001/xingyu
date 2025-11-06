import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import pinia from './store';

const app = createApp(App);

// 使用 Router
app.use(router);

// 使用 Pinia
app.use(pinia);

app.mount('#app');
