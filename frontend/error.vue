<script setup lang="ts">
import { useAuthStore } from "./stores/AuthStore";

// https://v8.i18n.nuxtjs.org/guide/per-component-translations
const { t } = useI18n({
  useScope: "local"
});

const props = defineProps({
  // Reference: https://nuxt.com/docs/getting-started/error-handling#rendering-an-error-page 
  error: Error,
});

const authStore = useAuthStore();

onBeforeMount(() => {
  authStore.initializeStore();
});

function onClearError() {
  clearError({ redirect: "/" });
}
</script>

<i18n lang="yaml">
  en:
    hero_subtitle_1: "We are sorry, an error has occured."
    button_back_to_home: "Back to home page"
  ru:
    hero_subtitle_1: "Извините, произошла ошибка."
    button_back_to_home: "Вернуться на главную"
</i18n>

<template>
  <TheNavbar />
  <section class="section p-5 page-content-section">
    <div class="container is-widescreen">
      <section class="hero is-small is-warning">
        <div class="hero-body">

          <div class="columns is-vcentered">
            <div class="column is-8">
              <p class="title">
                {{ props.error }}
              </p>
              <p class="subtitle">
                {{ t("hero_subtitle_1") }}
              </p>
              <button class="button is-primary" @click="onClearError">
                {{ t("button_back_to_home") }}
              </button>
            </div>

            <div class="column is-4">
              <figure class="image">
                <img src="/images/error.png">
              </figure>
            </div>
          </div>

        </div>
      </section>

    </div>
  </section>
  <TheFooter />
</template>

<style>
@import 'bulma/css/bulma.css';

.page-content-section {
  min-height: calc(100vh - 52px - 228px);
}
</style>