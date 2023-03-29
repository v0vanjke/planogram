<script setup>
import { ref, onMounted, watch, computed, reactive } from 'vue';
import { GridHelper } from 'three';
import {
  Group,
  PerspectiveCamera,
  Camera,
  PhysicalMaterial,
  DirectionalLight,
  Sphere,
  HemisphereLight,
  PointLight,
  Renderer,
  PhongMaterial,
  Plane,
  Scene,
} from 'troisjs';
import myBox from '@/components/Box';
import { useApiStore } from '@/store/api';
import { useAppStore } from '@/store/app';
const apiStore = useApiStore()
const appStore = useAppStore()

const positionComputed = computed(() => {
  if (appStore.pointerV3 && appStore.pointerV3.value) {
  return appStore.pointerV3.value
  }
})

const renderer = ref(null)
const scene = ref(null)

watch(
  // если есть выбранные объекты - перестать вращать камеру
  () => appStore.isSelectedBox,
  (state) => {
    renderer.value.three.cameraCtrl.enableRotate = !state
    renderer.value.three.cameraCtrl.update()
  },
)

onMounted(() => {
  const grid = new GridHelper(300, 30, "hsl(120, 100%, 80%)", "hsl(0, 1%, 92%)");
  grid.material.opacity = 0.9;
  grid.material.transparent = true;
  scene.value.add(grid);

  appStore.updateCameraCtrl(renderer.value.three.cameraCtrl)

  const positionV3 = renderer.value.three.pointer.positionV3

  const lastX = ref(0)
  const lastY = ref(0)
  renderer.value.onBeforeRender(() => {
    if (
      appStore.isSelectedBox
      && (lastX.value !== Math.round(positionV3.x)
      || lastY.value !== -Math.round(positionV3.z))
    ) {
      // выбрано оборудование. будем следить и двигать его туда сюда обратно
      lastX.value = Math.round(positionV3.x)
      lastY.value = -Math.round(positionV3.z)
      for (const boxID of appStore.selectedBoxId) {
        apiStore.moveBox(boxID, lastX.value, lastY.value)
      }
    }
  })
})

</script>
<template>
  <Renderer
    ref="renderer"
    antialias
    pointer
    resize
    shadow
    :orbit-ctrl="appStore.orbCtrlSettings"
  >
    <Camera :position="{ x: 0, y: 300, z: 0 }" />

    <Scene ref="scene" background="hsl(0, 0%, 30%)">
      <HemisphereLight />
      <DirectionalLight cast-shadow :position="{ x: 500, y: 700, z: 300 }" />
      <Group :rotation="{ x: -Math.PI / 2 }">
          <myBox v-for="v, boxID in apiStore.boxes" :key="`myBox-${boxID}`" :boxID="boxID"/>
      </Group>
      <Plane :width="300" :height="300" :rotation="{ x: -Math.PI / 2 }" receive-shadow>
        <PhongMaterial color="#999999" :props="{ depthWrite: false }" />
      </Plane>
    </Scene>
  </Renderer>
  <v-card class="helperCard">
    <v-btn text color="grey" @click="apiStore.addBox">
      add box
    </v-btn>
    appStore pointerV3:
    {{positionComputed}}
    <br>
    selectedBoxId:
    {{appStore.selectedBoxId}}
    <br>
    render:
    {{appStore.render}}
    <br>
    overBoxID:
    {{appStore.overBoxID}}
  </v-card>
</template>

<style scoped>
.helperCard {
  position: absolute;
  top: 20px;
  right: 30px;
  margin-left: 30px;
  padding: 10px;
}
</style>