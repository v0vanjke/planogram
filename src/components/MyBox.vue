// 📍 BOX - оборудование
<script setup>
import { ref, computed, onMounted } from "vue";
import {
  Box,
  Circle,
  Group,
  LambertMaterial,
  Text,
  Plane,
  RectAreaLight,
} from "troisjs";
import Article from "@/components/Article";
import { useApiStore } from "@/store/api";
import { useAppStore } from "@/store/app";
const apiStore = useApiStore();
const appStore = useAppStore();

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
    required: false,
  },
});

//📍 SELECT
const isSelected = computed(() => {
  if (appStore.selectedBoxID === props.boxID) {
    return true;
  }
  return false;
});

//📍 OVER
const isOver = computed(() => {
  if (appStore.overBoxID[0] === props.boxID) {
    return true;
  }
  return false;
});

const eventOver = (val) => {
  if (appStore.isSelectedBox) {
    return;
  }
  if (val.over === false) {
    appStore.unoverBox(props.boxID);
  } else {
    appStore.overBox(props.boxID);
  }
};

//📍 COLOR
const fillerColor = () => {
  return "hsl(27, 35%, 30%)";
  // return 'hsl(0, 0%, 30%)'
};

const wallColor = () => {
  // if (isSelected.value) {return 'hsl(80, 80%, 15%)'}
  if (isOver.value && !isSelected.value) {
    return "hsl(30, 100%, 20%)";
  }
  return "hsl(0, 0%, 10%)";
  // return 'hsl(27, 35%, 30%)'
};

const backWallColor = () => {
  // if (isSelected.value) {return 'hsl(80, 80%, 15%)'}
  if (isOver.value && !isSelected.value) {
    return "hsl(30, 100%, 20%)";
  }
  return "hsl(0, 0%, 10%)";
  // return 'hsl(27, 35%, 30%)'
};
const shadowBoxColor = () => {
  return "hsl(195, 80%, 10%)";
};
const shadowBorderColor = () => {
  return "hsl(95, 100%, 30%)";
};

const numberColor = () => {
  return "hsl(200, 30%, 20%)";
};

const numberTextColor = () => {
  return "hsl(0, 0%, 100%)";
};

//📍 BOX SIZES
const computedX = computed(() => {
  const normalizedSize = Math.round(props.box.size.x) - 0.06;
  return normalizedSize;
});
const computedY = computed(() => {
  const normalizedSize = Math.round(props.box.size.y) - 0.06;
  return normalizedSize;
});
const computedZ = computed(() => {
  return props.box.size.z;
});
</script>

<template>
  <Group
    :rotation="box.rotation"
    :position="{ ...box.position, z: box.position.z + computedZ / 2 }"
  >
    <!--📍 box 2d proection -->
    <div v-if="isSelected">
      <RectAreaLight
        v-if="box.position.z > computedZ / 10"
        :key="`plane-${boxID}`"
        :width="computedX"
        :height="computedY"
        :position="{ z: -(box.position.z + computedZ / 2) + 0.1 }"
        :intensity="6 - box.position.z / 5"
        :helper="true"
        :rotation="{ x: Math.PI }"
        :color="shadowBorderColor()"
      >
      </RectAreaLight>
      <div v-for="i in [1, -1]" :key="i">
        <Plane
          :width="10000"
          :height="0.2"
          :position="{
            z: -(box.position.z + computedZ / 2) + 0.1,
            y: i * (computedY / 2 + 0.1),
          }"
        >
          <LambertMaterial :color="shadowBorderColor()" />
        </Plane>
        <Plane
          :width="10000"
          :height="0.2"
          :rotation="{ z: Math.PI / 2 }"
          :position="{
            z: -(box.position.z + computedZ / 2) + 0.1,
            x: i * (computedX / 2 + 0.1),
          }"
        >
          <LambertMaterial :color="shadowBorderColor()" />
        </Plane>
      </div>
      <!-- ось  -->
      <Box
        :width="300"
        :height="0.2"
        :depth="0.2"
        :rotation="{ y: Math.PI / 2 }"
      >
        <LambertMaterial :color="shadowBorderColor()" />
      </Box>
    </div>

    <!--📍 box walls -->
    <Box
      :width="computedX - thickness * 2"
      :height="thickness"
      :depth="computedZ"
      :position="{ y: computedY / 2 - thickness / 2 }"
    >
      <LambertMaterial :color="backWallColor()" />
    </Box>
    <div v-for="i in [1, -1]" :key="i">
      <Box
        cast-shadow
        :width="computedY"
        :height="thickness"
        :depth="computedZ"
        :position="{ x: (computedX / 2 - thickness / 2) * i }"
        :rotation="{ z: Math.PI / 2 }"
      >
        <LambertMaterial :color="wallColor()" />
      </Box>
    </div>

    <!--📍 box filler -->
    <Box
      @pointerOver="eventOver"
      :width="computedX - thickness * 2"
      :height="computedY - thickness"
      :depth="computedZ - thickness / 2"
      cast-shadow
    >
      <LambertMaterial :color="fillerColor()" />

      <!-- кол-во полок -->
      <Text
        :text="`${box.shelf}`"
        align="center"
        :size="3"
        :height="0"
        :position="{ z: computedZ / 2 - thickness / 4 + 0.05 }"
        :rotation="{ z: Math.PI * 2 - box.rotation.z + appStore.cameraAzimuth }"
        font-src="https://troisjs.github.io/assets/helvetiker_regular.typeface.json"
      >
        <LambertMaterial :color="backWallColor()" />
      </Text>

      <!-- надпись у подножия -->
      <!-- <Text
            :text="`${Math.round(computedX * 100)} x ${Math.round(computedY * 100)} x ${Math.round(computedZ * 100)} mm`"
            align="center"
            :size="0.5"
            :height="0"
            :position="{y: -computedY / 2 - thickness, z: - computedZ / 2 + 0.1}"
            font-src="https://troisjs.github.io/assets/helvetiker_regular.typeface.json"
          >
            <LambertMaterial color="hsl(200, 40%, 21%)"/>
          </Text> -->
    </Box>

    <!--📍 box number -->
    <Circle
      :radius="box.index > 999 ? 2 : 1.6"
      :segments="20"
      :rotation="{ z: Math.PI * 2 - box.rotation.z + appStore.cameraAzimuth }"
      :position="{
        x: -computedX / 2 + 1.8,
        y: computedY / 2 - 1.4,
        z: computedZ / 2 + 0.05,
      }"
    >
      <LambertMaterial :color="numberColor()" />
      <Text
        :text="`${box.index}`"
        align="center"
        :size="box.index > 9 ? 1.4 : 1.2"
        :height="0"
        :position="{ z: 0.05 }"
        font-src="https://troisjs.github.io/assets/helvetiker_regular.typeface.json"
      >
        <LambertMaterial :color="numberTextColor()" />
      </Text>
    </Circle>
  </Group>
</template>

<style scoped></style>
