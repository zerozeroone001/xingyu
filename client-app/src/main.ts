import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import pinia from './store';
// 导入 uni-app API 兼容层
import '@/utils/uni-shim';

const app = createApp(App);

// 将 router 存储到 window 上，供 uni-shim 使用
(window as any).__APP_ROUTER__ = router;

// 使用 Router
app.use(router);

// 使用 Pinia
app.use(pinia);

app.mount('#app');
