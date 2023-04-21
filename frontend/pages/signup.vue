<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';

// https://v8.i18n.nuxtjs.org/guide/per-component-translations
const { t } = useI18n({
  useScope: "local"
});

const config = useRuntimeConfig();
const authStore = useAuthStore();
const router = useRouter();

const username: Ref<string> = ref("");
const password: Ref<string> = ref("");
const password2: Ref<string> = ref("");
const errors: Ref<string[]> = ref([]);

async function submitForm() {
  /*
    Check input values. Post input data to API if all is fine.
    Redirect to login page on success. If not, show errors.
  */
  console.log("submit")
  errors.value = [];

  /* Do simple form validation before sending it to backend */
  if (username.value.trim() === "") {
    errors.value.push(t("error_missing_username"));
  }

  if (password.value.trim() === "") {
    errors.value.push(t("error_password_too_short"));
  } else {
    if (password.value !== password2.value) {
      errors.value.push(t("error_passwords_must_match"));
    }
  }

  /* If all is OK, post data to API */
  if (!errors.value.length) {
    const formData = {
      username: username.value,
      password: password.value,
    };

    const { data, error: signupError } = await useFetch(() => `${config.public.apiBase}/api/v1/users/`, {
      method: "POST", body: formData,
    });

    if (signupError.value) {
      errors.value.push("Login error: " + signupError.value?.message);
    } else {
      router.push("/login/");
    }
  }
}

onBeforeMount(() => {
  if (authStore.isAuthenticated) {
    router.push("/profile/");
  }
});
</script>

<i18n lang="yaml">
  en:
    page_title: "Create new user account"
    page_header: "Sign up"
    page_header_subtitle: "Create new user account"
    label_username: "Username"
    label_password: "Password"
    label_repeat_password: "Repeat password"
    button_sign_up: "Sign up"
    link_log_in: "Log In"
    link_log_in_description: "if you already have an account."
    error_missing_username: "The username is missing."
    error_password_too_short: "The password is too short."
    error_passwords_must_match: "Passwords must match."
  ru:
    page_title: "Создание новой учетной записи"
    page_header: "Регистрация"
    page_header_subtitle: "Создайте новую учетную запись"
    label_username: "Имя пользователя"
    label_password: "Пароль"
    label_repeat_password: "Повторите пароль"
    button_sign_up: "Зарегистрироваться"
    link_log_in: "Войдите"
    link_log_in_description: "если у вас уже есть учетная запись."
    error_missing_username: "Не указано имя пользователя."
    error_password_too_short: "Пароль слишком короткий."
    error_passwords_must_match: "Пароли должны совпадать."
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
              <input v-model="username" type="text" class="input" />
            </div>
          </div>

          <div class="field">
            <label>
              {{ t("label_password") }}:
            </label>
            <div class="control">
              <input v-model="password" type="password" class="input" />
            </div>
          </div>

          <div class="field">
            <label>
              {{ t("label_repeat_password") }}:
            </label>
            <div class="control">
              <input v-model="password2" type="password" class="input" />
            </div>
          </div>

          <BulmaNotification v-if="errors.length" type="danger">
            <p v-for="error in errors" :key="error">{{ error }}</p>
          </BulmaNotification>

          <div class="field">
            <div class="control has-text-right">
              <button class="button is-success">
                {{ t("button_sign_up") }}
              </button>
            </div>
          </div>

          <hr />

          <p>
            <NuxtLink to="/login/" class="is-link">
              {{ t("link_log_in") }}
            </NuxtLink>
            {{ t("link_log_in_description") }}
          </p>
        </form>
      </div>
    </div>
  </div>
</template>