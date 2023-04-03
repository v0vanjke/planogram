<script setup>
import { ref, computed, watch, onUnmounted } from 'vue';
import { useAppStore } from '@/store/app';
import { useApiStore } from '@/store/api';
const appStore = useAppStore()
const apiStore = useApiStore()

const props = defineProps({
  position: {
    default: () => {},
    type: Object,
    required: true,
  }
})

const boxID = appStore.overBoxID[0]
const step = 22.5 / 180 * Math.PI
const rotate = (direction) => {
  const anglePI = apiStore.shopBoxes[boxID].rotation.z
  apiStore.shopBoxes[boxID].rotation.z = Number((anglePI + (step * direction)).toFixed(5))
}

const X = ref(Math.round(apiStore.shopBoxes[boxID].size.x * 100))
const Y = ref(Math.round(apiStore.shopBoxes[boxID].size.y * 100))
const Z = ref(Math.round(apiStore.shopBoxes[boxID].size.z * 100))

const isDeleted = ref(false)

watch (
  () => X.value,
  (state) => {
    apiStore.shopBoxes[boxID].size.x = Number(state) / 100
  }
)
watch (
  () => Y.value,
  (state) => {
    apiStore.shopBoxes[boxID].size.y = Number(state) / 100
  }
)
watch (
  () => Z.value,
  (state) => {
    apiStore.shopBoxes[boxID].size.z = Number(state) / 100
  }
)

const deleteBox = () => {
  isDeleted.value = true;
  apiStore.deleteShopBox(boxID);
  appStore.roomPlannerSubmenu = false;
}

const copyBox = () => {
  apiStore.copyShopBox(boxID);
  appStore.roomPlannerSubmenu = false;
  }

onUnmounted (() => {
  if (!isDeleted.value) {
    apiStore.updateShopBox(boxID)
  }
})

</script>

<template>
  <v-card
    flat
    class="glass text-white"
    width="200"
    :style="`position: absolute; top: ${position.y - 298}px; left: ${position.x + 20}px`"
    >
    <v-card-text class="d-flex flex-column">
      <v-btn @click="deleteBox" color="hsla(9, 30%, 50%)" text variant="outlined"> удалить </v-btn>
      <div class="mt-5">
        <v-text-field v-model="X" type="number" label="x: ширина  (мм)" density="compact" hide-details="auto" variant="outlined"></v-text-field>
        <v-text-field v-model="Y" type="number" label="y: глубина (мм)" class="my-2" density="compact" hide-details="auto" variant="outlined"></v-text-field>
        <v-text-field v-model="Z" type="number" label="z: высота  (мм)" density="compact" hide-details="auto" variant="outlined"></v-text-field>
      </div>
      <v-text-field class="my-5" v-model="apiStore.shopBoxes[boxID].index" type="number" label="номер стеллажа" density="compact" hide-details="auto" variant="outlined"></v-text-field>
      <div class="d-flex justify-space-between">
        <v-btn @click="rotate(1)" icon size="x-small" variant="outlined">
          <v-icon size="x-large"> mdi-axis-z-rotate-counterclockwise</v-icon>
        </v-btn>
        <div class="text-center font-weight-thin mr-n2 mt-1" style="font-size: 36px">
          {{ Math.round(360 / Math.PI / 2 * apiStore.shopBoxes[boxID].rotation.z) }}&deg;
        </div>
        <v-btn @click="rotate(-1)" icon size="x-small" variant="outlined">
          <v-icon size="x-large"> mdi-axis-z-rotate-clockwise</v-icon>
        </v-btn>
      </div>
      <v-btn @click="copyBox" text variant="outlined" class="mt-4"> копировать </v-btn>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.glass {
  background: hsla(0, 0%, 0%, 0.4);
  box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(7px);
  -webkit-backdrop-filter: blur(7px);
}
</style>