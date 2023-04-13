<script setup>
import { computed, onMounted, ref } from "vue";
import { useAppStore } from "@/store/app";
import { useApiStore } from "@/store/api";
const appStore = useAppStore();
const apiStore = useApiStore();

const items = [
  { name: "Песочница", path: "/" },
  // { name: 'Lights', path: '/lights' },
  // { name: 'LightsComposition', path: '/lightsComp' },
  // { name: 'FBX', path: '/fbx' },
];

// unique vendor names
const listVendor = computed(() => {
  if (!apiStore.apiCollections) return [];
  // from list of objects return list of unique item
  return apiStore.apiCollections
    .map((item) => item.vendor)
    .filter((value, index, self) => self.indexOf(value) === index);
});

// unique category names
const listCategory = computed(() => {
  if (!apiStore.apiCollections) return [];
  // from list of objects return list of unique item
  return apiStore.apiCollections
    .map((item) => item.category)
    .filter((value, index, self) => self.indexOf(value) === index);
});
</script>

<template>
  <div class="px-3 rounded-xl pt-8 mr-8 mb-8 navigation">
    <VList class="bg-transparent">
      <VListItem v-for="(item, i) in items" :key="i" class="rounded-lg text-white" :to="item.path">
        {{ item.name }}
      </VListItem>
    </VList>
    <div>
      <VBtn color="grey" @click="appStore.changeMode('roomPlanner')" block class="mb-1">
        Строительство
      </VBtn>
      <VBtn color="grey" @click="appStore.changeMode('goodsPlanner')" block>
        Планирование
      </VBtn>
    </div>
    <!--📍 элемент меню - оборудовние дефолтное -->
    <div color="transparent" v-if="appStore.mode === 'roomPlanner' && apiStore.apiBoxes">
      <div>Оборудование дефолтное</div>
      <div v-for="(box, boxID) in apiStore.apiBoxes" :key="boxID">
        <VCard flat @click="
          apiStore.addShopBox({ ...box, position: { x: -300, y: 0, z: 0 } })
        " class="my-2">
          <VCardSubtitle>
            <div>{{ box._id }}</div>
          </VCardSubtitle>
          <VCardText>
            <div>name: {{ box.name }}</div>
            <div>size: {{ box.size }}</div>
            <div>shelf: {{ box.shelf }}</div>
            <div>volume: {{ box.volume }}</div>
            <div>vendor: {{ box.vendor }}</div>
          </VCardText>
        </VCard>
      </div>
    </div>
    <!--📍 элемент меню - коллекции -->
    <div color="transparent" v-if="appStore.mode === 'goodsPlanner'">
      <v-card flat class="mt-5" color="transparent" v-if="appStore.mode === 'goodsPlanner'">
        <v-select label="категория" class="text-white" hide-selected density="comfortable" theme="dark"
          v-model="appStore.selectedCollectionCategory" :items="listCategory"></v-select>
        <v-select class="mt-n6" label="производители" hide-selected density="comfortable" theme="dark" variant="solo"
          v-model="appStore.selectedCollectionVendor" :items="listVendor"></v-select>
      </v-card>
      <div class="d-flex flex-wrap">
        <div v-for="el of appStore.apiCollectionFiltered" :key="el" class="pr-1 pb-1">
          <v-btn @click="apiStore.addShopCollection(el)" theme="dark" density="compact" flat text>
            {{ el.name }}
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.navigation {
  position: absolute;
  width: 360px;
  min-height: 50%;
  top: 2%;
  left: 1%;
  background: hsla(0, 0%, 0%, 0.4);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
}
</style>
