<template lang="pug">
  div
   div.buttonbar
     button.button.is-small
         i.mdi(@click="toggleselectall()", :class="{'mdi-checkbox-blank-outline': !selectall, 'mdi-checkbox-marked': selectall}")
     button.button.is-small.refreshing(@click="refreshing = true; reload()")
         i.mdi(:class="{'mdi-reload': !refreshing, 'mdi-progress-clock': refreshing}")
     button.button.is-small
         i.mdi.mdi-content-save
     button.button.is-small
         i.mdi.mdi-delete

   table.table.is-hoverable
     thead
       tr
         th
           span
         th
           span link
         th
           span URL
         th
           span creator
         th
           span hits
         th
           span created
         th
           span modified
         th
           span
     tbody
       tr
         th
         th
           p
             input.input.is-small(:class="{'is-danger': newurl.shortlinkexists, 'is-success': newurl.shortlinkok}" ref="shortlink", type="text", placeholder="shortlink", @input="newurl.shortlink = golink2shortlink($event.target.value, newurl)", :value="shortlink2golink(newurl.shortlink)", @keyup.enter="add(newurl)")
         th
           p.control.has-icons-left
             input.input.is-small(type="text", placeholder="URL to shorten", v-model="newurl.destination", @keyup.enter="add(newurl)")
             span.icon.is-small.is-left
               i.mdi.mdi-link
         th
           p.control.has-icons-left
             input.input.is-small(type="text", placeholder="User", v-model="newurl.creator", @keyup.enter="add(newurl)")
             span.icon.is-small.is-left
               i.mdi.mdi-account
         th
           p
             input.input.is-small(disabled, type="text", placeholder="0")
         th
           p.control.has-icons-left
             input.input.is-small(disabled, type="text", placeholder="right now")
             span.icon.is-small.is-left
               i.mdi.mdi-calendar-range
         th
           p.control.has-icons-left
             input.input.is-small(disabled, type="text", placeholder="right now")
             span.icon.is-small.is-left
               i.mdi.mdi-calendar-range
         th.icons
             span.icon(@click="add(newurl)", :class="{active: newurl.shortlinkok, inactive: !newurl.shortlinkok}")
               i.mdi.mdi-plus-circle.add
       tr(v-for="url in urls", :class="{'is-selected': url.selected}")
         td.selector
           //input.checkbox(v-model="url.selected", type="checkbox")
           span.icon(@click="url.selected = !url.selected")
             i.mdi(:class="{'mdi-checkbox-blank-outline': !url.selected, 'mdi-checkbox-marked': url.selected}")
         td.td-shortlink(@dblclick="url.editMode = true")
           div.shortlinkwrapper(v-if="!url.editMode")
             input.input-hidden(:ref="'input-' + url.shortlink", :value="'go/' + url.shortlink")
             span.golink(@click="copy(url.shortlink)")
               span.go go/
               span.shortlink {{url.shortlink}}
             span.icon.clipboard(@click="copy(url.shortlink)")
               i.mdi.mdi-clipboard-text
           input.input.is-small(v-if="url.editMode", :class="{'is-danger': url.shortlinkexists, 'is-success': url.shortlinkok}", :ref="'shortlink-' + url.shortlink", type="text", placeholder="shortlink", @input="url.shortlink = golink2shortlink($event.target.value, url)", :value="shortlink2golink(url.shortlink)", @keyup.enter="edit(url)")
         td.td-destination(@dblclick="url.editMode = true")
           span.destination(v-if="!url.editMode")  {{url.destination | shorten}}
           p.control.has-icons-left(v-if="url.editMode")
             input.input.is-small(type="text", v-model="url.destination", @keyup.enter="edit(url)", placeholder="URL to shorten")
             span.icon.is-small.is-left
               i.mdi.mdi-link
         td.td-creator
           span.creator {{url.creator}}
           //input.input.is-small(type="text", :value="url.creator")
         td.td-hits
           span.hits {{url.hits}}
           //span.hits(v-if="!url.editMode") {{url.hits}}
           //input.input.is-small(v-if="url.editMode", disabled, type="text", :value="url.hits")
         td.td-created
           span.created {{url.created | from_now}}
           //span.created(v-if="!url.editMode") {{url.created | from_now}}
           //input.input.is-small.is-info(v-if="url.editMode", disabled, type="text", :placeholder="url.created")
         td.td-modified
           span.modified {{url.modified | from_now}}
           //span.modified(v-if="!url.editMode") {{url.modified | from_now}}
           //input.input.is-small.is-info(v-if="url.editMode", disabled, type="text", placeholder="right now")
         td.icons.td-icons
           span.icon(@click="url.editMode = true")
             i.mdi.ed(:class="{'mdi-pencil': !url.editMode, 'mdi-content-save active': url.editMode}")
           span.icon(@click="del(url)")
             i.mdi.mdi-delete.del

</template>
<script>
import axios from "axios";
import moment from "moment";

import _ from "lodash";

