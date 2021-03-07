import { createStore } from 'vuex'
import authentication from './modules/authentication'

export default createStore({
  modules: {
    auth: authentication
  },
})