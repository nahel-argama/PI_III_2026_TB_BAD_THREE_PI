import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';
import './globals.css';
import { capitalize, formatName } from './utils/string';

const app = createApp(App);

// Register global formatting helpers
app.config.globalProperties.capitalize = capitalize;
app.config.globalProperties.formatName = formatName;
app.config.globalProperties.$capitalize = capitalize;
app.config.globalProperties.$formatName = formatName;

app.use(createPinia());
app.use(router);

app.mount('#app');
