// 📍 Collection - коллекции товара
<script setup>
import { ref, computed, onMounted } from "vue";
import {
  Box,
  Circle,
  Group,
  LambertMaterial,
  PhysicalMaterial,
  Text,
  Plane,
  RectAreaLight,
} from "troisjs";
// import Article from '@/components/Article';
import stringToColor from "string-to-color";
import { useApiStore } from "@/store/api";
import { useAppStore } from "@/store/app";
const apiStore = useApiStore();
const appStore = useAppStore();

const props = defineProps({
  id: {
    default: "",
    type: String,
    required: true,
  },
  size: {
    default: { x: 10.2, y: 4, z: 0.5 },
    type: Object,
    required: false,
  },
});

const data = computed(() => {
  return apiStore.shopCollections[props.id];
});

const box = computed(() => {
  if (data.value.boxID && !isSelected.value) {
    return apiStore.shopBoxes[data.value.boxID];
  }
  if (
    isSelected.value &&
    appStore.overBoxID.length > 0 &&
    appStore.collectionInOverBox.length < 2
  ) {
    return apiStore.shopBoxes[appStore.overBoxID[0]];
  }
  return data.value.boxID; // false
});

const collectionInCurrentBox = computed(() => {
  const result = ref([]);
  if (!data.value.boxID) return result.value;
  for (const collection of appStore.collectionInBox) {
    if (collection.boxID === data.value.boxID) {
      result.value.push(collection);
    }
  }
  return result.value;
});

const collectionInBoxCount = computed(() => {
  return collectionInCurrentBox.value.length;
});

//📍 SELECT
const isSelected = computed(() => {
  if (appStore.selectedCollectionID === props.id) {
    return true;
  }
  return false;
});

//📍 OVER
const isOver = computed(() => {
  if (appStore.overCollectionID[0] === props.id) {
    return true;
  }
  return false;
});
const eventOver = (val) => {
  if (val.over === false) {
    appStore.unoverCollection(props.id);
  } else {
    appStore.overCollection(props.id);
  }
};

const scale = computed(() => {
  if (typeof box.value === "object") {
    return { x: 1, y: 1, z: 1 };
  }
  return { x: 2, y: 2, z: 2 };
});

const rotation = computed(() => {
  if (typeof box.value === "object") {
    return box.value.rotation;
  }
  return { z: 0 };
});

const position = computed(() => {
  if (typeof box.value === "object") {
    return {
      ...box.value.position,
      z: box.value.size.z - props.size.z / 2 + 0.4,
    };
  }
  return { ...data.value.position, z: 0.2 };
});

const ifTwoCollectionShiftPosition = computed(() => {
  if (collectionInBoxCount.value === 2) {
    if (collectionInCurrentBox.value[0].name === data.value.name) {
      return { y: computedY.value / 2 };
    }
    return { y: -(computedY.value / 2) };
  }
  return { y: 0 };
});

//📍 Collection SIZES
const computedX = computed(() => {
  if (typeof box.value === "object") {
    return box.value.size.x - 1;
  }
  return props.size.x;
});
const computedY = computed(() => {
  if (typeof box.value === "object") {
    if (collectionInBoxCount.value === 2) {
      return box.value.size.y / 2;
    }
    return box.value.size.y;
  }
  return props.size.y;
});

const splitter = 0.8;

//📍 COLOR
const calcColor = stringToColor("black " + data.value.vendor);
const color = computed(() => {
  const rsp = ref({
    accent: calcColor,
    background: "hsl(0, 30%, 50%)",
    text: calcColor,
  });
  if (isOver.value || isSelected.value) {
    rsp.value["accent"] = "hsl(105, 70%, 30%)";
    rsp.value["background"] = "hsl(105, 70%, 30%)";
    rsp.value["text"] = "hsl(0, 0%, 0%)";
  }
  return rsp.value;
});
onMounted(() => {});
</script>

<template>
  <Group :position="position" :rotation="rotation" :scale="scale">
    <Plane
      :width="computedX"
      :height="computedY - computedY * splitter"
      :position="{
        y: (computedY / 2) * splitter + ifTwoCollectionShiftPosition.y,
      }"
    >
      <PhysicalMaterial :color="color.accent" />
    </Plane>
    <Plane
      @pointerOver="eventOver"
      :width="computedX"
      :position="{
        y: -(computedY / 2) * (1 - splitter) + ifTwoCollectionShiftPosition.y,
      }"
      :height="computedY - computedY * (1 - splitter)"
    >
      <PhysicalMaterial :color="color.background" />
    </Plane>
    <Text
      v-if="true"
      :text="data.name"
      align="center"
      :size="data.name.length < 9 ? 1.5 : 1.6 * (8 / data.name.length)"
      :curveSegments="1"
      :height="0"
      :position="{
        y: -(computedY / 2) * (0.9 - splitter) + ifTwoCollectionShiftPosition.y,
        z: 0.3,
      }"
      :font-src="appStore.typeface"
    >
      <PhysicalMaterial :color="color.text" />
    </Text>
  </Group>
</template>

<style scoped></style>
