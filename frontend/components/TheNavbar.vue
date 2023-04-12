<script setup>
import { useAuthStore } from '@/stores/AuthStore';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const config = useRuntimeConfig();

async function logOut() {
  /*
    Delete auth data from local storage.
    Forward user to login page if succeeded.
  */
  authStore.logOut();
  router.push("/login/");
}
</script>

<template>
  <nav class="navbar has-shadow is-link">
    <div class="container is-widescreen">

      <!-- Site title -->
      <div class="navbar-brand">
        <NuxtLink to="/" class="navbar-item">
          <Icon name="mdi:bookmark-multiple" class="has-text-primary" />
          &nbsp;<h2 class="title is-size-3 has-text-light">Bookmarks</h2>
        </NuxtLink>
        <div class="navbar-burger burger">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <!-- Menu items -->
          <a class="navbar-item" href="#">
            Add
          </a>
          <NuxtLink to="/bookmarks/" class="navbar-item" :class="route.path === '/bookmarks/' ? 'is-active' : ''">
            Bookmarks
          </NuxtLink>
          <NuxtLink to="/about/" class="navbar-item" :class="route.path === '/about/' ? 'is-active' : ''">
            About
          </NuxtLink>
        </div>

        <div class="navbar-end">
          <!-- Buttons -->
          <div class="navbar-item">
            <div class="buttons" v-if="!authStore.isAuthenticated">
              <NuxtLink to="/signup/" class="button is-primary">
                <strong>Sign up</strong>
              </NuxtLink>
              <NuxtLink to="/login/" class="button is-light">
                Log in
              </NuxtLink>
            </div>
          </div>

          <!-- Profile drop-down -->
          <div class="navbar-item has-dropdown is-hoverable" v-if="authStore.isAuthenticated">
            <div class="navbar-link">
              <figure class="image mr-2">
                <img class="is-rounded"
                  style="width: 32px !important; height: 32px !important; max-height: 32px !important;"
                  v-if="!authStore.user.profile_image" src="/images/default_profile_pic.png">
                <img class="is-rounded is-32x32 " v-else :src="config.apiBase + authStore.user.profile_image">
              </figure>
              {{ authStore.user.username }}
            </div>
            <!-- NB: `key` added to re-render menu (thus, hide dropdown) on each route change. -->
            <div class="navbar-dropdown is-right" :key="route.path">
              <NuxtLink to="/profile/" class="navbar-item">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="mdi:book-account" />
                  </span>
                  <span>
                    Profile
                  </span>
                </span>
              </NuxtLink>
              <a class="navbar-item" @click="logOut()">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="mdi:logout" />
                  </span>
                  <span>
                    Sign Out
                  </span>
                </span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>