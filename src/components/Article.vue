<script setup>
import { computed, onMounted } from "vue";
import { Box, LambertMaterial, Text, Plane } from "troisjs";
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
  inListID: {
    default: 0,
    type: Number,
    required: true,
  },
});

//📍 ENTITY
const box = computed(() => {
  return apiStore.shopBoxes[props.boxID];
});
const article = computed(() => {
  if (typeof box.value[props.inListID] === "undefined") {
    return false;
  }
  return box.articles[props.inListID];
});

//📍 PROPERTIES ARTICLE ELEMENT
const size = {
  x: box.value.size.x - 2,
  y: 0.2,
  z: box.value.size.z / box.value.shelf - 0.4,
};
const position = {
  x: 0,
  y: -(box.value.size.y / 2 + 0.3),
  z:
    box.value.size.z / 2 -
    size.z / 2 -
    (size.z + 0.2) * (props.inListID - 1) - // шаговое смещение от индекса
    0.6, // общее смещение вниз
};
const rotation = { ...box.rotation, x: Math.PI / 2 };

//📍 COLOR
const mainColor = () => {
  if (article.value) {
    return "grey";
  }
  return "hsl(27, 35%, 30%)";
};
</script>

<template>
  <Plane
    :width="size.x"
    :height="size.z"
    :position="position"
    :rotation="rotation"
  >
    <LambertMaterial :color="mainColor()" />
    <Text
      v-if="true"
      :text="article || inListID.toString()"
      align="center"
      :size="1"
      :curveSegments="1"
      :height="0"
      :position="{ z: 0.1 }"
      :font-src="appStore.typeface"
    >
      <LambertMaterial color="black" />
    </Text>
  </Plane>
</template>

<style scoped></style>
