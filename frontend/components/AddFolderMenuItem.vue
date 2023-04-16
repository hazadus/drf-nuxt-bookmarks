<script setup lang="ts">
const isCreating: Ref<boolean> = ref(false);
const newFolderTitle: Ref<string> = ref("");

function onClickAdd() {
  alert(newFolderTitle.value);
}

function onClickCancel() {
  newFolderTitle.value = "";
  isCreating.value = false;
}
</script>

<template>
  <template v-if="!isCreating">
    <a class="has-text-grey-light" @click="isCreating = true">
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
    <div class="field has-addons">
      <p class="control">
        <input class="input is-small" type="text" placeholder="New folder title" maxlength="16" v-model="newFolderTitle"
          @keyup.enter="onClickAdd">
      </p>

      <p class="control">
      <div class="field has-addons">
        <p class="control">
          <button class="button is-small is-success" @click="onClickAdd">
            <span class="icon is-small">
              <Icon name="mdi:plus" />
            </span>
          </button>
        </p>

        <p class="control">
          <button class="button is-small is-warning" @click="onClickCancel">
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