// 📍 Обработчик ошибок
// show           - видимость
// add(data)      - добавить новую ошибку
//
import { defineStore } from 'pinia'
import { ref } from 'vue'


export const useErrStore = defineStore('err', () => {
  // 📍 Data
  const id = ref(0)
  const show = ref(false)
  const template = {
    title: '',
    message: '',
    level: 'info',
    from: ''
  }
  const data = ref({...template})

  // 📍 Functions
  const add = (newData) => {
    show.value = false
    if (!(typeof newData === 'object')) {
      console.log('ошибка должна быть object а не вот это вот', newData)
      return
    }
    data.value = {...template, ...newData}
    show.value = true
    id.value++
  }

  return {
    show, data, add, id
  }

})
