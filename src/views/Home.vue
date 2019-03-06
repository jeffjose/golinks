<template lang="pug">
  div.home
    Header
    section.section
      div.columns
        .column.is-narrow
          div.sidebar
            p foo
        .column.is-four-fifths
          LinkTable(:urls="urls")

</template>
<script>
import { mapState } from "vuex";

import Header from "@/components/Header.vue";
import LinkTable from "@/components/LinkTable.vue";

export default {
  name: "home",
  mounted() {
    this.$store.dispatch("loadURLs");
  },
  computed: mapState(["urls"]),
  created() {
    document.title = document.location.hostname;
  },
  components: {
    Header,
    LinkTable
  }
};
</script>

<style scoped lang="sass">
.columns
  display: flex;
  flex-direction: row
  align-items: stretch

.sidebar
  width: 150px;
  border-right: 1px solid black
  height: 100%

</style>
