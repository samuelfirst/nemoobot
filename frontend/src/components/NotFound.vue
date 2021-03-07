<template>
  <div class="container mt-3 text-center">
    <h1>Oops, it looks like the page you're looking for doesn't exist.</h1>
    <router-link to="/" class="text-light">Back home.</router-link>
  </div>
</template>

<script>
export default {
  name: 'NotFound',
}
</script>