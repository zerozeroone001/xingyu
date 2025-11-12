<template>
  <div class="app">
    <header class="header">
      <h1>星语诗词平台</h1>
      <nav class="nav">
        <button @click="currentView = 'home'" :class="{ active: currentView === 'home' }">首页</button>
        <button @click="currentView = 'poetry'" :class="{ active: currentView === 'poetry' }">诗词</button>
        <button @click="currentView = 'profile'" :class="{ active: currentView === 'profile' }">我的</button>
      </nav>
    </header>

    <main class="main">
      <HomePage v-if="currentView === 'home'" />
      <PoetryPage v-else-if="currentView === 'poetry'" />
      <ProfilePage v-else-if="currentView === 'profile'" />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import HomePage from './pages/HomePage.vue'
import PoetryPage from './pages/PoetryPage.vue'
import ProfilePage from './pages/ProfilePage.vue'

const currentView = ref('home')
</script>

<style scoped>
.app {
  min-height: 100vh;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.header {
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(10px);
  padding: 1rem 2rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.header h1 {
  margin: 0 0 1rem 0;
  color: #2c3e50;
  font-size: 2rem;
}

.nav {
  display: flex;
  gap: 1rem;
}

.nav button {
  padding: 0.5rem 1.5rem;
  border: none;
  background: transparent;
  color: #666;
  cursor: pointer;
  font-size: 1rem;
  border-radius: 8px;
  transition: all 0.3s;
}

.nav button:hover {
  background: rgba(26, 115, 232, 0.1);
  color: #1a73e8;
}

.nav button.active {
  background: #1a73e8;
  color: white;
}

.main {
  padding: 2rem;
}
</style>
