<template lang="pug">
  nav.navbar.is-white(role="navigation", aria-label="main navigation")
     div.navbar-brand
       a.navbar-item(href="/")
         img(src="_admin/android-chrome-192x192.png", height=28)

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
@import "~bulma/sass/utilities/initial-variables";

.navbar a
  font-size: 0.90rem;
  color: $grey-dark !important

</style>
