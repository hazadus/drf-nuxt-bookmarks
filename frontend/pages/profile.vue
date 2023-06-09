<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { User } from "@/types";

// https://v8.i18n.nuxtjs.org/guide/per-component-translations
const { t } = useI18n({
  useScope: "local"
});

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
const fileInputElement: Ref<HTMLInputElement | null> = ref(null);
const selectedFileName: Ref<string | undefined> = ref(undefined);

const diskQuotaUsedPercent = computed(() => {
  if (authStore.user) {
    let used = authStore.user?.disk_space_used;
    let quota = authStore.user?.disk_quota;

    return quota ? (used / quota * 100).toFixed(0) : 0;
  } else {
    return 0;
  }
});

function onSelectFile() {
  selectedFileName.value = fileInputElement.value?.files?.item(0)?.name;
}

function onClickCancel() {
  newFirstName.value = authStore.user?.first_name;
  newLastName.value = authStore.user?.last_name;
  newTelegramID.value = authStore.user?.telegram_id;

  isEditing.value = false;
}

async function submitForm() {
  if (
    (authStore.user?.first_name === newFirstName.value)
    && (authStore.user?.last_name === newLastName.value)
    && (authStore.user?.telegram_id === newTelegramID.value)
    && (!fileInputElement.value?.files?.length)
  ) {
    // If nothing changed, don't bother the API:
    isEditing.value = false;
    return;
  }

  let formData = new FormData;

  formData.append("first_name", newFirstName.value ? newFirstName.value : "");
  formData.append("last_name", newLastName.value ? newLastName.value : "");
  formData.append("telegram_id", newTelegramID.value ? newTelegramID.value : "");

  if (fileInputElement.value?.files?.length) {
    const image = fileInputElement.value.files.item(0) as File;
    formData.append("profile_image", image);
  }

  const { data: userData, error: userUpdateError } = await useFetch(() => `${config.public.apiBase}/api/v1/user/${authStore.user?.id}/`, {
    method: "PATCH",
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ],
    body: formData,
  });

  if (userUpdateError.value) {
    console.error("Error updating user information: " + userUpdateError.value?.message);
    alert("Something went wrong. Please try again!");
    return;
  }

  const user = userData.value as User;
  authStore.setUser(user);

  isEditing.value = false;
}

function useFormatDateTime(dateObj: Date | undefined) {
  if (dateObj) {
    let date = new Date(dateObj);
    return date.toLocaleDateString("ru-RU") + " " + date.toLocaleTimeString("ru-RU", {
      hour: "2-digit",
      minute: "2-digit"
    });
  }
}
</script>

<i18n lang="yaml">
  en:
    page_header: "Your profile"
    page_subheader_edit_profile: "Edit profile info"
    label_first_name: "First name"
    label_last_name: "Last name"
    label_disk_quota: "Disk quota"
    label_disk_space_used: "Disk space used"
    label_megabytes: "Mb"
    info_header: "Information"
    info_line_1: "Telegram ID is needed to add bookmarks to your account via our"
    info_link_title: "Telegram bot"
    info_line_2: "Send any message to the bot, and it will answer with your ID in the reply."
    label_set_profile_picture: "Set profile picture"
    label_choose_a_file: "Choose a file..."
    button_cancel: "Cancel"
    button_save: "Save"
    label_username: "Username"
    label_joined_on: "Joined on"
    label_last_login: "Last login"
    button_edit_profile: "Edit profile"
  ru:
    page_header: "Ваш профиль"
    page_subheader_edit_profile: "Изменить данные пользователя"
    label_first_name: "Имя"
    label_last_name: "Фамилия"
    label_disk_quota: "Доступно на диске"
    label_disk_space_used: "Занято места на диске"
    label_megabytes: "Мб"
    info_header: "Информация"
    info_line_1: "Телеграм ID нужен, чтобы добавлять закладки в вашу учетную запись через нашего"
    info_link_title: "Телеграм бота"
    info_line_2: "Отправьте любое сообщение боту, и в ответ вы получите ваш Телеграм ID."
    label_set_profile_picture: "Установить изображение профиля"
    label_choose_a_file: "Выберите файл..."
    button_cancel: "Отмена"
    button_save: "Сохранить"
    label_username: "Имя пользователя"
    label_joined_on: "Зарегистрирован"
    label_last_login: "Последний вход"
    button_edit_profile: "Редактировать профиль"
</i18n>

