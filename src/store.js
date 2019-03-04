import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

import _ from "lodash";

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
      axios.get('_api/allurls')
        //axios.get('http://spectre:8000/_api/allurls')
        .then(r => r.data)
        .then(urls => {
          urls.forEach(function (x) {

            x.shortlinkok = false
            x.shortlinkexists = false
            x.editMode = false
            x.origshortlink = x.shortlink
            x.origdestination = x.destination
            x.selected = false

          })
          commit('SET_URLS', urls)
        })
    },

    forceRefresh({
      commit
    }) {
      axios.get('_api/refresh')
        //axios.get('http://spectre:8000/_api/refresh')
        .then(r => r.data)
        .then(urls => {
          urls.forEach(function (x) {

            x.shortlinkok = false
            x.shortlinkexists = false
            x.editMode = false
            x.origshortlink = x.shortlink
            x.origdestination = x.destination
            x.selected = false

          })
          commit('SET_URLS', urls)
        })
    },

  },
})