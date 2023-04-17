<script setup lang="ts">
import type { Folder } from '@/types';
import { is } from '@babel/types';

const props = defineProps({
  folder: {
    type: Object as PropType<Folder>,
    required: true,
  },
});

const isLoading: Ref<boolean> = ref(false);
const isEditing: Ref<boolean> = ref(false);
const changedFolderTitle: Ref<string> = ref(props.folder.title);

function onClickDelete() { }

function onClickEdit() {
  isEditing.value = true;
}

function onClickSave() {
  isLoading.value = true;
  //isEditing.value = false;
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
            :disabled="isLoading">
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