<template>
  <Title>
    {{ authStore.user?.username }} | Bookmarks
  </Title>

  <h2 class="title is-size-2">
    {{ t("page_header") }}
  </h2>

  <div class="columns">
    <div class="column is-6" :key="authStore.user?.id">

      <template v-if="isEditing">
        <h4 class="title is-size-4">
          {{ t("page_subheader_edit_profile") }}
        </h4>

        <form @submit.prevent="submitForm" enctype="multipart/form-data">
          <div class="field">
            <label class="label">
              {{ t("label_first_name") }}
            </label>
            <div class="control">
              <input class="input" type="text" placeholder="e.g Alex Smith" v-model="newFirstName" maxlength="16"
                id="input-first-name">
            </div>
          </div>

          <div class="field">
            <label class="label">
              {{ t("label_last_name") }}
            </label>
            <div class="control">
              <input class="input" type="text" placeholder="e.g Alex Smith" v-model="newLastName" maxlength="16"
                id="input-last-name">
            </div>
          </div>

          <div class="field">
            <label class="label">
              Telegram ID
            </label>
            <div class="control">
              <input class="input" type="string" placeholder="e.g. 123456789" v-model="newTelegramID" maxlength="12"
                id="input-telegram-id">
            </div>
          </div>

          <BulmaNotification type="light">
            <div class="icon-text mb-3">
              <span class="icon has-text-info">
                <Icon name="mdi:information-variant-circle" />
              </span>
              <span>
                <b>
                  {{ t("info_header") }}
                </b>
              </span>
            </div>
            <p class="block">
              {{ t("info_line_1") }}
              <a href="https://t.me/HazadusBookmarksBot"> {{ t("info_link_title") }} </a>.
              {{ t("info_line_2") }}
            </p>
          </BulmaNotification>

          <div class="field">
            <label class="label">
              {{ t("label_set_profile_picture") }}
            </label>
            <div class="control">
              <div class="file has-name">
                <label class="file-label">
                  <input class="file-input" ref="fileInputElement" type="file" name="profile-pic" accept="image/*"
                    @change="onSelectFile">
                  <span class="file-cta">
                    <span class="file-icon">
                      <Icon name="mdi:file-upload-outline" />
                    </span>
                    <span class="file-label">
                      {{ t("label_choose_a_file") }}
                    </span>
                  </span>
                  <span class="file-name">
                    {{ selectedFileName }}
                  </span>
                </label>
              </div>
            </div>
          </div>

          <div class="field">
            <div class="control has-text-right">
              <button class="button is-warning mr-2" @click="onClickCancel">
                {{ t("button_cancel") }}
              </button>
              <button class="button is-success" id="button-save-profile">
                {{ t("button_save") }}
              </button>
            </div>
          </div>
        </form>
      </template>

      <template v-else>
        <table class="table">
          <tbody>
            <tr>
              <td>
                {{ t("label_username") }}:
              </td>
              <td>{{ authStore.user?.username }}</td>
            </tr>
            <tr>
              <td>
                {{ t("label_first_name") }}:
              </td>
              <td>{{ authStore.user?.first_name }}</td>
            </tr>
            <tr>
              <td>
                {{ t("label_last_name") }}:
              </td>
              <td>{{ authStore.user?.last_name }}</td>
            </tr>
            <tr>
              <td>
                E-mail:
              </td>
              <td>{{ authStore.user?.email }}</td>
            </tr>
            <tr>
              <td>
                Telegram ID:
              </td>
              <td>{{ authStore.user?.telegram_id }}</td>
            </tr>
            <tr>
              <td>
                {{ t("label_disk_quota") }}:
              </td>
              <td>
                {{ authStore.user?.disk_quota }} {{ t("label_megabytes") }}
              </td>
            </tr>
            <tr>
              <td>
                {{ t("label_disk_space_used") }}:
              </td>
              <td>
                {{ authStore.user?.disk_space_used }} {{ t("label_megabytes") }} / {{ diskQuotaUsedPercent }}%
                <progress class="progress is-primary" :value="diskQuotaUsedPercent" max="100"></progress>
              </td>
            </tr>
            <tr>
              <td>
                {{ t("label_joined_on") }}:
              </td>
              <td>{{ useFormatDateTime(authStore.user?.date_joined) }}</td>
            </tr>
            <tr>
              <td>
                {{ t("label_last_login") }}:
              </td>
              <td>{{ useFormatDateTime(authStore.user?.last_login) }}</td>
            </tr>
          </tbody>
        </table>

        <div class="field">
          <div class="control">
            <button class="button is-success" @click="isEditing = true" id="button-edit-profile">
              {{ t("button_edit_profile") }}
            </button>
          </div>
        </div>
      </template>
    </div>

    <div class="column is-6">
      <figure class="image is-1by1">
        <img class="is-rounded" v-if="!authStore.user?.profile_image" src="/images/default_profile_pic.png">
        <img class="is-rounded" v-else :src="config.apiBase + authStore.user?.profile_image">
      </figure>
    </div>
  </div>
</template>