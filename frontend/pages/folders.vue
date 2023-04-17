<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { Folder } from '@/types';

// "auth" middleware redirects user to login page if not authenticated:
definePageMeta({
  middleware: "auth",
});

const authStore = useAuthStore();
const config = useRuntimeConfig();

const errors: Ref<string[]> = ref([]);
const allUserFolders: Ref<Folder[] | null> = ref(null);

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


function submitCreateFolderForm() { }

fetchFolderData();
</script>

<template>
  <Title>Manage folders | Bookmarks</Title>

  <h2 class="title is-size-2">Manage folders</h2>

  <div class="columns">
    <div class="column is-narrow">
      <BulmaNotification v-if="errors.length" type="danger" class="mt-5">
        <!-- Error list -->
        <div class="icon-text mb-3">
          <span class="icon has-text-warning is-hidden-mobile">
            <Icon name="material-symbols:dangerous-rounded" />
          </span>
          <span>
            <strong>An error has occured while fetching folder data!</strong>
          </span>
        </div>
        <p class="block" v-for="error in errors" :key="error">
          {{ error }}.
        </p>
      </BulmaNotification>

      <table class="table" v-if="allUserFolders">
        <EditFoldersTableRow v-for="folder in allUserFolders" :key="`folder-id-${folder.id}`" :folder="folder" />
      </table>

      <form @submit.prevent="submitCreateFolderForm">
        <div class="field">
          <label class="label">Create new folder:</label>
          <div class="control">
            <input class="input mr-1 new-folder-input" type="text" placeholder="New folder title" maxlength="16">
            <button class="button is-success">
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
          <span>Information</span>
        </div>
        <p class="block">
          If you delete a folder with bookmarks within, these bookmarks will be moved into &laquo;Inbox&raquo; folder.
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