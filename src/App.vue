<template lang="pug">
  #app
    router-view
</template>

<style lang="sass">
@import url("https://fonts.googleapis.com/css?family=Open+Sans|Material+Icons");
@import url("https://cdn.materialdesignicons.com/3.5.95/css/materialdesignicons.min.css");

// 1. Import the initial variables
@import "~bulma/sass/utilities/initial-variables";

// Customizations go here

$table-cell-border-width: 0px;
$table-head-cell-border-width: 0px;
$table-cell-padding: 0.20em

$table-row-active-background-color: lighten(adjust-hue($blue, 30%), 15%)

$table-row-hover-background-color: $white-ter


$family-sans-serif: 'Roboto', sans-serif;

// 2. Import the rest of Bulma
@import "~bulma";


html
  background-color: rgb(246, 249, 252);
</style>
