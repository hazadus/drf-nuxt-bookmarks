<script setup lang="ts">
import { useAuthStore } from './stores/AuthStore';

const authStore = useAuthStore();
authStore.initializeStore();
</script>

<template>
  <TheNavbar />
  <NuxtPage />
  <TheFooter />
</template>

<style>
@import 'bulma/css/bulma.css';
</style> 