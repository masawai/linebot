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
};

const userFilter = (data, user) => {
  let filtered_data = [];
  console.log(data);
  data.forEach((d) => {
    if (user == d.User){
      filtered_data.push(d);
  }});
  return filtered_data;
};

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

document.addEventListener('keydown', keydown_ivent);
function keydown_ivent(e) {
	switch (e.key) {
		case 'ArrowLeft':
			previousButton();
			break;
		case 'ArrowRight':
		  isAnswered.value == true ? nextButton():
		  answerButton();
			break;
	}
}
</script>

<template>
  <button block @click="isStarted=true" v-show="!isStarted" v-bind:disabled="!data">開始</button><br><br>
  <button @click="data=shuffle(data)" v-show="!isStarted" v-bind:disabled="!data">シャッフル</button>
  <button @click="data=userFilter(data, 'Masaya')" v-show="!isStarted" v-bind:disabled="!data">Masaya のデータでフィルタ</button>
  <button @click="data=userFilter(data, 'Mayu')" v-show="!isStarted" v-bind:disabled="!data">Mayu のデータでフィルタ</button>
  
  <div v-if="isStarted">
    <button @click="previousButton()" v-bind:disabled="!index" >前の問題</button>
    <button @click="nextButton()" v-if="isAnswered" >次の問題</button>
    <button @click="answerButton()" v-else >答え</button>
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