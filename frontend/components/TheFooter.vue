<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';

const authStore = useAuthStore();
</script>

<template>
  <footer class="footer">
    <div class="container is-widescreen">
      <div class="columns">
        <div class="column is-6">
          <p>
            &copy; <a href="https://github.com/hazadus/">hazadus</a>, 2023.
          </p>
        </div>

        <div class="column is-2">
          <ul>
            <li class="mb-1">
              <NuxtLink to="/">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="material-symbols:roofing-outline" />
                  </span>
                  <span>Home</span>
                </span>
              </NuxtLink>
            </li>
            <li class="mb-1">
              <NuxtLink to="/add/">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="material-symbols:bookmark-add" />
                  </span>
                  <span>Add Bookmark</span>
                </span>
              </NuxtLink>
            </li>
            <li class="mb-1">
              <NuxtLink to="/bookmarks/">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="material-symbols:bookmarks" />
                  </span>
                  <span>View Bookmarks</span>
                </span>
              </NuxtLink>
            </li>
            <li class="mb-1">
              <NuxtLink to="/folders/">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="material-symbols:folder-managed-rounded" />
                  </span>
                  <span>Manage Folders</span>
                </span>
              </NuxtLink>
            </li>
          </ul>
        </div>

        <div class="column is-2">
          <ul>
            <template v-if="!authStore.isAuthenticated">
              <li class="mb-1">
                <NuxtLink to="/login/">
                  <span class="icon-text">
                    <span class="icon">
                      <Icon name="material-symbols:login" />
                    </span>
                    <span>Log In</span>
                  </span>
                </NuxtLink>
              </li>
              <li class="mb-1">
                <NuxtLink to="/signup/">
                  <span class="icon-text">
                    <span class="icon">
                      <Icon name="mdi:handshake-outline" />
                    </span>
                    <span>
                      Sign Up
                    </span>
                  </span>
                </NuxtLink>
              </li>
            </template>
            <li class="mb-1" v-else>
              <NuxtLink to="/profile/">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="mdi:book-account" />
                  </span>
                  <span>
                    User Profile
                  </span>
                </span>
              </NuxtLink>
            </li>
          </ul>
        </div>

        <div class="column is-2">
          <ul>
            <li class="mb-1">
              <NuxtLink to="/about/">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="game-icons:gears" />
                  </span>
                  <span>
                    About Project
                  </span>
                </span>
              </NuxtLink>
            </li>
            <li class="mb-1">
              <a href="https://github.com/hazadus/drf-nuxt-bookmarks">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="mdi:github" />
                  </span>
                  <span>
                    Source Code
                  </span>
                </span>
              </a>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </footer>
</template>