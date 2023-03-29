<script setup>
import { ref, onMounted} from "vue"
import {
  Box,
  LambertMaterial,
  Text,
} from 'troisjs';
// import { useApiStore } from '@/store/api';
// import { useAppStore } from '@/store/app';
// const apiStore = useApiStore()
// const appStore = useAppStore()

const props = defineProps({
  boxID: {
    default: "",
    type: String,
    required: true,
  },
  article: {
    default: "",
    type: String,
    required: true,
  },
  collection: {
    default: "",
    type: String,
    required: false,
  },
  vendor: {
    default: "",
    type: String,
    required: false,
  },
  position: {
    default: () => {},
    type: Object,
    required: true,
  },
  boxOver: {

    default: false,
    type: Boolean,
    required: false,
  }
})

const over = ref(false)
const articleOver = (val) => {
  if (props.boxOver) {
    over.value = val.over
  }
}

const materialColor = () => {
  if (over.value) {
   return 'orange'}
  return 'white'
}
const textColor = () => {
  if (over.value) {
   return 'white'}
  return 'orange'
}

onMounted(() => {
  console.log(props.article, props.boxID, props.position)
})

</script>

<template>
  <Box
    :key="`${boxID}-article-${article}`"
    @pointerOver="articleOver"
    :height=0.4
    :width=10
    :depth=2
    :position="position"
  >
    <LambertMaterial :color="materialColor()"/>

    <Text
      :text="article"
      align="center"
      :size="0.8"
      :height="0.01"
      :position="{x: 0, y: -0.2, z: 0 }"
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