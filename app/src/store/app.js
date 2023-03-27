// 📍 Main App Store
import { ref, reactive, onMounted } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {

  const pointerV3 = ref({})

  // CAMERA
  const orbCtrl = reactive({
    autoRotate: false,
    enableDamping: true,
    enableRotate: true,
    dampingFactor: 0.05,

    maxPolarAngle: 1,

    minDistance: 50,
    maxDistance: 300,

    minAzimuthAngle: -1.56,
    maxAzimuthAngle: 1.56,

  })
  const enableRotate = () => {
    orbCtrl.enableRotate = true
  }
  const disableRotate = () => {
    orbCtrl.enableRotate = false
  }

  return {
    orbCtrl,
    enableRotate,
    disableRotate,
    pointerV3
  }
})
