<script setup>
import { computed, onMounted } from 'vue';
import { useAppStore } from '@/store/app';
import { useApiStore } from '@/store/api';
const appStore = useAppStore()
const apiStore = useApiStore()

const items = [
  { name: 'Песочница', path: '/' },
  { name: 'Lights', path: '/lights' },
  { name: 'LightsComposition', path: '/lightsComp' },
  { name: 'FBX', path: '/fbx' },
]
</script>

<template>
  <v-navigation-drawer elevation="6" width="300" class="rounded-r-xl px-3 glass">
      <v-list class="ml-4">
          <v-list-item v-for="(item, i) in items" :key="i" class="rounded-l-xl" :to="item.path">
              {{ item.name }}
          </v-list-item>
      </v-list>
      <div>
        <v-btn @click="appStore.changeMode('roomPlanner')" block class="mb-1"> Строительство </v-btn>
        <v-btn @click="appStore.changeMode('goodsPlanner')" block> Планирование </v-btn>
      </div>
      <!--📍 элемент меню - оборудовние дефолтное -->
      <div color="transparent" v-if="appStore.mode === 'roomPlanner' && apiStore.apiBoxes">
        <div> Оборудование дефолтное </div>
        <div v-for="box, boxID in apiStore.apiBoxes" :key="boxID">
          <v-card flat @click="apiStore.addShopBox({...box, position: {x: -300, y: 0, z: 0}})"  class="my-2">
            <v-card-subtitle>
              <div>{{box._id}}</div>
            </v-card-subtitle>
            <v-card-text>
              <div>name: {{box.name}}</div>
              <div>size: {{box.size}}</div>
              <div>shelf: {{box.shelf}}</div>
              <div>volume: {{box.volume}}</div>
              <div>vendor: {{box.vendor}}</div>
            </v-card-text>
          </v-card>
        </div>
      </div>
      <div color="transparent" v-if="appStore.mode === 'goodsPlanner'">
        <div> Коллекции из api </div>
        <div v-for="collection in apiStore.apiCollections" :key="collection._id">
          <div @click="apiStore.addCollection(collection)"  class="my-1">
              {{collection}}
          </div>
        </div>
      </div>
  </v-navigation-drawer>
</template>


<style scoped>
.glass {
  background: hsla(0, 0%, 0%, 0.4);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(7px);
  -webkit-backdrop-filter: blur(7px);
}
</style>