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
           a.navbar-item(href="/") Home
           a.navbar-item(href="https://github.com/jeffjose/golinks") Source
           a.navbar-item About
       //    div.navbar-item.has-dropdown.is-hoverable
       //      a.navbar-link More

       //      div.navbar-dropdown
       //        a.navbar-item About
       //        a.navbar-item Jobs

</template>

<script>
export default {
  name: "Header",
  props: {
    msg: String
  }
};
</script>

<style scoped lang="sass">
@import "~bulma/sass/utilities/initial-variables";

.navbar-item
  font-size: 0.90rem;
  color: $grey-dark !important
  border-bottom: 3px solid $white
  transition: 100ms all ease-in-out

.navbar-item:hover
  //background-color: lighten($grey-dark, 50%) !important
  background-color: $white !important
  border-bottom: 3px solid $grey-dark
  color: $black !important

.logo:hover
  border-bottom: 3px solid $white !important

</style>
