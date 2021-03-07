<template>
    <div class="container text-center mt-3">
    <h2 >Log in to nemoobot</h2>
    <form @submit.prevent='login'>
      <div class="col-xs-3 mb-3">
        <input type="text" class="form-control w-50 m-auto mt-1 text-center" v-model="username" autofocus="" autocapitalize="none" autocomplete="username" maxlength="150" required placeholder="Username">
      </div>
      <div class="col-12 mb-3">
        <input class="form-control w-50 m-auto mt-1 text-center" type="password" v-model="password" autocomplete="current-password" required placeholder="Password">
      </div>
      <div class="col-12">
        <button type="button" v-on:click="this.$router.push('/')"  class="btn btn-light mb-4 mx-1">Back</button>
        <button type="submit" class="btn btn-light mb-4 mx-1">Login</button>
      </div>
      <p class="px-2">
        New to nemoobot?
        <a href="/signup" class="text-light">Sign up</a>
      </p>
      <p class="px-2">
        <a href="/reset_pass" class="text-light">Forgot your password?</a>
      </p>
    </form>
  </div>
</template>

<script>
export default {
    name: "Login",
    data() {
        return {
            username: "",
            password: ""
        }
    },
    methods: {
        login: async function () {
            await this.$store.dispatch("auth/loginUser", {
                username: this.username,
                password: this.password
            })
            .then(() => this.$router.push('/'))
            .catch(err => console.log(err))
        }
    }
}
</script>