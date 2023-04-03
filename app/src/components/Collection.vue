<script setup>
import { ref, onMounted} from "vue"
import {
  Box,
  LambertMaterial,
  Text,
} from 'troisjs';
import { useApiStore } from '@/store/api';
import { useAppStore } from '@/store/app';
const apiStore = useApiStore()
const appStore = useAppStore()

const props = defineProps({
  collection: {
    default: "",
    type: String,
    required: false,
  },
})

const isSelected = ref(false)

const over = ref(false)
const collectionOver = (val) => {
  if (over.value === true && val === false && isSelected.value === true) {
    isSelected.value = false
  }
  over.value = val.over
}

const materialColor = () => {
  if (over.value) {
   return 'orange'}
  return 'white'
}

const textColor = () => {
  if (isSelected.value) {
    return 'red'
  }
  if (over.value) {
   return 'white'}
  return 'orange'
}

const box = ref(null)
const isSelected = ref(false)

const boxClick = () => {
  if (appStore.mode === 'goodsPlanner') {
    isSelected.value = !isSelected.value
  }
}

</script>

<template>
  <Box
    ref="box"
    :key="`${boxID}-article-${article}`"
    @pointerOver="collectionOver"
    :height=2
    :width=10
    :depth=2
    :position="{ x: 0, y: 0, z: 0 }"
    @click="boxClick"
  >
    <LambertMaterial :color="materialColor()"/>

    <Text
      :text="article"
      align="center"
      :size=0.8
      :height=0.01
      :position="{ x: 0, y: -0.2, z: 0 }"
      :rotation="{ x: Math.PI / 2 }"
      :cast-shadow="true"
      font-src="https://troisjs.github.io/assets/helvetiker_regular.typeface.json"
    >
      <LambertMaterial :color="textColor()"/>
    </Text>
  </Box>
</template>

<style scoped>
</style>