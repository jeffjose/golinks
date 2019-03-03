<template lang="pug">
  nav.navbar.is-light(role="navigation", aria-label="main navigation")
     div.navbar-brand
       a.navbar-item(href="/")
         img(src="http://localhost:8000/_admin/android-chrome-192x192.png", height=28)

       a.navbar-burger.burger(role="button", aria-label="menu", aria-expanded="false", data-target="navbarBasic")
         span(aria-hidden="true")
         span(aria-hidden="true")
         span(aria-hidden="true")

       div#navbarBasic.navbar-menu
         div.navbar-start
           a.navbar-item Home
           a.navbar-item Stats
           a.navbar-item Source
           a.navbar-item About
       //    div.navbar-item.has-dropdown.is-hoverable
       //      a.navbar-link More

       //      div.navbar-dropdown
       //        a.navbar-item About
       //        a.navbar-item Jobs

</template>

<script>

export default {
  name: 'Header',
  props: {
    msg: String
  }
}
</script>

<style scoped lang="sass">
</style>
