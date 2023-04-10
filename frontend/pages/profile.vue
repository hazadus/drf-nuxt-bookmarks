<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';

// "auth" middleware redirects user to login page if not authenticated:
definePageMeta({
  middleware: "auth",
});

const authStore = useAuthStore();
const config = useRuntimeConfig();
</script>

<template>
  <Title>{{ authStore.user?.username }}'s profile | Bookmarks</Title>

  <h2 class="title is-size-2">Your profile</h2>

  <div class="columns">
    <div class="column is-9">
      <div class="table">
        <tr>
          <td>Username:</td>
          <td>{{ authStore.user?.username }}</td>
        </tr>
        <tr>
          <td>First name:</td>
          <td>{{ authStore.user?.first_name }}</td>
        </tr>
        <tr>
          <td>Last name:</td>
          <td>{{ authStore.user?.last_name }}</td>
        </tr>
        <tr>
          <td>E-mail:</td>
          <td>{{ authStore.user?.email }}</td>
        </tr>
        <tr>
          <td>Telegram ID:</td>
          <td>{{ authStore.user?.telegram_id }}</td>
        </tr>
        <tr>
          <td>Joined on:</td>
          <td>{{ authStore.user?.date_joined }}</td>
        </tr>
        <tr>
          <td>Last login:</td>
          <td>{{ authStore.user?.last_login }}</td>
        </tr>

      </div>
    </div>
    <div class="column is-3">
      <figure class="image is-128x128">
        <img class="is-rounded" v-if="!authStore.user?.profile_image" src="/images/default_profile_pic.png">
        <img class="is-rounded" v-else :src="config.apiBase + authStore.user?.profile_image">
      </figure>
    </div>
  </div>
</template>