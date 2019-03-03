<template lang="pug">
  div.about
    h1 This is the about page.
</template>

<script>
  export default {
    name: 'about',
    created () {
      document.title = "golinks for your home"
    }
  }
</script>
