<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();
const config = useRuntimeConfig();

const showMobileMenu: Ref<boolean> = ref(false);

async function onClickLogOut() {
  /*
    Delete auth data from local storage.
    Forward user to login page if succeeded.
  */
  showMobileMenu.value = false;
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
        <div class="navbar-burger burger" @click="showMobileMenu = !showMobileMenu">
          <span></span>
          <span></span>
          <span></span>
        </div>
      </div>

      <div class="navbar-menu" :class="showMobileMenu ? 'is-active' : ''">
        <div class="navbar-start">
          <!-- Menu items -->
          <NuxtLink to="/add/" class="navbar-item" :class="route.path === '/add/' ? 'is-active' : ''"
            @click="showMobileMenu = false">
            Add
          </NuxtLink>
          <NuxtLink to="/bookmarks/" class="navbar-item" :class="route.path === '/bookmarks/' ? 'is-active' : ''"
            @click="showMobileMenu = false">
            Bookmarks
          </NuxtLink>
          <NuxtLink to="/about/" class="navbar-item" :class="route.path === '/about/' ? 'is-active' : ''"
            @click="showMobileMenu = false">
            About
          </NuxtLink>
        </div>

        <div class="navbar-end">
          <!-- Buttons -->
          <div class="navbar-item">
            <div class="buttons" v-if="!authStore.isAuthenticated">
              <NuxtLink to="/signup/" class="button is-primary" @click="showMobileMenu = false">
                <strong>Sign up</strong>
              </NuxtLink>
              <NuxtLink to="/login/" class="button is-light" @click="showMobileMenu = false">
                Log in
              </NuxtLink>
            </div>
          </div>

          <!-- Profile drop-down -->
          <div class="navbar-item has-dropdown is-hoverable" v-if="authStore.isAuthenticated">
            <div class="navbar-link">
              <figure class="image mr-2 is-hidden-mobile is-hidden-tablet-only">
                <img class="is-rounded"
                  style="width: 32px !important; height: 32px !important; max-height: 32px !important;"
                  v-if="!authStore.user?.profile_image" src="/images/default_profile_pic.png">
                <img v-else class="is-rounded is-32x32 "
                  style="width: 32px !important; height: 32px !important; max-height: 32px !important;"
                  :src="config.apiBase + authStore.user.profile_image">
              </figure>
              {{ authStore.user?.username }}
            </div>
            <!-- NB: `key` added to re-render menu (thus, hide dropdown) on each route change. -->
            <div class="navbar-dropdown is-right" :key="route.path">
              <NuxtLink to="/profile/" class="navbar-item" @click="showMobileMenu = false">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="mdi:book-account" />
                  </span>
                  <span>
                    Profile
                  </span>
                </span>
              </NuxtLink>
              <a class="navbar-item" @click="onClickLogOut()">
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