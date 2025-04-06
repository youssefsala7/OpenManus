<template>
  <div>
    <el-card class="index" body-style="height: 100%;" v-show="view == 'index'">
      <div class="fc hp-100">
      <div class="fxe mr-10 wp-100">
        <el-link type="primary" @click="toDocs" size="large"> {{ t('docs') }} </el-link>
      </div>


      <div class="body-content">
      <div class="welcome">
        <el-text tag="h1">{{ t('welcomeUseOpenManus') }}</el-text>
      </div>

      <div class="fxc">
        <img src="@/assets/img/logo-w.png" width="400" alt="OpenManus" v-if="isDark">
        <img src="@/assets/img/logo-b.png" width="400" alt="OpenManus" v-if="!isDark">
      </div>

      <div class="welcome">
        <el-text tag="h4" class="text-indent">{{ t('welcomeUseOpenManusTips') }}</el-text>
      </div>

      <div class="fxc mtb-20">
        <el-button type="primary" @click="getStarted" size="large"> {{ t('getStarted') }} </el-button>
      </div>
    </div>
    </div>
    </el-card>

    <el-card class="mb-0" v-show="view == 'docs'">
      <el-scrollbar>
        <div class="fxe mr-10">
          <el-link type="primary" @click="toIndex" size="large"> {{ t('homePage') }} </el-link>
        </div>
        <div class="mt-20" v-html="readme"> </div>
      </el-scrollbar>
    </el-card>
  </div>

</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from "vue-router"
import { useConfig } from '@/store/config'
import { useI18n } from 'vue-i18n'
import { marked } from 'marked'
import { useDark } from '@vueuse/core'

const router = useRouter()
const config = useConfig()
const { t } = useI18n()
const isDark = useDark()

const readme = ref('')

const langList = ref(config.langList)

const selectedLang = ref(config.selectedLang != null ? config.selectedLang : langList.value[0])

const view = ref('index')

function toDocs() {
  view.value = 'docs'
}

function toIndex() {
  view.value = 'index'
}

onMounted(async () => {
  const readmeMd = await import('@/assets/md/README.md?raw')
  const readmeZhMd = await import('@/assets/md/README_zh.md?raw')
  console.log("readmeZhMd:", readmeZhMd)
  readme.value = marked(selectedLang.value == 'zhCn' ? readmeZhMd.default : readmeMd.default)
})

function getStarted() {
  router.push({ path: '/config/init' })
}

</script>

<style scoped>
.index {
  min-height: 540px;
  height: 100vh;
  margin-bottom: 0px;
}

.body-content {
 flex-grow: 1;
 display: flex;
 flex-direction: column;
 justify-content: center;
 align-items: center;
}

.welcome {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
</style>
