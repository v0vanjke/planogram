<script setup>
import { ref, computed } from "vue"
import {
  Box,
  LambertMaterial,
  Text,
} from 'troisjs';
import Roll from '@/components/Roll';
import { useApiStore } from '@/store/api';
import { useAppStore } from '@/store/app';
const apiStore = useApiStore()
const appStore = useAppStore()

const props = defineProps({
  boxID: {
    default: "",
    type: String,
    required: true,
  }
})

const isSelected = computed(() => {
  if ( !appStore.selectedBoxId.includes(props.boxID)) {
    return false
  }
  return true
})

const over = ref(false)
// const over = computed(() => {
//   if (appStore.boxOverId === props.boxID) {
//     return true
//   }
//   return false
// })

const boxOver = (val) => {
  console.log(val)
  if (val.over === false) {
    appStore.unoverBox()
    over.value = false
  } else if (!appStore.overBoxID) {
    over.value = true
    appStore.overBox(props.boxID)
  }
}

const boxClick = () => {
  console.log(apiStore.boxes[props.boxID].articles)

  if (isSelected.value) {
    // console.log('unselect boxID', props.boxID)
    appStore.unselectBox(props.boxID)
  }
  else {
    // console.log('  select boxID', props.boxID)
    if (!appStore.isSelectedBox) {
      appStore.selectBox(props.boxID)
    }
  }
}


const materialColor = () => {
if (isSelected.value) {
  return 'green'
}
  if (over.value) {
   return 'orange'}
  return 'grey'
}

const data = computed(() => {
  if (!apiStore.boxes) {
    return (() => {})
  }
  return apiStore.getBox(props.boxID)
})

</script>

<template>
  <Box
    :key="`box-${boxID}`"
    @pointerOver="boxOver"
    :width=10.9
    :height=4
    :depth=16
    :rotation="{ z: Math.PI * 2 }"
    :position="{x: data.x, y: data.y, z: 8}"
    @click="boxClick">
    <LambertMaterial :color="materialColor()"/>

      <Roll
        v-for="v, i in data.articles"
        :key="`${boxID}-roll-${v}`"
        :boxID="boxID"
        :article="v"
        :collection="data.collection"
        :vendor="data.vendor"
        :boxOver="over"

        :height=0.4
        :width=10
        :depth=2
        :position="{x: 0, y: -2.2, z: (i * 2.2) - 6.6 + ((6 - data.articles.length) * 2.2) }"
      >
      </Roll>

    <Text
      :text="data.vendor"
      align="center"
      :size="0.3"
      :height="0.01"
      :position="{ x: 3, y: -2, z: 7.4 }"
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
      :position="{ x: 0, y: -2, z: 6.4 }"
      :rotation="{ x: Math.PI / 2 }"
      :cast-shadow="true"
      font-src="https://troisjs.github.io/assets/helvetiker_regular.typeface.json"
    > </Text>
    <Text
      :text="`N${data.index}`"
      align="center"
      :size="1"
      :height="0.2"
      :position="{ x: 0, y: 0, z: 8 }"
      :cast-shadow="true"
      font-src="https://troisjs.github.io/assets/helvetiker_regular.typeface.json"
    > </Text>
  </Box>
</template>

<style scoped>
</style>