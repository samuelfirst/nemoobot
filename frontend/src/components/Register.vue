<template>
    <div class="container text-light text-center mt-2">
      <h2>Sign up</h2>
      <form class="mb-3 row" @submit.prevent='register'>
        <div class="col-12 mb-2">
          <input type="text" v-model="username" class="form-control w-50 m-auto mt-1 text-center"  required placeholder="username"/>
        </div>
        <div class="col-12 mb-2">
          <input type="email" v-model="email" class="form-control w-50 m-auto mt-1 text-center" required placeholder="name@example.com"/>
        </div>
        <div class="col-12 mb-2">
          <input class="form-control w-50 m-auto mt-1 text-center" type="password" v-model="password1" autocomplete="new-password" required placeholder="Password"/>
        </div>
        <div class="col-12 mb-2">
          <input class="form-control w-50 m-auto mt-1 text-center" type="password" v-model="password2" autocomplete="new-password" required placeholder="Confirm password"/>
        </div>
        <div class="col-12 mb-2">
          <button type="button" v-on:click="this.$router.push('/')"  class="btn btn-light mx-1 mb-2">Back</button>
          <button type="button" v-on:click="this.$router.push('/login')"  class="btn btn-light mx-1 mb-2">Login</button>
          <button type="submit" class="btn btn-light mx-1 mb-2">Sign up</button>
        </div>
      </form>
    </div>
</template>

<script>
export default {
    name: "Register",
    data () {
        return {
            username: "",
            email: "",
            password1: "",
            password2: ""
        }
    },
    methods: {
        register: function () {
            this.$store.dispatch('auth/registerUser', {
                username: this.username,
                email: this.email,
                password: this.password1
            }).then(() => this.$store.dispatch('auth/loginUser', {
                username: this.username,
                password: this.password1
            })).then(() => this.$router.push('/'))
        }
    },
}
</script>