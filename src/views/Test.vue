<script setup>
import { ref, onMounted, watch, computed, reactive } from "vue";
import { GridHelper, RepeatWrapping } from "three";
import {
  RectAreaLight,
  PointLight,
  DirectionalLight,
  HemisphereLight,
  AmbientLight,
  SpotLight,
  BoxGeometry,
  Box,
  Camera,
  Group,
  Text,
  Mesh,
  StandardMaterial,
  PerspectiveCamera,
  LambertMaterial,
  PhongMaterial,
  PhysicalMaterial,
  Plane,
  Renderer,
  Scene,
  Texture,
  Sphere,
} from "troisjs";
import myBox from "@/components/MyBox";
import Collection from "@/components/Collection";
import roomPlannerSubmenu from "@/components/menu-room-planner-submenu";
import { useApiStore } from "@/store/api";
import { useAppStore } from "@/store/app";
const apiStore = useApiStore();
const appStore = useAppStore();

const texturesProps = {
  repeat: { x: 10, y: 5 },
  wrapS: RepeatWrapping,
  wrapT: RepeatWrapping,
};

const rectLightsProps = {
  lookAt: { x: 0, y: -90, z: 25 },
  intensity: 5,
  width: 300,
  height: 50,
  helper: true,
};
const rectLightsPosition = { x: 0, y: 0, z: 25 };

const renderer = ref(null);
const scene = ref(null);

const getPosition2D = () => {
  return renderer.value.three.pointer.position;
};

watch(
  // если есть выбранные объекты - перестать вращать камеру
  () => appStore.isSelectedBox,
  (state) => {
    renderer.value.three.cameraCtrl.enableRotate = !state;
    renderer.value.three.cameraCtrl.update();
  }
);

watch(
  // изменился режим работы - перенастраиваем
  () => appStore.mode,
  (state) => {
    if (state === "roomPlanner") {
    }
    if (state === "goodsPlanner") {
    }
  }
);

