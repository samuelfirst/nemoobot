<template>
    <div>
        <form class="mb-3 row" @submit.prevent="login">
            <h1>Sign in</h1>
            <label>Username: </label>
            <input class="form-control" required v-model="username" type="text" placeholder="Username"/>
            <label>Password: </label>
            <input class="form-control" required v-model="password" type="password" placeholder="Password"/>
            <hr/>
            <button type="submit" class="btn btn-dark">Login</button>
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
            console.log(this.$store.state.auth.accessToken)
            await this.$store.dispatch("auth/loginUser", {
                username: this.username,
                password: this.password
            })
//            .then(() => this.$router.push('/'))
//            .catch(err => console.log(err))
        }
    }
}
</script>