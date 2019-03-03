<template lang="pug">
   table.table.is-hoverable
     thead
       tr
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
           p
             input.input.is-small(:class="{'is-danger': shortlinkexists, 'is-success': shortlinkok}" ref="shortlink", type="text", placeholder="shortlink", @input="newurl.shortlink = golink2shortlink($event.target.value)", :value="golink", @keyup.enter="add_link(newurl)")
         th
           p.control.has-icons-left
             input.input.is-small(type="text", placeholder="URL to shorten", v-model="newurl.destination", @keyup.enter="add_link(newurl)")
             span.icon.is-small.is-left
               i.mdi.mdi-link
         th
           p.control.has-icons-left
             input.input.is-small(type="text", placeholder="User", v-model="newurl.creator", @keyup.enter="add_link(newurl)")
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
             span.icon(@click="add_link(newurl)", :class="{active: shortlinkok, inactive: !shortlinkok}")
               i.mdi.mdi-plus-circle.add
       tr(v-for="url in urls")
         td.td-shortlink
           input.input-hidden(:ref="'input-' + url.shortlink", :value="'go/' + url.shortlink")
           span.golink(@click="copy(url.shortlink)")
             span.go go/
             span.shortlink {{url.shortlink}}
           span.icon.clipboard(@click="copy(url.shortlink)")
             i.mdi.mdi-clipboard-text
         td.td-destination
           span.destination {{url.destination | shorten}}
         td.td-creator
           span.creator {{url.creator}}
         td.td-hits
           span.hits {{url.hits}}
         td.td-created
           span.created {{url.created | from_now}}
         td.td-modified
           span.modified {{url.modified | from_now}}
         td.icons.td-icons
           span.icon
             i.mdi.mdi-pencil.ed
           span.icon(@click="del_link(url)")
             i.mdi.mdi-delete.del

</template>
<script>
import axios from "axios";
import moment from "moment";

import _ from "lodash";

export default {
  name: "LinkTable",
  mounted() {
    this.$refs.shortlink.focus();
  },
  data: function() {
    return {
      newurl: {shortlink: ""},
      shortlinkexists: false,
      shortlinkok: false
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
  computed: {
    golink: function(){
      if(this.newurl.shortlink.length == 0) {
        return "go/"
      }else {
      return "go/" + this.newurl.shortlink
      }
    }
  },
  methods: {
    copy: function(val){
      this.$refs["input-"+val][0].select()
      document.execCommand('copy')
    },
    golink2shortlink: function(str){

      var shortlink =  str.replace(/^g/, '').replace(/^o/, '').replace(/^\//, '')


      if (shortlink.length > 0) {
        axios.get("_api/validate/" + shortlink)
        //axios.get("http://spectre:8000/_api/validate/" + shortlink)
          .then(r => r.data)
          .then(exists => {
              this.shortlinkexists = exists
              this.shortlinkok = !exists
          })

      }
      else {
        this.shortlinkexists = false
        this.shortlinkok = false
      }

      return shortlink
    },
    add_link: function() {

      // If shortlink isnt unique
      if (!this.shortlinkok) {
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
            this.newurl = {shortlink: ""};
          });

        this.$refs.shortlink.focus();
      }
    },
    del_link: function(url) {
      axios
        .get("_api/delete/" + url.shortlink)
        //.get("http://spectre:8000/_api/delete/" + url.shortlink)
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

.td-icons, .icons
  vertical-align: middle

.go
  color: $grey-light
  font-size: 0.75rem

.shortlink
  font-weight: bold

.destination:hover
  cursor: pointer;
  color: $black

.ed, .del
  color: $grey-light
  transition: $speed ease-in-out;

.icons .active
  cursor: pointer
  color: $green !important

.icons .inactive
  cursor: default
  color: $grey-lighter !important

tr:hover .del, tr:hover .ed
    color: $grey-dark

.del:hover
    color: $red !important
    cursor: pointer

.ed:hover
    color: $grey-dark !important
    cursor: pointer

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

.clipboard:hover
    color: $grey-dark !important
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
</style>

