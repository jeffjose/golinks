<template lang="pug">
 table.table.is-fullwidth.is-hoverable.is-striped
  thead
    tr
      th link
      th URL
      th creator
  tbody
    tr
      td mail
      td https://mail.google.com/mail
      td jeffjose
    tr
      td cal
      td https://calendar.google.com/
      td jeffjose
</template>
<script>

export default {
  name: 'LinkTable',
  props: {
    msg: String
  }
}
</script>

<style scoped lang="sass">
</style>
