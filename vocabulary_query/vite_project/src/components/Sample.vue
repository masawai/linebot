<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
// import HelloWorld from './components/HelloWorld.vue'
import Hello from './components/Hello.vue';
const message = 'Hello World';
const link = 'https://google.com';
const isActive = true;
const users = [
  { id: 1, name: 'John Doe', email: 'john@test.com', admin: true },
  { id: 2, name: 'Jane Doe', email: 'jane@example.com', admin: false },
  { id: 3, name: 'Kevin MacDonald', email: 'kevin@test.com', admin: false },
];
const clickButton = (msg) => {
  console.log(msg);
};
</script>

<template>
  <!--<img alt="Vue logo" src="./assets/logo.png" />-->
  <HelloWorld msg="Hello Vue 3 + Vite" />
  <p>{{message}}</p>
  <p :class="{ active: isActive }">v-bindの設定方法の確認</p>
  <p v-for="user in users" :key="user">{{ user }}</p>
  <button @click="clickButton('クリック')">クリック</button>
  <Hello />
  <Hello />
</template>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
.active {
  color: red;
  font-weight: 900;
}
</style>
