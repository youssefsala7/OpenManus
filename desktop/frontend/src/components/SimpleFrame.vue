<template>
  <main>
    <div class="container">
      <!-- 路由展示区 -->
      <RouterView />
    </div>
  </main>

</template>

<script setup>
import { RouterView } from 'vue-router'

</script>

<style scoped>
main {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: safe center;
  align-items: safe center;
}
</style>
