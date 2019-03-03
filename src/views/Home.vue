<template lang="pug">
  div
    Header
    section.section
      div.columns
        .column.is-full
          LinkTable(:urls="urls")

</template>
<script>

  import axios from 'axios'

  import Header from '@/components/Header.vue'
  import LinkTable from '@/components/LinkTable.vue'

  export default {
    name: 'home',
    data () {

      return {
        urls: []
      }

    },
    mounted() {
      axios
        .get('http://localhost:8000/_api/allurls')
        .then(response => {
          this.urls = response.data
        })
    },
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
