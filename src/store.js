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
      //axios.get('_api/allurls')
      axios.get('http://spectre:8000/_api/allurls')
        .then(r => r.data)
        .then(urls => {
          commit('SET_URLS', urls)
        })
    }

  }
})
