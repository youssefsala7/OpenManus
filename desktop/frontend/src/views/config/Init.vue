<template>
  <div class="main-content">
    <el-card>
      <template #header>
        <div class="title fxsb">
          <div>{{ t('initConfig') }}</div>
        </div>
      </template>

      <!-- Show Data -->
      <el-steps direction="vertical" :active="stepActive">
        <el-step title="Step 1" :status="initCheck.envLib ? 'success' : 'wait'">
          <template #description>
            <el-card class="mtb-10">
              <div class="fxsb min-h32">
                <div>
                  <el-text class="pr-10">{{ t('envLibDownload') }}:</el-text>
                  <el-text>
                    {{ envLibDownloadLoading ? t('envLibDownloading')
                      : (initCheck.envLib ? t('checkedPass') : t('checkedFailed')) }}
                  </el-text>
                </div>
                <el-button type="primary" class="mlr-10" @click="envLibDownload"
                  v-show="!initCheck.envLib && !envLibDownloadLoading">
                  {{ t('envLibDownload') }}
                </el-button>
              </div>

              <div class="wp-100" v-show="!envLibDownloadLoading">
                <el-progress :percentage="envLibDownloadProgress.percentage" :stroke-width="15"
                  :status="envLibDownloadProgress.status" striped
                  :striped-flow="envLibDownloadProgress.status != 'success'" :duration="10" class="mtb-10" />
                <div class="wp-100">
                  <el-text class="download-progress-tips">{{ t('envLibDownloadTips') }}</el-text>
                  <el-text class="download-progress-tips max-w-500" truncated>
                    {{ envLibDownloadProgress.text }}
                  </el-text>
                </div>
              </div>
            </el-card>
          </template>
        </el-step>

        <el-step title="Step 2" :status="initCheck.serverConfig ? 'success' : 'wait'">
          <template #description>
            <el-card class="mtb-10">
              <template #header>
                <div class="fxsb">
                  <div>
                    <el-text class="pr-10">{{ t('serverConfig') }}:</el-text>
                    <el-text>{{ initCheck.serverConfig ? t('checkedPass') : t('checkedFailed') }}</el-text>
                  </div>
                  <el-link type="primary" class="mlr-10" @click="toEdit('server')">{{ t('edit') }}</el-link>
                </div>
              </template>

              <!-- Show Data -->
              <div class="card-row-wrap" v-show="serverShow">
                <div class="card-row-item">
                  <el-text>host:</el-text>
                  <el-text>{{ serverConfig.host }}</el-text>
                </div>

                <div class="card-row-item">
                  <el-text>port:</el-text>
                  <el-text tag="p">{{ serverConfig.port }}</el-text>
                </div>
              </div>

              <!-- Edit Data -->
              <el-form ref="ruleFormRef" :model="serverConfigUpd" status-icon :rules="rules" v-show="serverEdit">
                <div class="card-row-wrap">
                  <div class="card-row-item">
                    <el-text>{{ t('step2') }}</el-text>
                    <el-form-item prop="host">
                      <el-input v-model="serverConfigUpd.host" />
                    </el-form-item>
                  </div>

                  <div class="card-row-item">
                    <el-text>port:</el-text>
                    <el-form-item prop="port">
                      <el-input v-model="serverConfigUpd.port" />
                    </el-form-item>
                  </div>

                  <div class="card-row-aline fxc" v-show="serverEdit">
                    <el-button class="mlr-10" @click="toShow('server')">{{ t('cancel') }}</el-button>
                    <el-button type="primary" class="mlr-10" @click="submitServerConfig">{{ t('submit') }}</el-button>
                  </div>
                </div>
              </el-form>
            </el-card>
          </template>
        </el-step>

        <el-step title="Step 3" :status="initCheck.llmConfig ? 'success' : 'wait'">
          <template #description>
            <el-card class="mtb-10">
              <template #header>
                <div class="fxsb">
                  <div>
                    <el-text class="pr-10">{{ t('llmConfig') }}:</el-text>
                    <el-text>{{ initCheck.llmConfig ? t('checkedPass') : t('checkedFailed') }}</el-text>
                  </div>
                  <div>
                    <el-link type="primary" class="no-select plr-6" @click="toEdit('llm')" v-show="llmShow">
                      {{ t('edit') }}
                    </el-link>
                    <el-link type="primary" class="no-select plr-6" @click="toShow('llm')" v-show="llmEdit">
                      {{ t('cancel') }}
                    </el-link>
                  </div>
                </div>
              </template>

              <!-- Show Data -->
              <div class="card-row-wrap" v-show="llmShow">
                <div class="card-row-item">
                  <el-text>model:</el-text>
                  <el-text>{{ llmConfig.model }}</el-text>
                </div>

                <div class="card-row-item">
                  <el-text>base_url:</el-text>
                  <el-text tag="p">{{ llmConfig.base_url }}</el-text>
                </div>

                <div class="card-row-item">
                  <el-text>api_key:</el-text>
                  <el-text>{{ llmConfig.api_key }}</el-text>
                </div>

                <div class="card-row-item">
                  <el-text>max_tokens:</el-text>
                  <el-text>{{ llmConfig.max_tokens }}</el-text>
                </div>

                <div class="card-row-item">
                  <el-text>temperature:</el-text>
                  <el-text>{{ llmConfig.temperature }}</el-text>
                </div>
              </div>

              <!-- Edit Module -->
              <el-form ref="ruleFormRef" :model="llmConfigUpd" status-icon :rules="rules" v-show="llmEdit">
                <div class="card-row-wrap">
                  <div class="card-row-item">
                    <el-text>model:</el-text>
                    <el-form-item prop="model">
                      <el-input v-model="llmConfigUpd.model" />
                    </el-form-item>
                  </div>

                  <div class="card-row-item">
                    <el-text>base_url:</el-text>
                    <el-form-item prop="base_url">
                      <el-input v-model="llmConfigUpd.base_url" />
                    </el-form-item>
                  </div>

                  <div class="card-row-item">
                    <el-text>api_key:</el-text>
                    <el-form-item prop="api_key">
                      <el-input v-model="llmConfigUpd.api_key" />
                    </el-form-item>
                  </div>

                  <div class="card-row-item">
                    <el-text>max_tokens:</el-text>
                    <el-form-item prop="max_tokens">
                      <el-input v-model="llmConfigUpd.max_tokens" />
                    </el-form-item>
                  </div>

                  <div class="card-row-item">
                    <el-text>temperature:</el-text>
                    <el-form-item prop="temperature">
                      <el-input v-model="llmConfigUpd.temperature" />
                    </el-form-item>
                  </div>

                  <div class="card-row-aline fxc" v-show="llmEdit">
                    <el-button class="mlr-10" @click="toShow('llm')">{{ t('cancel') }}</el-button>
                    <el-button type="primary" class="mlr-10" @click="submitLlmConfig">{{ t('submit') }}</el-button>
                  </div>
                </div>
              </el-form>
            </el-card>
          </template>
        </el-step>
      </el-steps>

    </el-card>

    <el-card v-show="initCheckPass">
      <div class="fxc mtb-20">
        <el-button type="primary" @click="startTheExperience" size="large"> {{ t('startTheExperience') }} </el-button>
      </div>
    </el-card>

  </div>

