<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';

// https://v8.i18n.nuxtjs.org/guide/per-component-translations
const { t } = useI18n({
  useScope: "local"
});

const authStore = useAuthStore();

if (authStore.isAuthenticated) {
  const router = useRouter();
  router.push("/bookmarks/");
}
</script>

<i18n lang="yaml">
  en:
    hero_title_1: "Keep all your bookmarks in one place"
    hero_subtitle_1: "Create folders, add tags, mark bookmarks as favorite, read or archived - your favorite links are always with you, in any browser and device!"
    hero_title_2: "Easily create bookmarks for any web sites"
    hero_subtitle_2: "Add any link to your bookmarks with just a few clicks via web page or our Telegram bot!"
    hero_title_3: "Edit and categorize your bookmarks"
    hero_subtitle_3: "Save all necessary information to easily find your bookmarks later."
    hero_title_4: "More features to come"
    hero_subtitle_4: "The project is in development right now, so there's a lot of cool features planned for future. Stay tuned!"
  ru:
    hero_title_1: "Храните все свои закладки в одном месте"
    hero_subtitle_1: "Создавайте папки, добавляйте теги, помечайте закладки как избранные, прочитанные или архивные - ваши любимые ссылки всегда с вами, в любом браузере и устройстве!"
    hero_title_2: "С лёгкостью создавайте закладки для любых веб сайтов"
    hero_subtitle_2: "Добавьте любую ссылку в свои закладки всего за пару кликов, через веб сайт или наш Телеграм бот!"
    hero_title_3: "Правьте и разбирайте по категориям ваши закладки"
    hero_subtitle_3: "Сохраните всю необходимую информацию, чтобы позднее с лёгкостью находить нужные закладки."
    hero_title_4: "Больше возможностей в будущем"
    hero_subtitle_4: "Проект прямо сейчас находится в разработке, запланировано много крутых фич для реализации в ближайшем будущем. Оставайтесь с нами!"
</i18n>

<template>
  <section class="hero is-small is-info">
    <div class="hero-body">
      <div class="columns is-vcentered">
        <div class="column is-4">
          <p class="title">
            {{ t("hero_title_1") }}
          </p>
          <p class="subtitle">
            {{ t("hero_subtitle_1") }}
          </p>
        </div>

        <div class="column is-8">
          <figure class="image">
            <img src="/images/screenshot_list.png">
          </figure>
        </div>
      </div>
    </div>
  </section>

  <section class="hero is-small is-primary">
    <div class="hero-body">
      <div class="columns is-vcentered">
        <div class="column is-8">
          <figure class="image">
            <img src="/images/screenshot_add.png">
          </figure>
        </div>

        <div class="column is-4">
          <p class="title">
            {{ t("hero_title_2") }}
          </p>
          <p class="subtitle">
            {{ t("hero_subtitle_2") }}
          </p>
        </div>
      </div>
    </div>
  </section>

  <section class="hero is-small is-success">
    <div class="hero-body">
      <div class="columns is-vcentered">
        <div class="column is-4">
          <p class="title">
            {{ t("hero_title_3") }}
          </p>
          <p class="subtitle">
            {{ t("hero_subtitle_3") }}
          </p>
        </div>

        <div class="column is-8">
          <figure class="image">
            <img src="/images/screenshot_edit.png">
          </figure>
        </div>
      </div>
    </div>
  </section>

  <section class="hero is-medium is-warning">
    <div class="hero-body">
      <p class="title">
        {{ t("hero_title_4") }}
      </p>
      <p class="subtitle">
        {{ t("hero_subtitle_4") }}
      </p>
    </div>
  </section>
</template>