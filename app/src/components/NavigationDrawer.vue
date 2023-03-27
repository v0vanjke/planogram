<script setup>
const items = [
     { name: 'Песочница', path: '/' },
     { name: 'Lights', path: '/lights' },
     { name: 'LightsComposition', path: '/lightsComp' },
     { name: 'FBX', path: '/fbx' },
 ]
</script>

<template>
  <v-navigation-drawer permanent elevation="6" color="grey" width="200" class="rounded-r-xl">
      <v-list class="ml-4">
          <v-list-item v-for="(item, i) in items" :key="i" class="rounded-l-xl" :to="item.path">
              {{ item.name }}
          </v-list-item>
      </v-list>
  </v-navigation-drawer>
</template>


<style scoped>
</style>