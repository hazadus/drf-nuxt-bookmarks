<script setup lang="ts">
// https://v8.i18n.nuxtjs.org/guide/lang-switcher
import { LocaleObject } from '@nuxtjs/i18n/dist/runtime/composables';

const { locale, locales, setLocale } = useI18n();
const availableLocales = computed(() => {
  // Exclude currently active locale
  return (locales.value as LocaleObject[]).filter((i: LocaleObject) => i.code !== locale.value);
})
</script>

<template>
  <a href="#" v-for="locale in availableLocales" :key="locale.code" @click.prevent.stop="setLocale(locale.code)">
    {{ locale.name }}
  </a>
</template>