<template>
    <div id="app">
        <Login></Login>
    </div>
</template>

<script>
import Login from './components/Login.vue';

export default {
  name: 'App',
  components: {
    Login
  },
}
</script>

<style>
html, body {
  margin: 0;
  padding: 0;
  font-family: Avenir, Helvetica, Arial, sans-serif;
}
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: left;
  color: #2c3e50;
  width: 100vw;
  min-width: 300px;
  max-width: 1000px;
  margin: 0 auto;
}
</style>
