// 📍 API Store
import axios from 'axios'
import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'
import { useAppStore } from '@/store/app';

export const useApiStore = defineStore('api', () => {
  const appStore = useAppStore()

  const shopID = ref(371)                // текущий магазин
  const snapApiCollection = ref([])      // коллекции из API
  const snapApiBoxes = reactive({})      // коробки из API
  const snapApiGoods = reactive({})      // номенклатура из API

  const snapBoxCollection = reactive({}) // коллекции пользовательские
  const snapShopBoxes = reactive({})     // оборудование по магазинам
  const snapShops = reactive({})         // оборудование по магазинам

  const getRequestData = async (url, data) => {
    const res = await axios({ url: url, data: data })
    return res.data.response
  }

  const apiCollections = computed(() => {
    const getHTTP = async () => {
      const req = await getRequestData('get/collections', {})
      if (typeof req === 'object') {
        snapApiCollection.value = req
        return snapApiCollection
      }
    }
    if (snapApiCollection.value.length > 0) {
      return snapApiCollection.value
    }
    getHTTP()
  })

  const apiBoxes = computed(() => {
    const getHTTP = async () => {
      const req = await getRequestData('get/boxes', {})
      if (typeof req === 'object') {
        for (const k in req) {
          snapApiBoxes[k] = req[k]
        }
        return snapApiBoxes
      } else {
        snapApiBoxes["error"] = 'box download error'
      }
    }
    if (typeof snapApiBoxes === 'object' && Object.keys(snapApiBoxes).length > 0) {
      return snapApiBoxes
    }
    getHTTP()
  })

  const shopBoxes = computed(() => {
    const getHTTP = async () => {
      const req = await getRequestData(
        (`shop/${shopID.value}/get/boxes`), {})
      if (typeof req === 'object') {
        for (const k in req) {
          snapShopBoxes[k] = req[k]
        }
        // snapShopBoxes.value = req
        return snapShopBoxes
      } else {
        snapShopBoxes['error'] = 'box download error'
      }
    }
    if (typeof snapShopBoxes === 'object' && Object.keys(snapShopBoxes).length > 0) {
      return snapShopBoxes
    }
    getHTTP()
  })

  // const getBox = (i) => {
  //   return (boxes[i])
  // }
  const moveShopBox = (boxID, x, y, z) => {
    snapShopBoxes[boxID].position.x = x
    snapShopBoxes[boxID].position.y = y
    snapShopBoxes[boxID].position.z = z
  }

  const maxIndexBox = () => {
    const index = ref(1)
    for (const k in snapShopBoxes) {
      if (index.value > snapShopBoxes[k].index) {
        continue
      }
      index.value = snapShopBoxes[k].index + 1
    }
    return Number(index.value)
  }

  const addShopBox = (box) => {
    const postHTTP = async () => {
      const req = await getRequestData((`shop/${shopID.value}/add/box`),
        {
          _id: null,
          index: maxIndexBox() || 9999,
          size: box.size || { x: 10, y: 10, z: 10 },
          position: box.position || { x: 0, y: 0, z: 0 },
          rotation: box.rotation || { x: 0, y: 0, z: 0 },
        }
      )
      if (typeof req === 'object') {
        for (const boxID in req) {
          snapShopBoxes[boxID] = req[boxID]
          appStore.selectBox(boxID)
        }

      }
    }
    postHTTP()
  }

  const updateShopBox = (boxID) => {
    const postHTTP = async (box) => {
      const req = await getRequestData((`shop/${shopID.value}/add/box`), box)
      if (!req) { console.error('not saved') }
    }
    snapShopBoxes[boxID].position.z = 0
    const box = { ...snapShopBoxes[boxID], '_id': boxID }
    postHTTP(box)
  }

  const copyShopBox = (boxID) => {
    const box = snapShopBoxes[boxID]
    addShopBox({
      ...box,
      position: { x: box.position.x, y: box.position.y - box.size.y - 1, z: box.position.z }
    })
  }

  const deleteShopBox = (boxID) => {
    const postHTTP = async (box) => {
      const req = await getRequestData((`delete/box/${boxID}`), box)
      if (!req) { console.error('not saved') }
    }
    const box = snapShopBoxes[boxID]
    postHTTP(box)

    appStore.unoverBox(boxID)
    appStore.isSelectedBox = false
    appStore.selectedBoxID = null
    delete snapShopBoxes[boxID]
  }

  return {
    apiCollections,
    apiBoxes,

    shopBoxes,
    updateShopBox,
    addShopBox,
    moveShopBox,
    copyShopBox,
    deleteShopBox,

    // getBox,
  }
})
