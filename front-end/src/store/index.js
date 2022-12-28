import Vue from 'vue'
import Vuex from 'vuex'
import getters from './getters'

import createPersistedState from 'vuex-persistedstate'

Vue.use(Vuex)

// https://webpack.js.org/guides/dependency-management/#requirecontext
const modulesFiles = require.context('./modules', true, /\.js$/)

// you do not need `import app from './modules/app'`
// it will auto require all vuex module from modules file
const modules = modulesFiles.keys().reduce((modules, modulePath) => {
  // set './app.js' => 'app'
  const moduleName = modulePath.replace(/^\.\/(.*)\.\w+$/, '$1')
  const value = modulesFiles(modulePath)
  modules[moduleName] = value.default
  return modules
}, {})

const store = new Vuex.Store({
  modules,
  getters,
  state: {
    barColor: 'rgba(45, 45, 45, .8), rgba(45, 45, 45, .8)',
    barImage: '',
    drawer: false,
  },
  mutations: {
    SET_BAR_IMAGE(state, payload) {
      state.barImage = payload
    },
    SET_DRAWER(state, payload) {
      state.drawer = payload
    },
    SET_SCRIM(state, payload) {
      state.barColor = payload
    },
  },
  actions: {},
  plugins: [createPersistedState()],
})

export default store
