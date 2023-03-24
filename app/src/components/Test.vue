<template>
  <v-card height="1200">
  <Renderer ref="renderer" antialias :orbit-ctrl="{ enableDamping: true, target }"
            resize shadow>
    <Camera :position="{ x: 0, y: 300, z: 0 }" />
    <Scene ref="scene" background="hsl(0, 0%, 30%)">
      <HemisphereLight />
      <DirectionalLight
        :position="{ x: 0, y: 300, z: 100 }"
      />
      <Group :rotation="{ x: -Math.PI / 2 }">
        <Box :width=11 :height=4 :depth=16 :position="{x: 20, y: 20, z: 8}">
          <PhysicalMaterial color="red"  :props="{ transparent: true, opacity: 0.7 }" />
        </Box>
        <Box :width=11 :height=4 :depth=16 :position="{x: 0, y: 0, z: 8}" >
          <PhysicalMaterial color="blue"  :props="{ transparent: true, opacity: 0.7 }" />
        </Box>
        <Box :width=9 :height=4 :depth=16 :position="{x: 20, y: 19, z: 9}">
          <PhysicalMaterial color="white"  :props="{ opacity: 0.7 }" />
        </Box>
      </Group>
      <Plane :width="300" :height="300" :rotation="{ x: -Math.PI / 2 }" receive-shadow>
        <PhongMaterial color="#999999" :props="{ depthWrite: false }" />
      </Plane>

    </Scene>
  </Renderer>
  </v-card>
  <div class="bg-grey">
    .
  {{mouse}}
  </div>
</template>

<script>
// Model from mixamo.com
import { GridHelper, Vector3 } from 'three';
import {
  Group,
  Box,
  Camera,
     PhysicalMaterial,
  DirectionalLight,
  HemisphereLight,
  Renderer,
  PhongMaterial,
  Plane,
  Scene,
} from 'troisjs';

export default {
  components: {
  Group,
  Box,
     PhysicalMaterial,
    Camera,
    DirectionalLight,
    HemisphereLight,
    Renderer,
    PhongMaterial,
    Plane,
    Scene,
  },
  data() {
    return {
      target: new Vector3(0, 0, 0),
      mouse: {},
    };
  },
  computed: {
  },
  mounted() {
    const grid = new GridHelper(300, 30, "hsl(120, 100%, 80%)", "hsl(0, 1%, 92%)");
    grid.material.opacity = 0.9;
    grid.material.transparent = true;
    this.$refs.scene.add(grid);

    const renderer = this.$refs.renderer;
    // const pointerV3 = renderer.three.pointer.positionV3;
    renderer.onBeforeRender(() => {
      console.log(renderer.three)
    });

  },
  methods: {
  },
};
</script>