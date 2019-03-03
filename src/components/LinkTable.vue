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
           span actions
     tbody
       tr
         th
           p
             input.input.is-small(ref="shortlink", type="text", placeholder="shortlink", @input="newurl.shortlink = golink2shortlink($event.target.value)", :value="golink", @keyup.enter="add_link(newurl)")
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
             span.icon(@click="add_link(newurl)")
               i.mdi.mdi-plus-circle.add
       tr(v-for="url in urls")
         td
           input.input-hidden(:ref="'input-' + url.shortlink", :value="'go/' + url.shortlink")
           span.golink(@click="copy(url.shortlink)")
             span.go go/
             span.shortlink {{url.shortlink}}
           span.icon.clipboard(@click="copy(url.shortlink)")
             i.mdi.mdi-clipboard-text
         td
           span.destination {{url.destination | shorten}}
         td
           span.creator {{url.creator}}
         td
           span.hits {{url.hits}}
         td
           span.created {{url.created | from_now}}
         td
           span.modified {{url.modified | from_now}}
         td.icons
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
      newurl: {shortlink: ""}
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
      return str.replace(/^g/, '').replace(/^o/, '').replace(/^\//, '')
    },
    add_link: function() {
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

.go
  color: $grey-light
  font-size: 0.75rem

.shortlink
  font-weight: bold

.destination:hover
  border-bottom: 1px solid $turquoise
  cursor: pointer;

.ed, .del, .add
  color: $grey-light
  transition: $speed ease-in-out;

tr:hover .del, tr:hover .ed, tr:hover .add
    color: $grey-dark

.del:hover
    color: $red !important
    cursor: pointer

.ed:hover
    color: $grey-dark !important
    cursor: pointer

.add:hover
    color: $green !important
    cursor: pointer

thead tr span, tbody tr span
   font-size: 0.75rem;

.icons span
   font-size: 1rem;

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

