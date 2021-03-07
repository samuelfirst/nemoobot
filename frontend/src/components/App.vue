<template>
    <a href="" class="text-light" style="margin: 90%;" v-on:click="logout" v-if="this.$store.getters['auth/loggedIn']">Logout</a>
    <router-view />
</template>

<script>
export default {
  name: 'App',
  methods: {
    logout: function () {
        this.$store.dispatch('auth/logoutUser')
        .then(() => {
          this.$router.push('/login')
        })
    }
  }
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
  width: 100vw;
  min-width: 300px;
  max-width: 1000px;
  margin: 0 auto;
}
</style>
