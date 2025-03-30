<template>
  <div class="main-content">
    <el-card>
      <template #header>
        <div class="title fxsb">
          <div>{{ t('envConfig') }}</div>
        </div>
      </template>

      <!-- Show Data -->
      <el-steps direction="vertical" :active="1">
        <el-step title="Step 1">
          <template #description>
            <el-card class="mtb-10">
              <div class="fxsb">
                <div>
                  <el-text class="pr-10">{{ t('envLibDownload') }}:</el-text>
                  <el-text>{{ t('checkedPass') }}</el-text>
                </div>
                <el-button type="primary" class="mlr-10" @click="envLibDownload">{{ t('envLibDownload') }}</el-button>
              </div>
            </el-card>
          </template>
        </el-step>

        <el-step title="Step 2">
          <template #description>
            <el-card class="mtb-10">
              <template #header>
                <div class="fxsb">
                  <div>
                    <el-text class="pr-10">{{ t('serverConfig') }}:</el-text>
                    <el-text>{{ t('checkedPass') }}</el-text>
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

        <el-step title="Step 3">
          <template #description>
            <el-card class="mtb-10">
              <template #header>
                <div class="fxsb">
                  <div>
                    <el-text class="pr-10">{{ t('llmConfig') }}:</el-text>
                    <el-text>{{ t('checkedPass') }}</el-text>
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
  </div>

</template>

<script setup>
import { ref, reactive, inject, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useConfig } from '@/store/config'
import { useI18n } from 'vue-i18n'
import { EventsEmit, EventsOn } from '../../../wailsjs/runtime/runtime'

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

function envLibDownload() {
  const runBatPath = "D:\\GitHubProjects\\OpenManus\\run.bat"

  if (EventsEmit) {
    console.log('EventsEmit: ', EventsEmit)
    EventsEmit('bat', 'Exec bat cmd', runBatPath)
  }

}

onMounted(() => {
  // 读取配置文件config/config.toml
  loadConfig()


  EventsOn('Exec bat cmd', (type, data) => {
    console.log('bat cmd exc: ', type, data)
  })
})

function loadConfig() {
  const filePath = "@/../../config/config.toml"
  files.readTomlNode(filePath, "server").then((node) => {
    console.log("config/config.toml: ", node)
    if (utils.isBlank(node)) {
      readConfigSuccess.value = false
      utils.pop(t('readTomlFailed'))
      return
    }
    utils.copyProps(node, serverConfig)
    utils.copyProps(node, serverConfigUpd)
  })

  files.readTomlNode(filePath, "llm").then((node) => {
    console.log("config/config.toml: ", node)
    if (utils.isBlank(node)) {
      readConfigSuccess.value = false
      utils.pop(t('readTomlFailed'))
      return
    }
    utils.copyProps(node, llmConfig)
    utils.copyProps(node, llmConfigUpd)
  })
}

function saveServerConfig() {
  const filePath = "@/../../config/config.toml"
  files.readAll(filePath)
  files.saveTomlNode(filePath, "server", serverConfigUpd).then((resp) => {
    console.log("config/config.toml: ", resp)
    loadConfig()
    toShow('server')
  })
}

function saveLlmConfig() {
  const filePath = "@/../../config/config.toml"
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

<style scoped></style>