</template>

<script setup>
import { ref, reactive, inject, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useConfig } from '@/store/config'
import { useI18n } from 'vue-i18n'
import { EventsEmit, EventsOff, EventsOn } from '../../../wailsjs/runtime/runtime'

const utils = inject('utils')
const verify = inject('verify')
const files = inject('files')
const router = useRouter()
const config = useConfig()
const { t } = useI18n()

// 视图模式
const viewModel = reactive({
  env: 'show',
  server: 'show',
  llm: 'show',
})

function toShow(model) {
  console.log("toShow:" + model)
  viewModel[model] = 'show'
}

function toEdit(model) {
  console.log("toEdit:" + model)
  viewModel[model] = 'edit'
}

const envShow = computed(() => {
  return viewModel.env == 'show'
})

const envEdit = computed(() => {
  return viewModel.env == 'edit'
})

const serverShow = computed(() => {
  return viewModel.server == 'show'
})

const serverEdit = computed(() => {
  return viewModel.server == 'edit'
})

const llmShow = computed(() => {
  return viewModel.llm == 'show'
})

const llmEdit = computed(() => {
  return viewModel.llm == 'edit'
})

const readConfigSuccess = ref(true)

const serverConfig = reactive({
  host: null,
  port: null,
})

const serverConfigUpd = reactive({
  host: null,
  port: null,
})


