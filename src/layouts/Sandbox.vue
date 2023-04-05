<script setup>
  import NavigationDrawer from '@/components/NavigationDrawer.vue'
</script>

<template>
  <v-card>
    <v-layout>
      <v-main>
        <v-app>
          <NavigationDrawer />
          <router-view />
        </v-app>
      </v-main>

    </v-layout>
  </v-card>
</template>
