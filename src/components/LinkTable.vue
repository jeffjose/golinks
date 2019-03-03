<template lang="pug">
 table.table.is-fullwidth.is-hoverable.is-striped
   thead
     tr
       th link
       th URL
       th creator
   tbody
     tr(v-for="url in urls")
       td
         span.go go/
         span.shortlink {{url.shortlink}}
       td
         span.destination {{url.destination}}
       td
         span.creator {{url.creator}}
</template>
<script>

export default {
  name: 'LinkTable',
  props: {
    urls: Array
  }
}
</script>

<style scoped lang="sass">
.go
  color: #AAA

.shortlink
  font-weight: bold
</style>

