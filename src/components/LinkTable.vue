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
           span actions
     tbody
       tr
         th
           p.control.has-icons-left
             input.input.is-small(type="text", placeholder="shortlink")
             span.icon.is-small.is-left
               i.mdi.mdi-link
         th
           p.control.has-icons-left
             input.input.is-small(type="text", placeholder="URL to shorten")
             span.icon.is-small.is-left
               i.mdi.mdi-link
         th
           p.control.has-icons-left
             input.input.is-small(type="text", placeholder="User")
             span.icon.is-small.is-left
               i.mdi.mdi-account
         th.icons
           span.icon
             i.mdi.mdi-link-plus.add
       tr(v-for="url in urls")
         td
           span.golink
             span.go go/
             span.shortlink {{url.shortlink}}
         td
           span.destination {{url.destination}}
         td
           span.creator {{url.creator}}
         td.icons
           span.icon
             i.mdi.mdi-pencil.ed
           span.icon(@click="deleteLink(url)")
             i.mdi.mdi-delete.del

</template>
<script>
import axios from "axios";

import _ from "lodash";

export default {
  name: "LinkTable",
  props: {
    urls: Array
  },
  methods: {
    deleteLink: function(url) {
      console.log("delete", url);
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

