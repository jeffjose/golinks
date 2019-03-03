import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    urls: []
  },
  mutations: {
    SET_URLS(state, urls) {
      state.urls = urls
    }
  },
  actions: {
    loadURLs({
      commit
    }) {
      axios.get('http://localhost:8000/_api/allurls')
        .then(r => r.data)
        .then(urls => {
          console.log(urls)
          commit('SET_URLS', urls)
        })
    }

  }
})