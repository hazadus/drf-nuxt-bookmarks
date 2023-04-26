<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { User } from "@/types";

// https://v8.i18n.nuxtjs.org/guide/per-component-translations
const { t } = useI18n({
  useScope: "local"
});

const config = useRuntimeConfig();
const authStore = useAuthStore();
const router = useRouter();

const username: Ref<string> = ref("");
const password: Ref<string> = ref("");
const error: Ref<string | undefined> = ref("");

interface AuthToken {
  auth_token: string;
}

async function submitForm() {
  // Clear errors from previous attempt:
  error.value = "";

  const formData = {
    username: username.value,
    password: password.value,
  };

  const { data: authData, error: loginError } = await useFetch(() => `${config.public.apiBase}/api/v1/token/login/`, {
    method: "POST", body: formData,
  });

  if (loginError.value) {
    error.value = t("error_logging_in") + loginError.value?.message;
    return;
  }

  const token = authData.value as AuthToken;

  // Fetch user info
  const { data: userData, error: userDataError } = await useFetch(() => `${config.public.apiBase}/api/v1/user/details/`, {
    headers: [
      ["Authorization", "Token " + token.auth_token,],
    ]
  });

  if (userDataError.value) {
    error.value = t("error_fetching_user_info") + userDataError.value?.message;
    return;
  }

  const user = userData.value as User;

  // Save token and user info in store:
  authStore.logIn(token.auth_token, user);

  // Forward user to the bookmark list
  router.push("/bookmarks/");
}

onBeforeMount(() => {
  if (authStore.isAuthenticated) {
    router.push("/profile/");
  }
});
</script>

<i18n lang="yaml">
  en:
    page_title: "Log in"
    page_header: "Log in"
    page_header_subtitle: "Log into the site with your account."
    label_username: "Username"
    label_password: "Password"
    button_log_in: "Log In"
    link_sign_up: "Sign up"
    link_sign_up_description: "if you don't have an account yet."
    error_logging_in: "Login error: "
    error_fetching_user_info: "Error fetching user information: "
  ru:
    page_title: "Войти"
    page_header: "Войти"
    page_header_subtitle: "Зайдите на сайт с вашей учетной записью"
    label_username: "Имя пользователя"
    label_password: "Пароль"
    button_log_in: "Войти"
    link_sign_up: "Зарегистрируйтесь"
    link_sign_up_description: "если у вас ещё нет учетной записи."
    error_logging_in: "Ошибка входа: "
    error_fetching_user_info: "Error fetching user information: "
</i18n>

<template>
  <Title>
    {{ t("page_title") }} | Bookmarks
  </Title>

  <div class="columns">
    <div class="column is-4 is-offset-4">
      <div class="box">
        <h1 class="title is-size-2">
          {{ t("page_header") }}
        </h1>
        <h2 class="subtitle">
          {{ t("page_header_subtitle") }}
        </h2>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label>
              {{ t("label_username") }}:
            </label>
            <div class="control">
              <input v-model="username" type="text" class="input" id="username" />
            </div>
          </div>

          <div class="field">
            <label>
              {{ t("label_password") }}:
            </label>
            <div class="control">
              <input v-model="password" type="password" class="input" id="password" />
            </div>
          </div>

          <BulmaNotification v-if="error?.length" type="danger">
            <p>{{ error }}</p>
          </BulmaNotification>

          <div class="field">
            <div class="control has-text-right">
              <button class="button is-success">
                {{ t("button_log_in") }}
              </button>
            </div>
          </div>

          <hr />

          <p>
            <NuxtLink to="/signup/" class="is-link">
              {{ t("link_sign_up") }}
            </NuxtLink>
            {{ t("link_sign_up_description") }}
          </p>
        </form>
      </div>
    </div>
  </div>
</template>