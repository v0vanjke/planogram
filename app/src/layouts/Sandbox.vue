<script setup>
  import NavigationDrawer from '@/components/NavigationDrawer.vue'
</script>

<template>
  <v-card>
    <v-layout>
      <NavigationDrawer />
      <v-main>
        <v-app>
          <router-view />
        </v-app>
      </v-main>

    </v-layout>
  </v-card>
</template>
