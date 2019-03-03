<template lang="pug">
  div
    Header
    section.section
      h1.title All links


      div.columns
        .column.is-full
          LinkTable

</template>
<script>
  import Header from '@/components/Header.vue'
  import LinkTable from '@/components/LinkTable.vue'

  export default {
    name: 'home',
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
