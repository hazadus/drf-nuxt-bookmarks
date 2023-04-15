<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { Bookmark } from '@/types';

// "auth" middleware redirects user to login page if not authenticated:
definePageMeta({
  middleware: "auth",
});

const authStore = useAuthStore();
const config = useRuntimeConfig();

const url: Ref<string> = ref("");
const errors: Ref<string[]> = ref([]);
const addedBookmarks: Ref<Bookmark[]> = ref([]);

async function submitForm() {
  errors.value = [];

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
    const errorMessage = "Error updating user information " + error.value?.message;
    console.error(errorMessage);
    errors.value.push(errorMessage);
    return;
  }

  const newBookmark = data.value as Bookmark;
  addedBookmarks.value.unshift(newBookmark);
  url.value = "";
}
</script>

<template>
  <Title>Add new bookmark | Bookmarks</Title>

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
    <!-- Error list -->
    <div class="icon-text mb-3">
      <span class="icon has-text-warning is-hidden-mobile">
        <Icon name="material-symbols:dangerous-rounded" />
      </span>
      <span>
        <strong>An error has occured while trying to add new bookmark!</strong>
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