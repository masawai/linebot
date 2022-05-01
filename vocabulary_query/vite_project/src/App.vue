<script setup>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://v3.vuejs.org/api/sfc-script-setup.html#sfc-script-setup
// import HelloWorld from './components/HelloWorld.vue'

import { ref, reactive } from 'vue';

const data = ref(0);
const index = ref(0);
const isStarted = ref(false);
const isAnswered = ref(false);

const url = import.meta.env.VITE_API_URL;

async function resJson () {
  const res = await window.fetch(url);
  const res_data = await res.json();
  data.value = res_data;
  console.log(data);
}

resJson();

const shuffle = ([...array]) => {
  for (let i = array.length - 1; i >= 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

const previousButton = () => {
  isAnswered.value = false;
  index.value -= 1;
  console.log(isAnswered);
};

const nextButton = () => {
  isAnswered.value = false;
  index.value += 1;
  console.log(isAnswered);
};

const answerButton = () => {
  isAnswered.value = true;
  console.log(isAnswered);
};
</script>

<template>
  <v-btn block @click="isStarted=true" v-show="!isStarted" >開始</v-btn><br><br>
  <v-btn @click="data=shuffle(data)" v-show="!isStarted" >シャッフル</v-btn>
  
  <div v-if="isStarted">
    <v-btn @click="previousButton()" v-bind:disabled="!index" >前の問題</v-btn>
    <v-btn @click="nextButton()" v-if="isAnswered" >次の問題</v-btn>
    <v-btn @click="answerButton()" v-else >答え</v-btn>
    <br><br>
    <p>{{ data[index].Word }}</p><br>
    <p v-show="isAnswered">{{ data[index].Japanese }}</p>
  </div>

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
</style>