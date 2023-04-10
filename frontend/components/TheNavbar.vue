<script setup>
import { useAuthStore } from '@/stores/AuthStore';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

function logOut() {
  authStore.logOut();
  router.push("/login/");
}
</script>

<template>
  <nav class="navbar has-shadow is-link">
    <div class="container is-widescreen">

      <div class="navbar-brand">
        <a class="navbar-item">
          <img src="/images/logo.jpg">
        </a>
        <div class="navbar-burger burger">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>

      <div class="navbar-menu">
        <div class="navbar-start">
          <!-- Site title -->
          <div class="navbar-item">
            <div>
              <small>Hazadus Bookmarks App</small>
            </div>
          </div>
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
            <div class="buttons">
              <a class="button is-primary" v-if="!authStore.isAuthenticated">
                <strong>Sign up</strong>
              </a>
              <NuxtLink to="/login/" class="button is-light" v-if="!authStore.isAuthenticated">
                Log in
              </NuxtLink>
            </div>
          </div>

          <!-- Profile drop-down -->
          <div class="navbar-item has-dropdown is-hoverable" v-if="authStore.isAuthenticated">
            <div class="navbar-link">
              <figure class="image is-32x32 mr-2">
                <img class="is-rounded" src="/images/logo.jpg">
              </figure>
              hazadus
            </div>
            <div class="navbar-dropdown is-right">
              <a class="navbar-item">
                <div>
                  <span class="icon">
                    <Icon name="mdi:book-account" />
                  </span>
                  Profile
                </div>
              </a>
              <a class="navbar-item" @click="logOut()">
                <div>
                  <span class="icon">
                    <Icon name="mdi:logout" />
                  </span>
                  Sign Out
                </div>
              </a>
            </div>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>