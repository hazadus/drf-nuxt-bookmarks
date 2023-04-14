<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { Bookmark } from '@/types';

// "auth" middleware redirects user to login page if not authenticated:
definePageMeta({
  middleware: "auth",
});

const config = useRuntimeConfig();

const url: Ref<string> = ref("");
const errors: Ref<string[]> = ref([]);
const addedBookmarks: Ref<Bookmark[]> = ref([]);

function submitForm() {
  console.log("Add URL: ", url.value);
}
</script>

<template>
  <h2 class="title is-size-2">Add bookmark</h2>
  <BulmaNotification type="secondary">
    <div class="icon-text">
      <span class="icon has-text-info is-hidden-mobile">
        <Icon name="mdi:information-variant-circle" />
      </span>
      <span>
        Enter an URL below and press "Add" or hit Enter key to create a new bookmark.
      </span>
    </div>
  </BulmaNotification>

  <form @submit.prevent="submitForm">
    <div class="field">
      <label class="label">Create bookmark for URL:</label>
      <div class="control">
        <input class="input mr-3" type="url" placeholder="e.g.: https://bookmarks.hazadus.ru" v-model="url"
          style="width: calc(100% - 70px - 12px);">
        <button class="button is-success">Add</button>
      </div>
    </div>
  </form>

  <BulmaNotification v-if="errors.length" type="danger" class="mt-5">
    <div class="icon-text mb-3">
      <span class="icon has-text-warning is-hidden-mobile">
        <Icon name="material-symbols:dangerous-rounded" />
      </span>
      <span>
        <strong>An error has occured while trying to add new bookmark!</strong>
      </span>
    </div>
    <p class="block">
      Error description goes here...
    </p>
  </BulmaNotification>

  <!-- List new bookmarks -->
  <div class="box mt-5" v-for="bookmark in addedBookmarks" :key="`added-bkmrk-${bookmark.id}`">
    <a :href="bookmark.url" target="_blank">
      {{ bookmark.title }}
    </a>
  </div>
</template>