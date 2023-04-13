<template>
  <n-space vertical id="container">

    <div style="display: flex; align-items: center; justify-items: center;">
      <n-spin v-show="!loaded" size="large" />
      <img width="300" v-show="loaded" :src="mask"
        :style="{ filter: `brightness(${B}%) saturate(${S}%) hue-rotate(${H}deg) `, marginRight: '-100%', zIndex: 1 }" @load="onLoadImg">
      <img width="300" v-show="loaded" :src="img" style="z-index: 0;" @load="onLoadImg"/>
    </div>
    <slider-area>
      <n-tag> 色调 </n-tag>
      <div style="display: block; width: 20px;" />
      <n-slider v-model:value="h" :step="1" :format-tooltip="() => `${H.toFixed(2)}deg`"
        :on-update:value="(val) => { h = val; onChange() }" />
    </slider-area>
    <slider-area>
      <n-tag> 饱和 </n-tag>
      <div style="display: block; width: 20px;" />
      <n-slider v-model:value="s" :step="1" :format-tooltip="() => `${S.toFixed(2)}%`"
        :on-update:value="(val) => { s = val; onChange() }" />
    </slider-area>
    <slider-area>
      <n-tag> 亮度 </n-tag>
      <div style="display: block; width: 20px;" />
      <n-slider v-model:value="b" :step="1" :format-tooltip="() => `${B.toFixed(2)}%`"
        :on-update:value="(val) => { b = val; onChange() }" />
    </slider-area>
    <n-button @click="resetHSB">重置颜色</n-button>
  </n-space>
</template>

<script setup>

import { computed, defineEmits, defineProps, ref } from 'vue';

defineProps({
  img: String,
  mask: String
});
const emit = defineEmits(['change']);

// slider  value [0,100]
let h = ref(0)
let s = ref(0)
let b = ref(0)

// filter parameter
let H = computed(() => (h.value - 50) * 0.5) // deg
let S = computed(() => 100 + (s.value - 50)) // %
let B = computed(() => 100 + (b.value - 50) * 0.5) // %

resetHSB()

function resetHSB() {
  h.value = 50
  s.value = 50
  b.value = 50
  onChange()
}

function onChange() {
  // console.log('hsb-change-value')
  emit('change', { "H": H.value, "S": S.value, "B": B.value })
}

let cnt_load_img = ref(0)
let loaded = computed(()=>cnt_load_img.value==2)
function onLoadImg(){
  cnt_load_img.value++
}


let loading = ref(true)

loading.value = false;

</script>

<style>
#container {
  width: 300px;
}

slider-area {
  width: 300px;
  display: flex;
  align-items: center;
  justify-content: space-around;
}
</style>
