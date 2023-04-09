// 📍 Collection - коллекции товара
<script setup>
import { ref, computed, onMounted } from "vue"
import {
    Box,
    Circle,
    Group,
    LambertMaterial,
    Text,
    Plane,
    RectAreaLight,
} from 'troisjs';
// import Article from '@/components/Article';
import { useApiStore } from '@/store/api';
import { useAppStore } from '@/store/app';
const apiStore = useApiStore()
const appStore = useAppStore()

const props = defineProps({
    id: {
        default: "",
        type: String,
        required: true,
    },
    size: {
        default: { x: 1.1, y: 0.3, z: 0.3 },
        type: Object,
        required: false,
    }
})

const data = computed(() => {
    return apiStore.shopCollections[props.id]
})


//📍 SELECT
const isSelected = computed(() => {
    if (appStore.selectedCollectionID === props.id) {
        return true
    }
    return false
})

//📍 OVER
const isOver = computed(() => {
    if (appStore.overCollectionID[0] === props.id) {
        return true
    }
    return false
})

const eventOver = (val) => {
    if (val.over === false) {
        appStore.unoverCollection(props.id)
    } else {
        appStore.overCollection(props.id)
    }
}

//📍 COLOR
// const fillerColor = () => {
//   return 'hsl(27, 35%, 30%)'
//   // return 'hsl(0, 0%, 30%)'
// }
//
// const wallColor = () => {
//   // if (isSelected.value) {return 'hsl(80, 80%, 15%)'}
//   if (isOver.value && !isSelected.value) {return 'hsl(30, 100%, 20%)'}
//   return 'hsl(0, 0%, 10%)'
//   // return 'hsl(27, 35%, 30%)'
// }
//
// const backWallColor = () => {
//   // if (isSelected.value) {return 'hsl(80, 80%, 15%)'}
//   if (isOver.value && !isSelected.value) {return 'hsl(30, 100%, 20%)'}
//   return 'hsl(0, 0%, 10%)'
//   // return 'hsl(27, 35%, 30%)'
// }
// const shadowBoxColor = () => {
//   return 'hsl(195, 80%, 10%)'
// }
// const shadowBorderColor = () => {
//   return 'hsl(95, 100%, 30%)'
// }
//
// const numberColor = () => {
//   return 'hsl(200, 30%, 20%)'
// }
//
const collectionColor = () => {
    return 'hsl(0, 100%, 50%)'
}


//📍 BOX SIZES
const computedX = computed(() => {
    return props.size.x
})
const computedY = computed(() => {
    return props.size.y
})
const computedZ = computed(() => {
    return props.size.z
})

</script>

<template>
    <Group :position="{ ...data.position, z: data.position.z + computedZ / 2 }">
        <Box :width=10 :height=10 :depth=10>
            <LambertMaterial :color="collectionColor()" />
        </Box>
    </Group>
</template>

<style scoped>
</style>
