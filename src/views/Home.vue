<template lang="pug">
  div
    router-link(:to="{name:'about'}") about
    section.hero.is-fullheight.welcome
      .hero-body
        .container
          p.title golinks

</template>
<script>
  import Header from '@/components/Header.vue'

  export default {
    name: 'home',
    created () {
      document.title = document.location.hostname;
    },
    components: {
      Header,
    }
  }
</script>

<style scoped lang="sass">
</style>
