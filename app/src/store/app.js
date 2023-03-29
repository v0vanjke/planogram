// 📍 Main App Store
import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'

export const useAppStore = defineStore('app', () => {

  // CAMERA
  const orbCtrlSettings = {
    autoRotate: false,
    enableDamping: true,
    enableRotate: true,
    dampingFactor: 0.05,

    maxPolarAngle: 1,
    minPolarAngle: 0.01,

    minDistance: 50,
    maxDistance: 300,

    minAzimuthAngle: -1.56,
    maxAzimuthAngle: 1.56,

  }

  const overBoxID = ref(null)
  const overBox = (boxID) => {
    overBoxID.value = boxID
  }
  const unoverBox = () => {
    overBoxID.value = null
  }


  const selectedBoxId = ref([])
  const selectBox = (boxID) => {
    selectedBoxId.value.push(boxID)
  }
  const unselectBox = (boxID) => {
    if (selectedBoxId.value.includes(boxID)) {
      selectedBoxId.value.splice(selectedBoxId.value.indexOf(boxID), 1)
    }
  }
  const isSelectedBox = computed(() => {
    if (selectedBoxId.value.length === 0) {
      return false
    }
    return true
  })

  const cameraCtrl = ref(null)
  const updateCameraCtrl = (val) => {
    cameraCtrl.value = val
  }


  return {
    cameraCtrl,
    updateCameraCtrl,

    overBoxID,
    overBox,
    unoverBox,

    selectedBoxId,
    selectBox,
    unselectBox,
    isSelectedBox,

    orbCtrlSettings,
  }
})
