// 📍 BOX - оборудование
<script setup>
import { ref, computed, onMounted } from "vue"
import {
  Box,
  Circle,
  Group,
  LambertMaterial,
  Text,
  Plane,
  RectAreaLight,
} from 'troisjs';
import Article from '@/components/Article';
import { useApiStore } from '@/store/api';
import { useAppStore } from '@/store/app';
const apiStore = useApiStore()
const appStore = useAppStore()

const props = defineProps({
  boxID: {
    default: "",
    type: String,
    required: true,
  },
  box: {
    default: () => {},
    type: Object,
    required: true,
  },
  thickness: {
    default: 1,
    type: Number,
    required: false
  }
})

//📍 SELECT
const isSelected = computed(() => {
  if (appStore.selectedBoxID === props.boxID) {
    return true
  }
  return false
})

//📍 OVER
const isOver = computed(() => {
  if (appStore.overBoxID[0] === props.boxID) {
    return true
  }
  return false
})

const eventOver = (val) => {
  if (val.over === false) {
    appStore.unoverBox(props.boxID)
  } else {
    appStore.overBox(props.boxID)
  }
}

//📍 COLOR
const fillerColor = () => {
  return 'hsl(0, 0%, 10%)'
}

const wallColor = () => {
  if (isSelected.value) {return 'hsl(80, 100%, 50%)'}
  if (isOver.value) {return 'hsl(25, 100%, 50%)'}
  return 'hsl(27, 35%, 30%)'
}

//📍 BOX SIZES
const computedX = computed(() => {
  const normalizedSize = Math.round(props.box.size.x) - 0.06
  return normalizedSize
})
const computedY = computed(() => {
  const normalizedSize = Math.round(props.box.size.y) - 0.06
  return normalizedSize
})

</script>

<template>
  <Group
    :rotation="box.rotation"
    :position="{...box.position, z: box.position.z + box.size.z / 2}"
  >

    <!--📍 box 2d proection -->
    <RectAreaLight
      v-if="isSelected"
      :key="`plane-${boxID}`"
      :width="computedX"
      :height="computedY"
      :position="{z: - (box.position.z + box.size.z / 2) + 0.05}"
      :intensity="6 - box.position.z / 10"
      :helper="true"
      :rotation="{x: Math.PI}"
      color="hsl(95, 80%, 10%)"
    >
    </RectAreaLight>

    <!--📍 box walls -->
    <Box
      :width="computedX - (thickness * 2)"
      :height="thickness"
      :depth="box.size.z"
      :position="{y: (computedY / 2) - (thickness / 2)}"
    >
      <LambertMaterial :color="wallColor()"/>
    </Box>
    <div v-for="i in [1, -1]" :key="i">
      <Box
        :width="computedY"
        :height="thickness"
        :depth="box.size.z"
        :position="{x: ((computedX / 2 - (thickness / 2)) * i)}"
        :rotation="{z: Math.PI / 2}"
      >
        <LambertMaterial :color="wallColor()"/>
      </Box>
    </div>

    <!--📍 box filler -->
    <Box
      @pointerOver="eventOver"
      :width="computedX - thickness / 2"
      :height="computedY - thickness / 2"
      :depth="box.size.z - thickness / 2"
    >
      <!-- @click="eventClick" -->

      <LambertMaterial :color="fillerColor()"/>

    </Box>
    <Circle
      :radius="box.index > 999 ? 1.2 : 0.9"
      :segments=20
      :position="{ x: -box.size.x / 2 + 1.8, y: box.size.y / 2 - 1, z: box.size.z / 2 + 0.1}"
    >
        <LambertMaterial color="hsl(200, 80%, 10%)"/>
      <Text
        :text="`${box.index}`"
        align="center"
        :size="box.index > 9 ? 0.7 : 1"
        :height="0"
        :position="{z: 0.1}"
        :cast-shadow="true"
        font-src="https://troisjs.github.io/assets/helvetiker_regular.typeface.json"
      >
      <LambertMaterial color="hsl(0, 0%, 100%)"/>
      </Text>
    </Circle>
  </Group>


  <!-- <div v-if="appStore.mode != 'roomPlanner'">
       <Article
       v-for="v, i in data.articles"
       :key="`${boxID}-roll-${v}`"
       :boxID="boxID"
       :article="v"
       :collection="data.collection"
       :vendor="data.vendor"
       :boxOver="isOver"
       :height=0.4
       :width=10
       :depth=2
       :position="{x: data.x, y: data.y - 2.2, z: 8  + (i * 2.2) - 6.6 + ((6 - data.articles.length) * 2.2) }"
       >
       </Article>
       </div> -->
</template>

<style scoped>
</style>
