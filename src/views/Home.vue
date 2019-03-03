<template lang="pug">
  div
    Header
    section.section
      div.columns
        .column.is-full
          LinkTable(:urls="urls")

</template>
<script>

import {mapState } from 'vuex'

  import Header from '@/components/Header.vue'
  import LinkTable from '@/components/LinkTable.vue'

  export default {
    name: 'home',
    mounted() {
      this.$store.dispatch('loadURLs')
    },
    computed: mapState([
      'urls'
    ]),
    created () {
      document.title = document.location.hostname;
    },
    components: {
      Header,
      LinkTable,
    }
  }
</script>

<style scoped lang="sass">
</style>
