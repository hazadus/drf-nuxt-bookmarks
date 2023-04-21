<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';

// https://v8.i18n.nuxtjs.org/guide/per-component-translations
const { t } = useI18n({
  useScope: "local"
});

const authStore = useAuthStore();
</script>

<i18n lang="yaml">
  en:
    home: "Home"
    add_bookmark: "Add Bookmark"
    view_bookmarks: "View Bookmarks"
    log_in: "Log In"
    sign_up: "Sign Up"
    user_profile: "User Profile"
    manage_folders: "Manage Folders"
    about_project: "About Project"
    source_code: "Source Code"
  ru:
    home: "Главная"
    add_bookmark: "Создать Закладку"
    view_bookmarks: "Все Закладки"
    log_in: "Войти"
    sign_up: "Регистрация"
    user_profile: "Профиль"
    manage_folders: "Ваши Папки"
    about_project: "О проекте"
    source_code: "Исходный код"
</i18n>

<template>
  <footer class="footer">
    <div class="container is-widescreen">
      <div class="columns">
        <div class="column is-6">
          <p>
            &copy; <a href="https://github.com/hazadus/">hazadus</a>, 2023.
          </p>
          <p>
            <LangSwitcher />
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
                  <span>
                    {{ t("home") }}
                  </span>
                </span>
              </NuxtLink>
            </li>
            <li class="mb-1">
              <NuxtLink to="/add/">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="material-symbols:bookmark-add" />
                  </span>
                  <span>
                    {{ t("add_bookmark") }}
                  </span>
                </span>
              </NuxtLink>
            </li>
            <li class="mb-1">
              <NuxtLink to="/bookmarks/">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="material-symbols:bookmarks" />
                  </span>
                  <span>
                    {{ t("view_bookmarks") }}
                  </span>
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
                    <span>
                      {{ t("log_in") }}
                    </span>
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
                      {{ t("sign_up") }}
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
                    {{ t("user_profile") }}
                  </span>
                </span>
              </NuxtLink>
            </li>
            <li class="mb-1">
              <NuxtLink to="/folders/">
                <span class="icon-text">
                  <span class="icon">
                    <Icon name="material-symbols:folder-managed-rounded" />
                  </span>
                  <span>
                    {{ t("manage_folders") }}
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
                    {{ t("about_project") }}
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
                    {{ t("source_code") }}
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