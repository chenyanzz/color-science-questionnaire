<template>
    <!-- 说明区 -->
    <n-alert title="问卷介绍" type="info" style="margin: 50px;">
        感谢您在百忙之中抽空完成此问卷，请您拖动每张图片下方的3个控制条，使得每张图片的人物「肤色」达到您最喜欢的效果并提交，感谢您的配合。
    </n-alert>
    <div style="display: flex; justify-content: center; align-items: center;">
        <n-space vertical style="width: 300px;" :size="[0, 100]">
            <!-- 调色区 -->
            <h3>【肤色调节】</h3>
            <ImageHSBInput v-for="([img, mask], i) in zip(imgs, masks)" :key="img" :img="img" :mask="mask"
                @change="(val) => onHSBChange(i, val)" />

            <!-- 个人信息区 -->
            <n-space vertical style="width: 300px;" :size="[0, 10]">
                <h3>【个人信息】</h3>
                <n-space align="center">
                    <div>姓名</div>
                    <n-input v-model:value="name" type="text" placeholder="请输入姓名" />
                </n-space>
                <n-space align="center">
                    <div>性别</div>
                    <n-radio :checked="gender === '男'" value="男" name="gender" @change="onGenderChange">男</n-radio>
                    <n-radio :checked="gender === '女'" value="女" name="gender" @change="onGenderChange">女</n-radio>
                </n-space>
                <n-space align="center">
                    <div>年龄</div>
                    <n-input-number v-model:value="age" />
                </n-space>


                <div style="height: 25px;"></div>
                <n-button type="primary" style="display: inline; text-align: center;" @click="submit">提交问卷</n-button>
                <h3 v-if="submitted" style="color: sienna;">提交成功！您可以关闭页面了</h3>
                <div style="height: 50px;"></div>
                <!-- {{ computed(() => JSON.stringify(colors)) }} -->
            </n-space>
        </n-space>
    </div>
</template>

<script setup>
import { zip } from 'lodash';
import { ref } from 'vue';
import ImageHSBInput from './ImageHSBInput.vue';

let imgs = [
    "https://cystudio.tech/static/faces/p1.png",
    "https://cystudio.tech/static/faces/p2.png",
    "https://cystudio.tech/static/faces/p3.png",
    "https://cystudio.tech/static/faces/p4.png",
];
let masks = [
    "https://cystudio.tech/static/faces/p1m.png",
    "https://cystudio.tech/static/faces/p2m.png",
    "https://cystudio.tech/static/faces/p3m.png",
    "https://cystudio.tech/static/faces/p4m.png",
];


let colors = new Array(imgs.length).fill({ H: 0, S: 0, B: 0 })
let name = ref('')
let gender = ref('男')
let age = ref(18)
let submitted = ref(false)

function onHSBChange(i, hsb) {
    colors[i] = hsb
    console.log(colors)
}

function onGenderChange(e) {
    gender.value = e.target.value
}

function submit() {
    fetch('https://cystudio.tech/color-science/upload', {
        method: 'post',
        mode: 'cors',
        body: JSON.stringify({
            colors,
            name: name.value,
            age: age.value,
            gender: gender.value,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then((response) => {
        submitted.value = true;
        if (response.ok) alert('提交成功，感谢您的配合！');
        else alert('提交出错！');
    }).catch(()=>alert('提交出错！'))
}

</script>

<style></style>