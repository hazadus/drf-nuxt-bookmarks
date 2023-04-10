<script setup lang="ts">
import { useAuthStore } from './stores/AuthStore';

const authStore = useAuthStore();

onBeforeMount(() => {
  authStore.initializeStore();
});
</script>

<template>
  <TheNavbar />
  <section class="section p-5 page-content-section">
    <div class="container is-widescreen">
      <NuxtPage />
    </div>
  </section>
  <TheFooter />
</template>

<style>
@import 'bulma/css/bulma.css';

.page-content-section {
  min-height: calc(100vh - 52px - 168px);
}
</style> 