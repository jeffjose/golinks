<template lang="pug">
   table.table.is-fullwidth.is-hoverable
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
           p.control.has-icons-left
             input.input.is-small(type="text", placeholder="shortlink", v-model="newurl.shortlink", @keyup.enter="add_link(newurl)")
             span.icon.is-small.is-left
               i.mdi.mdi-link
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
           p.control.has-icons-left
             input.input.is-small(disabled, type="text", placeholder="0")
             span.icon.is-small.is-left
               i.mdi.mdi-counter
         th
           p.control.has-icons-left
             input.input.is-small(disabled, type="text", placeholder="-")
             span.icon.is-small.is-left
               i.mdi.mdi-calendar-range
         th
           p.control.has-icons-left
             input.input.is-small(disabled, type="text", placeholder="-")
             span.icon.is-small.is-left
               i.mdi.mdi-calendar-range
         th.icons
             span.icon(@click="add_link(newurl)")
               i.mdi.mdi-plus-circle.add
       tr(v-for="url in urls")
         td
           span.golink
             span.go go/
             span.shortlink {{url.shortlink}}
         td
           span.destination {{url.destination}}
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
  data: function(){

  return {
      newurl: {}
    }
  },
  props: {
    urls: Array
  },
  filters: {
    from_now: function(date) {
      return moment(date).fromNow();
    }
  },
  methods: {
    add_link: function(){

      // Only if these values are set
      if (_.has(this.newurl, 'shortlink') && _.has(this.newurl, 'destination')) {

      axios
        .post("_api/add/" + this.newurl.shortlink, this.newurl)
        //.post("http://spectre:8000/_api/add/" + this.newurl.shortlink, this.newurl)
        .then(response => {
          this.$store.dispatch("loadURLs");
          this.newurl = {}
        });

      }
      else {
      console.log("lol")
      }
    },
    del_link: function(url) {
      console.log("delete", url);
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
.go
  color: #AAA
  font-size: 0.75rem

.shortlink
  font-weight: bold

.destination:hover, .golink:hover
  border-bottom: 1px solid blue;
  cursor: pointer;

.ed, .del, .add
  color: #D5D5D5

tr:hover .del, tr:hover .ed, tr:hover .add
    color: #AAA

.del:hover
    color: #ff3d3d !important
    cursor: pointer

.ed:hover
    color: #333333 !important
    cursor: pointer

.add:hover
    color: green !important
    cursor: pointer

thead tr span, tbody tr span
   font-size: 0.75rem;

.icons span
   font-size: 1rem;

</style>

