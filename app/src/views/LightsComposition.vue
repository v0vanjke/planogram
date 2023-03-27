<script setup>
import { ref, onMounted } from 'vue';
import { RepeatWrapping } from 'three';
import {
  AmbientLight,
  Camera,
  EffectComposer,
  FXAAPass,
  Group,
  Renderer,
  Plane,
  Box,
  PointLight,
  RectAreaLight,
  RenderPass,
  Scene,
  Sphere,
  StandardMaterial,
  Texture,
  UnrealBloomPass,
} from 'troisjs';

const texturesProps = {
        repeat: { x: 10, y: 10 },
        wrapS: RepeatWrapping,
        wrapT: RepeatWrapping,
      }

const rectLightsProps = {
        // rotation: { x: -Math.PI / 2 },
        lookAt: { x: 0, y: 0, z: 1 },
        intensity: 5,
        width: 5,
        height: 5,
        helper: true,
      }

const renderer = ref(null)
const light = ref(null)

onMounted(() => {
  const pointerV3 = renderer.value.three.pointer.positionV3
    renderer.value.onBeforeRender(() => {
      console.log(renderer.value.three, pointerV3)
  })
})

</script>

<template>
    <Renderer ref="renderer" resize antialias pointer :orbit-ctrl="{ autoRotate: false, enableDamping: true, dampingFactor: 0.05 }" >
      <Camera :position="{ x: 0, y: 0, z: 10 }" />
      <Scene background="#000000" >
        <!-- <AmbientLight color="red" /> -->
        <PointLight ref="light" :intensity="0.5" :position="{ x: 0, y: 0, z: 0 }">
          <Sphere :radius="0.1" />
        </PointLight>
        <Group :rotation="{ x: -Math.PI / 2, y: 0, z: 0 }">
          <Box :position="{ x: 0, y: 10, z: 1 }" />
          <RectAreaLight color="#0060ff" :position="{ x: 10, y: 0, z: 1 }" v-bind="rectLightsProps" />
          <RectAreaLight color="#60ff60" :position="{ x: -10, y: 0, z: 1 }" v-bind="rectLightsProps" />
          <RectAreaLight color="orange" :position="{ x: 0, y: -10, z: 1 }" v-bind="rectLightsProps" />
          <Plane :width="30" :height="30" :rotation="{ x: 0 }" :position="{ z: -3 }">
            <StandardMaterial :props="{ displacementScale: 0.2, roughness: 0, metalness: 0 }"  >
              <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_basecolor.jpg" />
              <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_height.png" name="displacementMap" />
              <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_normal.jpg" name="normalMap" />
              <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_roughness.jpg" name="roughnessMap" />
              <Texture :props="texturesProps" src="https://troisjs.github.io/assets/textures/Wood_Tiles_002_ambientOcclusion.jpg" name="aoMap" />
            </StandardMaterial>
          </Plane>
        </Group>
      </Scene>
      <EffectComposer>
        <RenderPass />
        <UnrealBloomPass :strength="0.5" />
        <FXAAPass />
      </EffectComposer>
    </Renderer>
</template>
