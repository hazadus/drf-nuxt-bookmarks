<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';

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
    errors.value.push("The username is missing.");
  }

  if (password.value.trim() === "") {
    errors.value.push("The password is too short.");
  } else {
    if (password.value !== password2.value) {
      errors.value.push("Passwords must match.");
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

<template>
  <Title>Create new user account | Bookmarks</Title>

  <div class="columns">
    <div class="column is-4 is-offset-4">
      <div class="box">
        <h1 class="title is-size-2">Sign up</h1>
        <h2 class="subtitle">Create new user account</h2>
        <form @submit.prevent="submitForm">
          <div class="field">
            <label>Username:</label>
            <div class="control">
              <input v-model="username" type="text" class="input" />
            </div>
          </div>

          <div class="field">
            <label>Password:</label>
            <div class="control">
              <input v-model="password" type="password" class="input" />
            </div>
          </div>

          <div class="field">
            <label>Repeat password:</label>
            <div class="control">
              <input v-model="password2" type="password" class="input" />
            </div>
          </div>

          <BulmaNotification v-if="errors.length" type="danger">
            <p v-for="error in errors" :key="error">{{ error }}</p>
          </BulmaNotification>

          <div class="field">
            <div class="control has-text-right">
              <button class="button is-success">Sign up</button>
            </div>
          </div>

          <hr />

          <p>
            <NuxtLink to="/login/" class="is-link">
              Log In
            </NuxtLink>
            if you already have an account.
          </p>
        </form>
      </div>
    </div>
  </div>
</template>