// 📍 API Store
import { ref, reactive, computed } from 'vue'
import { defineStore } from 'pinia'

export const useApiStore = defineStore('api', () => {
  const boxes = reactive(
    {
      "64141c50579e718b714edc1d":
      {
        index: 1,
        shopID: "371",
        boxID: "id_box",
        x: 20,
        y: 30,
        h: 0,
        r: 0,
        vendor: "Victoria Stenova",
        collection: "Collection TWO",
        articles: ["999888", "999887", "999886", "999885", "999884", "999883"]
      },
      "64133333579e718b714edc1d":
      {
        index: 2,
        shopID: "371",
        boxID: "id_box",
        x: 10,
        y: 10,
        h: 0,
        r: 0,
        vendor: "Victoria Stenova",
        collection: "Collection ONE",
        articles: ["999888", "999887", "999886", "999885", "999884", "999883"]
      }
    }
  )

  const getBox = (i) => {
    return (boxes[i])
  }

  const moveBox = (i, x, y, h) => {
    boxes[i].update({x: x, y: y, h: h})
  }

  const addBox = () => {
    boxes[Math.random() * 10] = {
        index: 2,
        shopID: "371",
        boxID: "id_box",
        x: 0,
        y: 0,
        h: 0,
        r: 0,
        vendor: "",
        collection: "",
        articles: []
    }
  }


  return {
    boxes,
    getBox,
    moveBox,
    addBox,
  }
})
