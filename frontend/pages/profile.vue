<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';

// "auth" middleware redirects user to login page if not authenticated:
definePageMeta({
  middleware: "auth",
});

const authStore = useAuthStore();
const config = useRuntimeConfig();

const isEditing: Ref<boolean> = ref(false);
const newFirstName: Ref<string | undefined> = ref(authStore.user?.first_name);
const newLastName: Ref<string | undefined> = ref(authStore.user?.last_name);
const newTelegramID: Ref<string | undefined> = ref(authStore.user?.telegram_id);

function submitForm() { }
</script>

<template>
  <Title>{{ authStore.user?.username }}'s profile | Bookmarks</Title>

  <h2 class="title is-size-2">Your profile</h2>

  <div class="columns">
    <div class="column is-9">

      <template v-if="isEditing">
        <h4 class="title is-size-4">Edit your profile</h4>

        <form @submit.prevent="submitForm">
          <div class="field">
            <label class="label">First name</label>
            <div class="control">
              <input class="input" type="text" placeholder="e.g Alex Smith" v-model="newFirstName" maxlength="16">
            </div>
          </div>

          <div class="field">
            <label class="label">Last name</label>
            <div class="control">
              <input class="input" type="text" placeholder="e.g Alex Smith" v-model="newLastName" maxlength="16">
            </div>
          </div>

          <div class="field">
            <label class="label">Telegram ID</label>
            <div class="control">
              <input class="input" type="string" placeholder="e.g. 123456789" v-model="newTelegramID" maxlength="12">
            </div>
          </div>

          <BulmaNotification type="light">
            <div class="icon-text mb-3">
              <span class="icon has-text-info">
                <Icon name="mdi:information-variant-circle" />
              </span>
              <span>Information</span>
            </div>
            <p class="block">
              Telegram ID is needed to add bookmarks to your account via our
              <a href="https://t.me/HazadusBookmarksBot">Telegram bot</a>.
              Send any message to <a href="https://t.me/HazadusBookmarksBot">the bot</a>, and it will answer with your ID
              in the reply.
            </p>
          </BulmaNotification>

          <div class="field">
            <div class="control has-text-right">
              <button class="button is-warning mr-2" @click="isEditing = false">Cancel</button>
              <button class="button is-success">Save</button>
            </div>
          </div>
        </form>
      </template>

      <template v-else>
        <table class="table">
          <tbody>
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
          </tbody>
        </table>

        <div class="field">
          <div class="control">
            <button class="button is-success" @click="isEditing = true">Edit profile</button>
          </div>
        </div>
      </template>
    </div>
    <div class="column is-3">
      <figure class="image is-128x128">
        <img class="is-rounded" v-if="!authStore.user?.profile_image" src="/images/default_profile_pic.png">
        <img class="is-rounded" v-else :src="config.apiBase + authStore.user?.profile_image">
      </figure>
    </div>
  </div>
</template>