onMounted(() => {
  const grid = new GridHelper(500, 50, "hsl(80, 100%, 50%)", "hsl(0, 1%, 92%)");
  grid.material.opacity = 0.1;
  grid.material.transparent = true;
  grid.position.y = 0.05;
  scene.value.add(grid);

  const positionV3 = renderer.value.three.pointer.positionV3;

  const cameraCtrl = renderer.value.three.cameraCtrl;
  const frameN = ref(0);
  // console.log(cameraCtrl)

  const lastX = ref(0);
  const lastY = ref(0);
  const lastZ = ref(0);
  renderer.value.onBeforeRender(() => {
    if (frameN.value > 59) {
      appStore.cameraAzimuth = cameraCtrl.getAzimuthalAngle();
      frameN.value = -1;
    }
    frameN.value += 1;
    if (
      (appStore.isSelectedBox || appStore.isSelectedCollection) &&
      (lastX.value !== Math.round(positionV3.x) ||
        lastY.value !== -Math.round(positionV3.z) ||
        lastZ.value !== Math.round(positionV3.y))
    ) {
      // курсор переместился
      lastX.value = Math.round(positionV3.x);
      lastY.value = -Math.round(positionV3.z);
      lastZ.value = Math.round(positionV3.y);

      if (appStore.isSelectedBox) {
        // выбрано оборудование. будем следить и двигать его туда сюда обратно
        if (lastZ.value < 0) {
          lastZ.value = 0;
        }
        apiStore.moveShopBox(
          appStore.selectedBoxID,
          lastX.value,
          lastY.value,
          lastZ.value
        );
      }
      if (appStore.isSelectedCollection) {
        if (lastZ.value < 0) {
          lastZ.value = 0;
        }
        apiStore.moveShopCollection(
          appStore.selectedCollectionID,
          lastX.value,
          lastY.value,
          lastZ.value
        );
      }
    }
  });
});
</script>
<template>
  <!-- pointer -->
  <Renderer
    @mousedown="appStore.eventMouseDown"
    @mouseup="appStore.eventMouseUp"
    ref="renderer"
    antialias
    resize
    pointer
    shadow
    :orbit-ctrl="appStore.orbCtrlSettings"
  >
    <Camera :position="{ x: 0, y: 500, z: 0 }" />

    <Scene ref="scene" background="hsl(0, 0%, 60%)">
      <AmbientLight color="hsl(0, 0%, 100%)" />
      <!-- если выключить - будет как бы ночь -->
      <HemisphereLight />
      <DirectionalLight cast-shadow :position="{ x: 100, y: 200, z: 100 }" />

      <SpotLight
        cast-shadow
        color="hsl(0, 0%, 100%)"
        :intensity="0.2"
        :position="{ x: 0, y: 300, z: 300 }"
        :angle="Math.PI / 8"
        :penumbra="0.1"
        :shadow-map-size="{ width: 2048, height: 2048 }"
      />
      <SpotLight
        cast-shadow
        color="hsl(0, 0%, 100%)"
        :intensity="0.2"
        :position="{ x: 0, y: 300, z: -300 }"
        :angle="Math.PI / 8"
        :penumbra="0.1"
        :shadow-map-size="{ width: 2048, height: 2048 }"
      />

      <SpotLight
        cast-shadow
        color="hsl(0, 0%, 100%)"
        :intensity="0.5"
        :position="{ x: 500, y: 300, z: 0 }"
        :angle="Math.PI / 8"
        :penumbra="0.1"
        :shadow-map-size="{ width: 2048, height: 2048 }"
      />
      <SpotLight
        cast-shadow
        color="hsl(0, 0%, 100%)"
        :intensity="0.5"
        :position="{ x: -500, y: 300, z: 0 }"
        :angle="Math.PI / 8"
        :penumbra="0.1"
        :shadow-map-size="{ width: 2048, height: 2048 }"
      />

      <Box
        :width="500"
        :height="300"
        :depth="1"
        :position="{ y: -0.9 }"
        :rotation="{ x: -Math.PI / 2 }"
      >
        <LambertMaterial color="hsl(0, 0%, 5%)" />
      </Box>
      <Box
        :width="500"
        :height="300"
        :depth="2"
        :position="{ y: -2.4 }"
        :rotation="{ x: -Math.PI / 2 }"
      >
        <LambertMaterial color="hsl(0, 0%, 15%)" />
      </Box>
      <Box
        :width="500"
        :height="300"
        :depth="4"
        :position="{ y: -5.4 }"
        :rotation="{ x: -Math.PI / 2 }"
      >
        <LambertMaterial color="hsl(25, 50%, 20%)" />
      </Box>
      <Box
        :width="500"
        :height="300"
        :depth="12"
        :position="{ y: -13.4 }"
        :rotation="{ x: -Math.PI / 2 }"
      >
        <LambertMaterial color="hsl(40, 100%, 30%)" />
      </Box>

      <Plane
        :width="500"
        :height="300"
        receive-shadow
        :rotation="{ x: -Math.PI / 2 }"
      >
        <Collection
          v-for="(v, collectionID) in apiStore.shopCollections"
          :key="collectionID"
          :id="collectionID"
        />
        <myBox
          v-for="(v, boxID) in apiStore.shopBoxes"
          :key="boxID"
          :boxID="boxID"
          :box="v"
        />
        <PhongMaterial
          color="hsl(200, 50%, 15%)"
          :props="{ depthWrite: true }"
        />
      </Plane>
    </Scene>
  </Renderer>
  <roomPlannerSubmenu
    v-if="appStore.roomPlannerSubmenu"
    :position="getPosition2D()"
  />
  <v-card class="helperCard" v-if="true">
    overBoxID:
    {{ appStore.overBoxID }}
    <br />
    mode:
    {{ appStore.mode }}
    <br />
    overCollectionID:
    {{ appStore.overCollectionID }}
  </v-card>
  <div class="gltfViewer"></div>
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

<script>
(function () {
  var script = document.createElement("script");
  script.onload = function () {
    var stats = new Stats();
    stats.domElement.style.top = "";
    stats.domElement.style.left = "10px";
    stats.domElement.style.bottom = "10px";
    document.body.appendChild(stats.dom);
    requestAnimationFrame(function loop() {
      stats.update();
      requestAnimationFrame(loop);
    });
  };
  script.src = "https://mrdoob.github.io/stats.js/build/stats.min.js";
  document.head.appendChild(script);
})();
</script>
