<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { Folder } from '@/types';

const props = defineProps({
  folder: {
    type: Object as PropType<Folder>,
    required: true,
  },
});

const emit = defineEmits<{
  (e: "updated", isUpdated: boolean): void;
  (e: "deleted", isDeleted: boolean): void;
}>();

const authStore = useAuthStore();
const config = useRuntimeConfig();

const isLoading: Ref<boolean> = ref(false);
const isEditing: Ref<boolean> = ref(false);
const changedFolderTitle: Ref<string> = ref(props.folder.title);
const titleInputElement: Ref<HTMLInputElement | null> = ref(null);

async function onClickDelete() {
  isLoading.value = true;

  const { error: folderDeleteError } = await useFetch(() => `${config.public.apiBase}/api/v1/folders/delete/${props.folder.id}/`, {
    method: "DELETE",
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ],
  });

  if (folderDeleteError.value) {
    console.error("Error deleting the folder: " + folderDeleteError.value?.message);
    alert("Something went wrong. Please try again!");
    return;
  }

  emit("deleted", true);
  isLoading.value = false;
}

function onClickEdit() {
  isEditing.value = true;
  nextTick(() => {
    titleInputElement.value?.focus();
  });
}

async function onClickSave() {
  if (!changedFolderTitle.value.length) {
    return;
  }

  isLoading.value = true;

  const { error: folderUpdateError } = await useFetch(() => `${config.public.apiBase}/api/v1/folders/update/${props.folder.id}/`, {
    method: "PATCH",
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ],
    body: {
      title: changedFolderTitle.value,
    },
  });

  if (folderUpdateError.value) {
    console.error("Error updating the folder: " + folderUpdateError.value?.message);
    alert("Something went wrong. Please try again!");
    isLoading.value = false;
    return;
  }

  emit("updated", true);

  isLoading.value = false;
  isEditing.value = false;
}

function onClickCancelSave() {
  changedFolderTitle.value = props.folder.title;
  isEditing.value = false;
}
</script>

<template>
  <tr>
    <td class="py-1 px-0 is-vcentered folder-title-cell">
      <template v-if="!isEditing">
        <span class="icon-text is-size-5">
          <span class="icon">
            <Icon name="mdi:folder" />
          </span>
          <span class="mr-3">
            {{ folder.title }}
          </span>
          <span class="tag is-light">
            {{ folder.bookmarks_qty }}
          </span>
        </span>
      </template>
      <div class="field" v-else>
        <p class="control has-icons-left has-icons-right mr-1">
          <input class="input" type="text" placeholder="Folder title" maxlength="16" v-model="changedFolderTitle"
            ref="titleInputElement" @keydown.enter="onClickSave" :disabled="isLoading">
          <span class="icon is-left">
            <Icon name="mdi:folder" />
          </span>
        </p>
      </div>
    </td>
    <td class="py-1 px-0">
      <template v-if="!isEditing">
        <button class="button is-danger mr-1" @click="onClickDelete" :disabled="isLoading">
          <Icon name="material-symbols:delete" />
        </button>
        <button class="button is-success" @click="onClickEdit" :disabled="isLoading">
          <Icon name="material-symbols:edit" />
        </button>
      </template>
      <template v-else>
        <button class="button is-success mr-1" @click="onClickSave" :disabled="isLoading"
          :class="isLoading ? 'is-loading' : ''">
          <Icon name="material-symbols:check-circle-outline" />
        </button>
        <button class="button is-warning" @click="onClickCancelSave" :disabled="isLoading">
          <Icon name="material-symbols:cancel" />
        </button>
      </template>
    </td>
  </tr>
</template>

<style scoped>
.folder-title-cell {
  min-width: 310px;
}
</style>