const llmConfig = reactive({
  model: null,
  base_url: null,
  api_key: null,
  max_tokens: null,
  temperature: null,
})

const llmConfigUpd = reactive({
  model: null,
  base_url: null,
  api_key: null,
  max_tokens: null,
  temperature: null,
})

const initCheck = reactive({
  envLib: true,
  serverConfig: false,
  llmConfig: false,
})

const envLibDownloadProgress = reactive({
  status: null,
  percentage: 0,
  text: '豆腐干豆腐干豆腐干豆腐干地方 人地方官梵蒂冈的豆腐干豆腐干地方 人地方官梵蒂冈的豆腐干豆腐干地方 人地方官梵蒂冈的豆腐干豆腐干地方 人地方官梵蒂冈的豆腐干豆腐干地方 人地方官梵蒂冈的豆腐干豆腐干地方 人地方官梵蒂冈的豆腐干豆腐干地方 人地方官梵蒂冈的豆腐干豆腐干地方 人地方官梵蒂冈的豆腐干豆腐干地方 人地方官梵蒂冈的豆腐干豆腐干地方 人地方官梵蒂冈的地方 人地方官梵蒂冈的',
})

function envLibCheck() {
  const envLibPath = appDataPath.value + "\\venv"
  files.pathExists(envLibPath).then((exists) => {
    console.log('envLibPath exists: ', exists)
    if (exists) {
      initCheck.envLib = true
      return
    } else {
      initCheck.envLib = false
      return
    }
  })
}

const envLibDownloadLoading = ref(false)

function envLibDownload() {
  const runBatPath = appDataPath.value + "\\run.bat"
  if (EventsEmit) {
    // 触发执行bat命令事件给后台
    console.log('EventsEmit: ', EventsEmit)
    EventsEmit('bat', 'ExecRunBat', runBatPath)
    envLibDownloadLoading.value = true
    venvFolderSizeCheck()
  }

}

async function venvFolderSizeCheck() {
  const targetSize = 1024 * 1024 * 1024 * 2 // 2GB
  // 检测venv文件夹大小, 计算百分比
  const envLibPath = appDataPath.value + "\\venv"
  await files.awaitDirSize(envLibPath).then((size) => {
    console.log('envLibPath size: ', size)
    const percentage = Math.floor((size / targetSize) * 100)
    if (envLibDownloadProgress.percentage < percentage) {
      envLibDownloadProgress.percentage = percentage
    }
    console.log('envLibDownloadProgress.percentage: ', envLibDownloadProgress.percentage)
    if (envLibDownloadProgress.percentage >= 100) {
      envLibDownloadProgress.percentage = 99
    }
  })
  // 递归检测
  if (envLibDownloadLoading.value && envLibDownloadProgress.percentage < 100) {
    setTimeout(() => {
      venvFolderSizeCheck()
    }, 300)
  }
}

const appDataPath = ref()

onMounted(async () => {
  await files.awaitAppPath().then((path) => {
    appDataPath.value = path
    console.log('appDataPath: ', appDataPath.value)
    if (appDataPath.value && appDataPath.value.endsWith('\\desktop\\build\\bin')) {
      appDataPath.value = appDataPath.value.replace('\\desktop\\build\\bin', '')
    }
    console.log('appDataPath: ', appDataPath.value)
  })
  // 读取配置文件config/config.toml
  loadConfig()

  // 监听后台执行bat命令事件
  EventsOn('ExecRunBat', (type, data) => {
    console.log('bat cmd exc: ', type, data)
    envLibDownloadLoading.value = true
    if (type == 'msg') {
      envLibDownloadProgress.text = data
    }
    if (data.startsWith('Press any key to continue')
      || (data.endsWith('. . .') && envLibDownloadProgress.percentage >= 99)) {
      // data.endsWith('. . .') 兼容中文环境下的bat命令输出
      console.log('envLib download finished')
      envLibDownloadLoading.value = false
      envLibDownloadProgress.percentage = 100
      envLibDownloadProgress.status = 'success'
      envLibDownloadProgress.text = t('envLibDownloadSuccess')
      initCheck.envLib = true
      utils.pop(t('envLibDownloadSuccess'))
    }
  })

  // 检查环境
  envLibCheck()
})

