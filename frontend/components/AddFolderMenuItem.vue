<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';

const emit = defineEmits<{
  (e: "created", isNewFolderCreated: boolean): void;
}>();

const authStore = useAuthStore();
const config = useRuntimeConfig();

const isCreating: Ref<boolean> = ref(false);
const isLoading: Ref<boolean> = ref(false);
const newFolderTitle: Ref<string> = ref("");

function onClickAddFolderMenu() {
  isCreating.value = true;
  // Auto-focus on input element:
  nextTick(() => {
    (document.querySelector(".new-folder-title-input") as HTMLInputElement).focus();
  });
}

async function onClickAddButton() {
  if (!newFolderTitle.value.trim().length) {
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
    alert("Something went wrong. Please try again!");
    isLoading.value = false;
    return;
  }

  emit("created", true);

  newFolderTitle.value = "";
  isCreating.value = false;
  isLoading.value = false;
}

function onClickCancel() {
  newFolderTitle.value = "";
  isCreating.value = false;
}
</script>

<template>
  <template v-if="!isCreating">
    <a class="has-text-grey-light" @click="onClickAddFolderMenu">
      <span class="icon-text">
        <span class="icon">
          <Icon name="mdi:folder-plus" />
        </span>
        <span class="mr-3">
          <em>Add folder...</em>
        </span>
      </span>
    </a>
  </template>

  <template v-else>
    <div class="field has-addons mt-1">
      <p class="control">
        <input class="input is-small new-folder-title-input" type="text" placeholder="New folder title" maxlength="16"
          v-model="newFolderTitle" @keyup.enter="onClickAddButton" :disabled="isLoading">
      </p>

      <p class="control">
      <div class="field has-addons">
        <p class="control">
          <button class="button is-small is-success" @click="onClickAddButton" :disabled="isLoading"
            :class="isLoading ? 'is-loading' : ''">
            <span class="icon is-small">
              <Icon name="mdi:plus" />
            </span>
          </button>
        </p>

        <p class="control">
          <button class="button is-small is-warning" @click="onClickCancel" :disabled="isLoading">
            <span class="icon is-small">
              <Icon name="mdi:close" />
            </span>
          </button>
        </p>
      </div>
      </p>
    </div>
  </template>
</template>