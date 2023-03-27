// Composables
import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('@/layouts/Sandbox.vue'),
    children: [
      {
        path: '',
        name: 'Test',
        component: () => import('@/views/Test.vue'),
      },
      {
        path: 'lights',
        name: 'Lights',
        component: () => import('@/views/Lights.vue'),
      },
      {
        path: 'lightsComp',
        name: 'LightsComposition',
        component: () => import('@/views/LightsComposition.vue'),
      },
      {
        path: 'fbx',
        name: 'FBX',
        component: () => import('@/views/FBX.vue'),
      },
    ],
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
})

export default router
