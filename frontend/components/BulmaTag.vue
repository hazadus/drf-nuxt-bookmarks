<script setup lang="ts">
// https://bulma.io/documentation/elements/tag/

import type { Tag } from '@/types';

// https://vuejs.org/guide/typescript/composition-api.html#typing-component-props
const props = defineProps<{
  tag: Tag,
  hasDeleteButton: Boolean,
}>();

const emit = defineEmits<{
  (e: "delete", tag: Tag): void;
}>();

function onClickDelete() {
  emit("delete", props.tag);
}
</script>

<template>
  <div class="control">
    <div class="tags has-addons">
      <a class="tag is-info is-light">{{ tag.title }}</a>
      <a class="tag is-delete" v-if="props.hasDeleteButton" @click="onClickDelete"></a>
      <a class="tag" v-else>{{ tag.bookmarks_qty }}</a>
    </div>
  </div>
</template>