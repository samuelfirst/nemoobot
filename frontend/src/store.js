import { createStore } from 'vuex'
import axios from 'axios'

const store = createStore({
  state() {
    return {
     accessToken: localStorage.getItem('access_token') || null, // makes sure the user is logged in even after
    // refreshing the page
     APIData: ''
    }
  },
  getters: {
    loggedIn (state) {
      return state.accessToken != null
    }
  },
  mutations: {
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
  },
  actions: {
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
  },
})

export default store