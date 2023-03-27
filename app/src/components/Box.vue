<script setup>
import { ref, computed, onMounted, watch } from "vue"
import {
  Box,
  PhysicalMaterial,
  LambertMaterial,
  Text,
} from 'troisjs';
import { useApiStore } from '@/store/api';
import { useAppStore } from '@/store/app';
const apiStore = useApiStore()
const appStore = useAppStore()

const props = defineProps({
  key: {
    default: "",
    type: String,
    required: true,
  },
  boxID: {
    default: "",
    type: String,
    required: true,
  }
})

const isSelected = ref(false)

const over = ref(false)
const boxOver = (val) => {
  over.value = val.over
}

const click = ref(false)
const boxClick = (val) => {
  if (!isSelected.value) {
    appStore.disableRotate()
  }
  else {
    appStore.enableRotate()
  }
  isSelected.value = !isSelected.value
}


const materialColor = () => {
if (isSelected.value) {
  return 'green'
}
  if (over.value) {
   return 'orange'
 }
  return 'grey'
}

const data = computed(() => {
  if (!apiStore.boxes) {
    return (() => {})
  }
  return apiStore.getBox(props.boxID)
})

const position = computed (() => {
  return {x: 0, y: 0, z: 8}
})

</script>

<template>
    <Box
      @pointerOver="boxOver"
      cast-shadow
      :width=11
      :height=4
      :depth=16
      :rotation="{ z: Math.PI * 2 }"
      :position="{x: data.x, y: data.y, z: 8}"
      @click="boxClick">
        <LambertMaterial :color="materialColor()"/>
        <Text
        :text="data.vendor"
        align="center"
        :size="0.3"
        :height="0.01"
        :position="{ x: 2, y: -2, z: 7 }"
        :rotation="{ x: Math.PI / 2 }"
        :cast-shadow="true"
        font-src="https://troisjs.github.io/assets/helvetiker_regular.typeface.json"
      >
        <LambertMaterial color="black"/>
      </Text>
      <Text
        :text="data.collection"
        align="center"
        :size="1"
        :height="0.2"
        :position="{ x: 0, y: -2, z: 6 }"
        :rotation="{ x: Math.PI / 2 }"
        :cast-shadow="true"
        font-src="https://troisjs.github.io/assets/helvetiker_regular.typeface.json"
      > </Text>
    </Box>
</template>

<style scoped>
</style>