const stepActive = computed(() => {
  if (!initCheck.envLib) {
    return 0
  }
  if (!initCheck.serverConfig) {
    return 1
  }
  if (!initCheck.llmConfig) {
    return 2
  }
  return 0
})

const initCheckPass = computed(() => {
  return initCheck.envLib && initCheck.serverConfig && initCheck.llmConfig
})

function startTheExperience() {
  config.setInit(true)
  router.push({ path: '/task' })
}

onUnmounted(() => {
  // 取消监听后台执行bat命令事件
  EventsOff('ExecRunBat', null)
})

function loadConfig() {
  const filePath = appDataPath.value + "\\config\\config.toml"
  files.readTomlNode(filePath, "server").then((node) => {
    console.log("config/config.toml: ", node)
    if (utils.isBlank(node)) {
      readConfigSuccess.value = false
      initCheck.serverConfig = false
      utils.pop(t('readTomlFailed'))
      return
    }
    utils.copyProps(node, serverConfig)
    utils.copyProps(node, serverConfigUpd)
    initCheck.serverConfig = true
  })

  files.readTomlNode(filePath, "llm").then((node) => {
    console.log("config/config.toml: ", node)
    if (utils.isBlank(node)) {
      readConfigSuccess.value = false
      initCheck.llmConfig = false
      utils.pop(t('readTomlFailed'))
      return
    }
    utils.copyProps(node, llmConfig)
    utils.copyProps(node, llmConfigUpd)
    initCheck.llmConfig = true
  })
}

function saveServerConfig() {
  const filePath = appDataPath.value + "\\config\\config.toml"
  files.readAll(filePath)
  files.saveTomlNode(filePath, "server", serverConfigUpd).then((resp) => {
    console.log("config/config.toml: ", resp)
    loadConfig()
    toShow('server')
  })
}

function saveLlmConfig() {
  const filePath = appDataPath.value + "\\config\\config.toml"
  files.readAll(filePath)
  files.saveTomlNode(filePath, "llm", llmConfigUpd).then((resp) => {
    console.log("config/config.toml: ", resp)
    loadConfig()
    toShow('llm')
  })
}

const ruleFormRef = ref()

const rules = reactive({
  host: [{ validator: verify.validator('notBlank'), trigger: 'blur' }],
  port: [{ validator: verify.validator('notBlank'), trigger: 'blur' }],

  model: [{ validator: verify.validator('notBlank'), trigger: 'blur' }],
  base_url: [{ validator: verify.validator('notBlank'), trigger: 'blur' }],
  api_key: [{ validator: verify.validator('notBlank'), trigger: 'blur' }],
  max_tokens: [{ validator: verify.validator('notBlank'), trigger: 'blur' }],
  temperature: [{ validator: verify.validator('notBlank'), trigger: 'blur' }],
})

const submitServerConfig = async () => {
  try {
    await ruleFormRef.value.validate();
    if (!utils.hasDfProps(serverConfig, serverConfigUpd)) {
      ElMessage.success('未发生更改!');
      toShow('server')
      return
    }
    ElMessage.success('验证通过，提交表单');
    saveServerConfig()
  } catch (error) {
    console.log('error: ', error);
    ElMessage.error('参数验证失败');
  }
}

const submitLlmConfig = async () => {
  try {
    await ruleFormRef.value.validate();
    if (!utils.hasDfProps(llmConfig, llmConfigUpd)) {
      ElMessage.success('未发生更改!');
      toShow('llm')
      return
    }
    ElMessage.success('验证通过，提交表单');
    saveLlmConfig()
    toShow('llm')
  } catch (error) {
    ElMessage.error('参数验证失败');
  }
}

</script>

<style scoped>
.download-progress-tips {
  max-width: 100%;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
