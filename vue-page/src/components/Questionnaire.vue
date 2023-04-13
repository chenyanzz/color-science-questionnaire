<template>
    <!-- 说明区 -->
    <n-alert title="问卷介绍" type="info" style="margin: 50px;">
        介绍介绍 介绍介绍 介绍介绍 介绍介绍；介绍介绍 介绍介绍 介绍介绍 介绍介绍
    </n-alert>
    <div style="display: flex; justify-content: center; align-items: center;">
        <n-space vertical style="width: 300px;" :size="[0, 100]">
            <!-- 调色区 -->
            <ImageHSBInput v-for="([img,mask], i) in  zip(imgs,masks)" :key="img" :img="img" :mask="mask" @change="(val) => onHSBChange(i, val)" />

            <!-- 个人信息区 -->
            <n-space vertical style="width: 300px;" :size="[0, 10]">
                <div>个人信息</div>
                <n-input v-model:value="zjuid" type="text" placeholder="请输入姓名" />
                <n-input v-model:value="name" type="text" placeholder="请输入ZJU ID" />
            </n-space>
            <n-button type="primary" style="margin-left: 140px;" @click="submit">提交问卷</n-button>

            <div></div>

            <!-- {{ computed(() => JSON.stringify(colors)) }} -->
        </n-space>
    </div>
</template>

<script setup>
import { zip } from 'lodash';
import { ref } from 'vue';
import ImageHSBInput from './ImageHSBInput.vue';

let imgs = [
   "https://s1.ax1x.com/2023/04/13/ppvZEYF.png",
   "https://s1.ax1x.com/2023/04/13/ppverHx.png",
   "https://s1.ax1x.com/2023/04/13/ppveQjs.png",
   "../assets/女2/女2.png",
];
let masks = [
   "https://s1.ax1x.com/2023/04/13/ppvZAFU.png",
   "https://s1.ax1x.com/2023/04/13/ppveyE6.png",
   "https://s1.ax1x.com/2023/04/13/ppveK3Q.png",
   "../assets/女2/女2.png",
];


let colors = new Array(imgs.length).fill({ H: 0, S: 0, B: 0 })
let zjuid = ref('')
let name = ref('')

function onHSBChange(i, hsb) {
    colors[i] = hsb
    console.log(colors)
}

function submit() {
    fetch('xxx/upload', {
        method: 'post',
        mode: 'cors',
        body: JSON.stringify({
            colors,
            zjuid: zjuid.value,
            name: name.value
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(() => {
        alert('提交成功，感谢您的配合！');
    })
}

</script>

<style></style>