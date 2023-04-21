<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { Folder } from '@/types';

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

const errors: Ref<string[]> = ref([]);
const allUserFolders: Ref<Folder[] | null> = ref(null);
const newFolderTitle: Ref<string> = ref("");
const isLoading: Ref<boolean> = ref(false);

async function fetchFolderData() {
  errors.value = [];

  const { data: folders, error: foldersError } = await useFetch<Folder[]>(() => `${config.public.apiBase}/api/v1/folders/`, {
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ]
  });

  if (foldersError.value) {
    errors.value.push(foldersError.value.message);
    return;
  }

  allUserFolders.value = folders.value;
}


async function submitCreateFolderForm() {
  if (!newFolderTitle.value.length) {
    return;
  }

  isLoading.value = true;

  const formData = {
    user_id: authStore.user?.id,
    title: newFolderTitle.value,
  };

  const { data: folderData, error: folderCreateError } = await useFetch(() => `${config.public.apiBase}/api/v1/folders/create/`, {
    method: "POST",
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ],
    body: formData,
  });

  if (folderCreateError.value) {
    console.error("Error creating new folder: " + folderCreateError.value?.message);
    alert(t("error_something_went_wrong"));
    isLoading.value = false;
    return;
  }

  newFolderTitle.value = "";
  isLoading.value = false;

  fetchFolderData();
}

fetchFolderData();
</script>

<i18n lang="yaml">
  en:
    page_title: "Manage folders"
    page_header: "Manage folders"
    error_header: "An error has occured while fetching folder data!"
    error_something_went_wrong: "Something went wrong. Please try again!"
    label_create_folder: "Create new folder"
    input_placeholder: "New folder title"
    info_header: "Information"
    info_text: "If you delete a folder with bookmarks within, these bookmarks will be moved into Inbox folder."
  ru:
    page_title: "Управлять папками"
    page_header: "Управлять папками"
    error_header: "При получении данных о папках возникла ошибка!"
    error_something_went_wrong: "Что-то пошло не так. Попробуйте ещё раз!"
    label_create_folder: "Создать новую папку"
    input_placeholder: "Название новой папки"
    info_header: "Информация"
    info_text: "Если вы удалите папку с закладками внутри, эти закладки будут перенесены в папку Входящие."
</i18n>

<template>
  <Title>
    {{ t("page_title") }} | Bookmarks
  </Title>

  <h2 class="title is-size-2">
    {{ t("page_header") }}
  </h2>

  <div class="columns">
    <div class="column is-narrow">
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

      <table class="table" v-if="allUserFolders">
        <EditFoldersTableRow v-for="folder in allUserFolders" :key="`folder-id-${folder.id}`" :folder="folder"
          @deleted="fetchFolderData" @updated="fetchFolderData" />
      </table>

      <form @submit.prevent="submitCreateFolderForm">
        <div class="field">
          <label class="label">
            {{ t("label_create_folder") }}:
          </label>
          <div class="control">
            <input class="input mr-1 new-folder-input" v-model="newFolderTitle" type="text"
              :placeholder="t('input_placeholder')" maxlength="16" :disabled="isLoading">
            <button class="button is-success" :disabled="isLoading" :class="isLoading ? 'is-loading' : ''">
              <Icon name="mdi:plus" />
            </button>
          </div>
        </div>
      </form>
    </div>

    <div class="column">
      <BulmaNotification type="light" v-if="allUserFolders?.length">
        <div class="icon-text mb-3">
          <span class="icon has-text-info">
            <Icon name="mdi:information-variant-circle" />
          </span>
          <span>
            <b>
              {{ t("info_header") }}
            </b>
          </span>
        </div>
        <p class="block">
          {{ t("info_text") }}
        </p>
      </BulmaNotification>
    </div>
  </div>
</template>

<style scoped>
.new-folder-input {
  width: 350px;
}
</style>