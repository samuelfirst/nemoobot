<template>
  <div class="container mt-3 text-center">
    <h2 v-if="this.$store.getters['auth/loggedIn']">Hello, {{ this.$store.state.auth.username }}!<br><a href="https://id.twitch.tv/oauth2/authorize?client_id=cj6u5ko0kn9bpdgajxrbz5ircahgff&redirect_uri=http://localhost:8000/connect_to_twitch&response_type=code&scope=user:edit+user:read:email+chat:edit+chat:read+channel:moderate+user:edit:broadcast&force_verify=true" class="text-white">Connect</a> to your Twitch to start using nemoobot.</h2>
    <h2 v-else>Welcome!<br>Please <a href="/login" class="text-white">login</a> or <a href="/signup" class="text-white">sign up</a>!</h2>
  </div>
</template>

<script>

export default {
  name: 'Home',
  data() {},
  methods: {}
}
</script>