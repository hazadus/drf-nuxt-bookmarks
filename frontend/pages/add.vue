<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { Bookmark } from '@/types';

// https://v8.i18n.nuxtjs.org/guide/per-component-translations
const { t } = useI18n({
  useScope: "local"
});

// "auth" middleware redirects user to login page if not authenticated:
definePageMeta({
  middleware: "auth",
});

const authStore = useAuthStore();
const config = useRuntimeConfig();

const url: Ref<string> = ref("");
const errors: Ref<string[]> = ref([]);
const isLoading: Ref<boolean> = ref(false);
const addedBookmarks: Ref<Bookmark[]> = ref([]);
const urlInputElement: Ref<HTMLInputElement | null> = ref(null);

async function submitForm() {
  errors.value = [];
  isLoading.value = true;

  const formData = {
    user: authStore.user,
    url: url.value,
  }

  const { data, error } = await useFetch(() => `${config.public.apiBase}/api/v1/bookmarks/create/`, {
    method: "POST",
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ],
    body: formData,
  });

  if (error.value) {
    const errorMessage = t("error_adding_bookmark") + error.value?.message;
    console.error(errorMessage);
    errors.value.push(errorMessage);
    isLoading.value = false;
    return;
  }

  const newBookmark = data.value as Bookmark;
  addedBookmarks.value.unshift(newBookmark);
  url.value = "";
  isLoading.value = false;
  nextTick(() => {
    urlInputElement.value?.focus();
  });
}

onMounted(() => {
  urlInputElement.value?.focus();
});
</script>

<i18n lang="yaml">
  en:
    page_title: "Add new bookmark"
    page_header: "Add bookmark"
    info_text: "Enter an URL below and press \"Add\" or hit Enter key to create a new bookmark."
    label_input_url: "Create bookmark for URL"
    button_add: "Add"
    error_header: "An error has occured while trying to add new bookmark!"
    error_adding_bookmark: "Error creating new bookmark: "
  ru:
    page_title: "Добавить новую закладку"
    page_header: "Добавить закладку"
    info_text: "Введите ссылку в поле снизу и нажмите кнопку \"Добавить\" или клавишу Enter, чтобы создать новую закладку."
    label_input_url: "Создать закладку для URL"
    button_add: "Добавить"
    error_header: "При создании новой закладки произошла ошибка!"
    error_adding_bookmark: "Ошибка при создании закладки: "
</i18n>

<template>
  <Title>
    {{ t("page_title") }} | Bookmarks
  </Title>

  <h2 class="title is-size-2">
    {{ t("page_header") }}
  </h2>

  <BulmaNotification type="secondary">
    <div class="icon-text">
      <span class="icon has-text-info is-hidden-mobile">
        <Icon name="mdi:information-variant-circle" />
      </span>
      <span>
        {{ t("info_text") }}
      </span>
    </div>
  </BulmaNotification>

  <form @submit.prevent="submitForm">
    <div class="field">
      <label class="label">
        {{ t("label_input_url") }}:
      </label>
      <div class="control">
        <input ref="urlInputElement" v-model="url" :disabled="isLoading" class="input mr-3" type="url"
          placeholder="https://bookmarks.hazadus.ru" style="width: calc(100% - 110px - 12px);" id="input-url">
        <button class="button is-success" :class="isLoading ? 'is-loading' : ''">
          {{ t("button_add") }}
        </button>
      </div>
    </div>
  </form>

  <BulmaNotification v-if="errors.length" type="danger" class="mt-5">
    <!-- Error list -->
    <div class="icon-text mb-3">
      <span class="icon has-text-warning is-hidden-mobile">
        <Icon name="material-symbols:dangerous-rounded" />
      </span>
      <span>
        <strong>
          {{ t("error_header") }}
        </strong>
      </span>
    </div>
    <p class="block" v-for="error in errors" :key="error">
      {{ error }}.
    </p>
  </BulmaNotification>

  <!-- List added bookmarks -->
  <div class="box mt-5" v-for="bookmark in addedBookmarks" :key="`added-bkmrk-${bookmark.id}`">
    <div class="columns">
      <div class="column" :class="bookmark.image_url ? 'is-8' : 'is-12'">
        <!-- Link title and description -->
        <a :href="bookmark.url" target="_blank" class="title is-size-5">
          {{ bookmark.title }}
        </a>
        <p v-if="bookmark.description" class="mt-4">
          {{ bookmark.description }}
        </p>
      </div>
      <div class="column is-4" v-if="bookmark.image_url">
        <!-- Cover image -->
        <figure class="image is-16by9">
          <img :src="bookmark.image_url">
        </figure>
      </div>
    </div>
  </div>
</template>