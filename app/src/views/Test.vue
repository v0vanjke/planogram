<script setup>
import { ref, onMounted, watch, computed, reactive } from 'vue';
import { GridHelper, RepeatWrapping } from 'three';
import {
  RectAreaLight,
  BoxGeometry,
  Camera,
  DirectionalLight,
  Group,
  Text,
  HemisphereLight,
  Mesh,
  StandardMaterial,
  PerspectiveCamera,
  PhongMaterial,
  PhysicalMaterial,
  Plane,
  PointLight,
  Renderer,
  Scene,
  Texture,
  Sphere,
} from 'troisjs';
import myBox from '@/components/MyBox';
import roomPlannerSubmenu from '@/components/menu-room-planner-submenu';
import { useApiStore } from '@/store/api';
import { useAppStore } from '@/store/app';
const apiStore = useApiStore()
const appStore = useAppStore()


const texturesProps = {
        repeat: { x: 10, y: 5 },
        wrapS: RepeatWrapping,
        wrapT: RepeatWrapping,
      }

const rectLightsProps = {
        lookAt: { x: 0, y: -90, z: 25 },
        intensity: 5,
        width: 300,
        height: 50,
        helper: true,
      }
const rectLightsPosition = { x: 0, y: 0, z: 25 }

const renderer = ref(null)
const scene = ref(null)

const getPosition2D = () => {
  return renderer.value.three.pointer.position
}

watch(
  // если есть выбранные объекты - перестать вращать камеру
  () => appStore.isSelectedBox,
  (state) => {
    renderer.value.three.cameraCtrl.enableRotate = !state
    renderer.value.three.cameraCtrl.update()
  },
)

watch(
  // изменился режим работы - перенастраиваем
  () => appStore.mode,
  (state) => {
    if (state === 'roomPlanner')
    renderer.value.three.cameraCtrl.enableRotate = !state
    renderer.value.three.cameraCtrl.update()
  },
)

onMounted(() => {
  const grid = new GridHelper(300, 30, "hsl(80, 100%, 50%)", "hsl(0, 1%, 92%)");
  grid.material.opacity = 0.1;
  grid.material.transparent = true;
  scene.value.add(grid);

  appStore.updateCameraCtrl(renderer.value.three.cameraCtrl)

  const positionV3 = renderer.value.three.pointer.positionV3

  const lastX = ref(0)
  const lastY = ref(0)
  const lastZ = ref(0)
  renderer.value.onBeforeRender(() => {
    if (
      appStore.isSelectedBox
      && (
        lastX.value !== Math.round(positionV3.x)
        || lastY.value !== -Math.round(positionV3.z)
        || lastZ.value !== Math.round(positionV3.y)
      )
    ) {
      // выбрано оборудование. будем следить и двигать его туда сюда обратно
      lastX.value = Math.round(positionV3.x)
      lastY.value = -Math.round(positionV3.z)
      lastZ.value = Math.round(positionV3.y)
      if (lastZ.value < 0) { lastZ.value = 0 }
      apiStore.moveShopBox(appStore.selectedBoxID, lastX.value, lastY.value, lastZ.value)
    }
  })
})

</script>
<template>
  <Renderer
    @mousedown="appStore.eventMouseDown"
    @mouseup="appStore.eventMouseUp"
    ref="renderer"
    antialias
    pointer
    resize
    shadow
    :orbit-ctrl="appStore.orbCtrlSettings"
  >
    <Camera :position="{ x: 0, y: 200, z: 0 }" />

    <Scene ref="scene" background="hsl(0, 0%, 60%)" >
      <HemisphereLight />
      <DirectionalLight cast-shadow :position="{ x: 500, y: 700, z: 300 }" />
      <Plane :width="300" :height="100" receive-shadow :rotation="{ x: -Math.PI / 2, y: 0, z: 0 }">
        <myBox v-for="v, boxID in apiStore.shopBoxes" :key="boxID" :boxID="boxID" :box="v"/>
        <PhongMaterial color="hsl(200, 50%, 15%)" :props="{ depthWrite: true }" />
        <!-- <StandardMaterial :props="{ displacementScale: 0.2, roughness: 0, metalness: 0 }"  >
             <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_basecolor.jpg" />
             <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_height.png" name="displacementMap" />
             <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_normal.jpg" name="normalMap" />
             <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_roughness.jpg" name="roughnessMap" />
             <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_ambientOcclusion.jpg" name="aoMap" />
             </StandardMaterial> -->
      </Plane>
    </Scene>
  </Renderer>
  <roomPlannerSubmenu v-if="appStore.roomPlannerSubmenu" :position="getPosition2D()"/>
  <v-card class="helperCard">
    <v-btn text color="grey" @click="apiStore.addBox">
      add box
    </v-btn>
    selectedBoxId:
    {{appStore.selectedBoxId}}
    <br>
    overBoxID:
    {{appStore.overBoxID}}
    <br>
    overCollectionID:
    {{appStore.overCollectionID}}
    <br>
    mode:
    {{appStore.mode}}
    <br>
    roomPlannerSubmenu:
    {{appStore.roomPlannerSubmenu}}
    <br>
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