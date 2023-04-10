<script setup lang="ts">
import { useAuthStore } from '~/stores/AuthStore';

const config = useRuntimeConfig();
const authStore = useAuthStore();
const router = useRouter();

const username: Ref<string> = ref("");
const password: Ref<string> = ref("");
const error: Ref<string | undefined> = ref("");

interface AuthToken {
  auth_token: string;
}

interface UserInfo {
  id: number;
  username: string;
  email: string;
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
    error.value = "Login error " + loginError.value?.message;
    return;
  }

  // On success, save token in the store:
  const token = authData.value as AuthToken;
  authStore.logIn(token.auth_token);

  // Fetch user info
  // const { data: userData, error: userDataError } = await useFetch(() => `${config.public.apiBase}/api/v1/users/me/`, {
  //   headers: [
  //     ["Authorization", "Token " + token,],
  //   ]
  // });

  // if (userDataError.value) {
  //   error.value = "Error fetching user information " + userDataError.value?.message;
  //   return;
  // }

  // const userInfo = userData.value as UserInfo;
  // console.log("userInfo: ", userInfo);

  // Forward user to the bookmark list
  router.push("/bookmarks/");
}

</script>

<template>
  <Title>Log in | Bookmarks</Title>

  <section class="section login">
    <div class="container is-widescreen">

      <div class="columns">
        <div class="column is-4 is-offset-4">
          <div class="box">
            <h1 class="title is-size-2">Log in</h1>
            <h2 class="subtitle">Log into the site with your account.</h2>
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

              <BulmaNotification v-if="error?.length" type="danger">
                <p>{{ error }}</p>
              </BulmaNotification>

              <div class="field">
                <div class="control has-text-right">
                  <button class="button is-success">Log in</button>
                </div>
              </div>

              <hr />

              <p>

                Sign up

                if you don't have an account yet.
              </p>
            </form>
          </div>
        </div>
      </div>

    </div>
  </section>
</template>

<style scoped>
.login {
  min-height: calc(100vh - 52px - 168px);
}
</style>