import axios from 'axios'

const state = () => ({
     accessToken: localStorage.getItem('access_token') || null, // makes sure the user is logged in even after
    // refreshing the page
     APIData: ''
})

const getters = {
    loggedIn (state) {
      return state.accessToken != null
    }
}

const mutations = {
    updateLocalStorage (state, access) {
      localStorage.setItem('access_token', access)
      state.accessToken = access
    },
    updateAccess (state, access) {
      state.accessToken = access
    },
    destroyToken (state) {
      state.accessToken = null
    }
}

const actions = {
    async registerUser (context, data) {
      await axios.post('http://localhost:8000/api/v1/signup/', {
        username: data.username,
        email: data.email,
        password: data.password
      })
      .then(
        response => { console.log(response.data) }
      )
      .catch(
        error => {console.log(error.response.data)}
      )
    },
    async loginUser (context, data) {
      await axios.post('http://localhost:8000/api/v1/auth/token/', {
        username: data.username,
        password: data.password
      })
      .then(
        response => {
          context.commit('updateLocalStorage', response.data.token)
        }
      )
    }
}

export default {
  namespaced: true,
  state,
  getters,
  actions,
  mutations
}