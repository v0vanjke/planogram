// 📍 Main App Store
import { ref, watch, computed } from "vue";
import { defineStore } from "pinia";
import { useApiStore } from "@/store/api";

export const useAppStore = defineStore("app", () => {
  const apiStore = useApiStore();

  //📍 Mouse ClickHandler
  const eventMouseUp = (event) => {
    if (mode.value === "roomPlanner") {
      // Режим - ОБОРУДОВАНИЕ
      if (event.button === 0) {
        // Левая кнопка
        roomPlannerSubmenu.value = false;
      }
      if (event.button === 2) {
        if (overBoxID.value.length > 0) {
          roomPlannerSubmenu.value = !roomPlannerSubmenu.value;
        } else {
          roomPlannerSubmenu.value = false;
        }
      }
    }
    if (mode.value === "goodsPlanner") {
      // Режим - Номенклатура
    }
  };
  const eventMouseDown = (event) => {
    if (mode.value === "roomPlanner") {
      // Режим - ОБОРУДОВАНИЕ
      if (event.button === 0) {
        // Левая кнопка
        if (selectedBoxID.value) {
          // бросить Box
          unselectBox();
        } else if (!selectedBoxID.value && overBoxID.value.length > 0) {
          // Схватить первый попавшийся Box
          selectBox();
        }
      }
      if (event.button === 2) {
      }
    }
    if (mode.value === "goodsPlanner") {
      // Режим - Номенклатура
      if (event.button === 0) {
        if (selectedCollectionID.value) {
          unselectCollection();
        } else if (
          !selectedCollectionID.value &&
          overCollectionID.value.length > 0
        ) {
          selectCollection();
        }
      }
    }
  };
  //📍 MODE
  // roomPlanner -
  // goodsPlanner -
  // const mode = ref('roomPlanner')
  const mode = ref("goodsPlanner");
  const changeMode = (m) => {
    mode.value = m;
  };

  //📍 CAMERA
  // const cameraCtrl = ref(null)
  const cameraAzimuth = ref(0);
  // const updateCameraCtrl = (val) => {
  //   cameraCtrl.value = val
  // }

  const orbCtrlSettings = {
    autoRotate: false,
    enableDamping: true,
    enableRotate: true,
    dampingFactor: 0.05,

    maxPolarAngle: 1.4,
    minPolarAngle: 0.01,

    minDistance: 50,
    maxDistance: 500,

    // minAzimuthAngle: -1.56,
    // maxAzimuthAngle: 1.56,
  };

  // Over Collection
  const overCollectionID = ref([]);
  const overCollection = (collectionID) => {
    overCollectionID.value.push(collectionID);
  };
  const unoverCollection = (collectionID) => {
    overCollectionID.value.splice(
      overCollectionID.value.indexOf(collectionID),
      1
    );
  };

  //📍 Over Box
  const overBoxID = ref([]);
  const overBox = (boxID) => {
    overBoxID.value.push(boxID);
  };
  const unoverBox = (boxID) => {
    overBoxID.value.splice(overBoxID.value.indexOf(boxID), 1);
  };

  //📍 Selected Boxes
  const isSelectedBox = ref(false);
  const selectedBoxID = ref(null);
  const selectBox = (boxID) => {
    selectedBoxID.value = boxID || overBoxID.value[0];
    isSelectedBox.value = true;
  };
  const deleteBox = () => {
    isSelectedBox.value = false;
    selectedBoxID.value = null;
  };
  const unselectBox = () => {
    // save
    apiStore.updateShopBox(selectedBoxID.value);
    isSelectedBox.value = false;
    selectedBoxID.value = null;
  };

  //📍 Collection
  const selectedCollectionCategory = ref("Обои");
  const selectedCollectionVendor = ref("Victoria Stenova");
  // in box
  const apiCollectionFiltered = computed(() => {
    const result = [];
    if (!apiStore.apiCollections) return result;
    // filter objects by category and vendor
    for (const el of apiStore.apiCollections) {
      if (
        el.category === selectedCollectionCategory.value &&
        el.vendor === selectedCollectionVendor.value
      ) {
        result.push(el);
      }
    }
    // return array of objects sorted by key (name)
    return result.sort((a, b) => {
      if (a.name < b.name) return -1;
      if (a.name > b.name) return 1;
    });
  });

  const isSelectedCollection = ref(false);
  const selectedCollectionID = ref(null);
  const selectCollection = (collectionID) => {
    selectedCollectionID.value = collectionID || overCollectionID.value[0];
    // selectedCollectionID.value.push(overCollectionID.value[0]);
    isSelectedCollection.value = true;
  };
  const unselectCollection = () => {
    // save
    apiStore.updateShopCollection(selectedCollectionID.value);
    isSelectedCollection.value = false;
    selectedCollectionID.value = null;
  };

  //📍 Submenu
  const roomPlannerSubmenu = ref(false);
  watch(
    () => overBoxID.value[0],
    (state) => {
      if (state) {
        roomPlannerSubmenu.value = false;
      }
    }
  );

  return {
    mode,
    changeMode,
    roomPlannerSubmenu,

    cameraAzimuth,
    orbCtrlSettings,
    eventMouseUp,
    eventMouseDown,

    overBoxID,
    overBox,
    unoverBox,

    overCollectionID,
    overCollection,
    unoverCollection,

    isSelectedBox,
    selectedBoxID,
    selectBox,
    unselectBox,
    deleteBox,

    selectedCollectionCategory,
    selectedCollectionVendor,
    apiCollectionFiltered,

    isSelectedCollection,
    selectedCollectionID,
    selectCollection,
    unselectCollection,
  };
});
