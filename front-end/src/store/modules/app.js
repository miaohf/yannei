const state = {
  barColor: 'rgba(50, 50, 50, .7), rgba(50, 50, 50, .7)',
  barImage: '',
  drawer: null,
}

const mutations = {
  SET_BAR_IMAGE(state, payload) {
    state.barImage = payload
  },
  SET_DRAWER(state, payload) {
    state.drawer = payload
  },
  SET_SCRIM(state, payload) {
    state.barColor = payload
  },
}

const actions = {}

export default {
  namespaced: true,
  state,
  mutations,
  actions,
}