export default {
  name: "LinkTable",
  mounted() {
  },
  data: function() {
    return {
      newurl: {shortlink: "", shortlinkexists: false, shortlinkok: false},
      selectall: false,
      refreshing:false
    };
  },
  props: {
    urls: Array
  },
  filters: {
    from_now: function(date) {
      return moment(date).fromNow();
    },
    shorten: function(url) {
      if(url.length > 30) {
        return url.substring(0,30) + "..."
      } else {
        return url
      }

    },},
  methods: {
    toggleselectall: function(){

      this.urls.forEach(function(x) {x.selected  = !x.selected})

      this.selectall = !this.selectall
    },
    focus: function(ref) {
      this.$refs[ref].focus()
    },
    shortlink2golink: function(shortlink) {
      if(shortlink.length == 0) {
        return "go/"
      }else {
      return "go/" + shortlink
      }
    },
    reload: function() {
      this.$store.dispatch("forceRefresh").then(response => {

        setTimeout( () => {
        this.refreshing = false

        }, 300)
      }

      )
    },
    edit: function(url) {


        axios
          .post("_api/edit/" + url.shortlink, url)
          //.post("http://spectre:8000/_api/edit/" + url.shortlink, url)
          .then(response => {
            this.$store.dispatch("loadURLs");
            url.editMode = false
          });

    },
    copy: function(val){
      this.$refs["input-"+val][0].select()
      document.execCommand('copy')
    },
    golink2shortlink: function(str, url){

      var shortlink =  str.replace(/^g/, '').replace(/^o/, '').replace(/^\//, '').replace(/ /, '-')


      if (shortlink.length > 0) {

      // If user is editing, its possible the user wants to go back to the origshortlink
      // in that case, dont validate because it'll be an error for sure (and that's not good)
      if (url.origshortlink == shortlink) {

              url.shortlinkexists = false
              url.shortlinkok = true


      }
      else {


        axios.get("_api/validate/" + shortlink)
        //axios.get("http://spectre:8000/_api/validate/" + shortlink)
          .then(r => r.data)
          .then(exists => {

              url.shortlinkexists = exists
              url.shortlinkok = !exists
          })

      }


      }
      else {
        // nothing is entered, show no colors
        url.shortlinkexists = false
        url.shortlinkok = false
      }

      return shortlink
    },
    add: function() {

      // If shortlink isnt unique
      if (!this.newurl.shortlinkok) {
        this.$refs.shortlink.select();
        this.$refs.shortlink.focus();

        return
      }

      // Only if these values are set
      if (
        _.has(this.newurl, "shortlink") &&
        _.has(this.newurl, "destination")
      ) {
        axios
          .post("_api/add/" + this.newurl.shortlink, this.newurl)
          //.post("http://spectre:8000/_api/add/" + this.newurl.shortlink, this.newurl)
          .then(response => {
            this.$store.dispatch("loadURLs");
            this.newurl= {shortlink: "", shortlinkexists: false, shortlinkok: false}
          });

        this.$refs.shortlink.focus();
      }
    },
    del: function(url) {
      axios
        .get("_api/delete/" + url.shortlink)
        .then(response => {
          this.$store.dispatch("loadURLs");
        });
    }
  }
};
</script>

<style scoped lang="sass">

@import "~bulma/sass/utilities/initial-variables";

table
  color: $grey-dark

th, .td-creator, .td-hits, .td-created, .td-modified, .td-icons
  text-align: center

table td
  vertical-align: middle
  padding-top: 0px;
  padding-bottom: 0px;

.go
  color: $grey-light
  font-size: 0.75rem

.is-selected .go
  color: $white

.shortlink
  font-weight: bold

.destination:hover
  cursor: pointer;

.ed, .del
  color: $grey-light
  transition: $speed ease-in-out;

.icons .active
  cursor: pointer
  color: $green !important

.icons .inactive
  cursor: default
  color: $grey-lighter !important

.del:hover
    color: $red !important
    cursor: pointer

.ed:hover
    color: $grey-dark !important
    cursor: pointer

.ed.active:hover
    color: $green !important
    cursor: pointer

.is-selected .ed, .is-selected .del
    color: $white;

thead tr span, tbody tr span
   font-size: 0.75rem;

.icons span
   font-size: 1rem;

// Increase the font size of only the plus button
.add
  font-size: 1.2rem

.clipboard
  opacity: 0
  transition: 50ms ease-in-out;
  color: $grey-light

.is-selected .clipboard
  color: $white

.clipboard:hover
    color: $grey-darker !important
    cursor: pointer

tr:hover .clipboard
   opacity: 1;

table
  cursor: default

.golink
  cursor: pointer

  // Make the input as small as possible, but still allowing for copying
.input-hidden
  width: 1px
  height: 1px
  border: 0px
  opacity: 0

.selector i
  color: $grey
  font-size: 1.3em
  cursor: pointer;

.selector i:hover
  color: $grey-darker

.is-selected .selector i
  color: $grey-darker

.shortlinkwrapper
    margin-top: -2px;

.buttonbar button
  border: 0
  color: $grey

.buttonbar button i
  font-size: 1.3em

.buttonbar button:hover
  background-color: $white-ter
  color: $grey-darker

.buttonbar button:focus, .buttonbar button:active
  outline: none
  box-shadow: none

.td-destination
  cursor: pointer

</style>

