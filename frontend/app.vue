<script setup lang="ts">
import type { Bookmark } from './types';

const config = useRuntimeConfig();
const { data } = await useFetch<Bookmark[]>(() => `${config.public.apiBase}/api/v1/bookmarks/`);

console.log("API base is " + config.public.apiBase);

let folder = ref("inbox");
let filter = ref("all");

const inboxBookmarks = computed(() => {
  return data.value?.filter((bookmark) => !bookmark.folder);
});

const favoriteBookmarks = computed(() => {
  return data.value?.filter((bookmark) => bookmark.is_favorite);
});

const archivedBookmarks = computed(() => {
  return data.value?.filter((bookmark) => bookmark.is_archived);
});

const bookmarksInSelectedFolder = computed(() => {
  if (folder.value === "inbox") {
    return inboxBookmarks.value;
  } else if (folder.value === "favorites") {
    return favoriteBookmarks.value;
  } else if (folder.value === "archived") {
    return archivedBookmarks.value;
  }
});

const bookmarks = computed(() => {
  if (filter.value === "all") {
    return bookmarksInSelectedFolder.value;
  } else if (filter.value === "unread") {
    return bookmarksInSelectedFolder.value?.filter((bookmark) => !bookmark.is_read);
  } else if (filter.value === "read") {
    return bookmarksInSelectedFolder.value?.filter((bookmark) => bookmark.is_read);
  }

});

</script>

<template>
  <Title>Bookmarks</Title>

  <nav class="navbar has-shadow">
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
        <div class="navbar-item">
          <div>
            <small>Hazadus Bookmarks App</small>
          </div>
        </div>
      </div>

      <div class="navbar-end">
        <div class="navbar-item has-dropdown is-hoverable">
          <div class="navbar-link">
            Username
          </div>
          <div class="navbar-dropdown is-right">
            <a class="navbar-item">
              <div>
                <span class="icon is-small">
                  <i class="fa fa-user-circle-o"></i>
                </span>
                Profile
              </div>
            </a>
            <a class="navbar-item">
              <div>
                <span class="icon is-small">
                  <i class="fa fa-sign-out"></i>
                </span>
                Sign Out
              </div>
            </a>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <section class="section">
    <div class="columns">
      <div class="column is-4-tablet is-3-desktop is-2-widescreen">
        <nav class="menu">
          <p class="menu-label">
            Folders
          </p>
          <ul class="menu-list">
            <li>
              <a :class="folder === 'inbox' ? 'is-active' : ''" href="#" @click="folder = 'inbox'">
                <span class="icon">
                  <Icon name="mdi:inbox" />
                </span>
                Inbox ({{ inboxBookmarks?.length }})
              </a>
            </li>
            <li>
              <a :class="folder === 'favorites' ? 'is-active' : ''" href="#" @click="folder = 'favorites'">
                <span class="icon">
                  <Icon name="material-symbols:star" />
                </span>
                Favorites ({{ favoriteBookmarks?.length }})
              </a>
            </li>
            <li>
              <a :class="folder === 'archived' ? 'is-active' : ''" href="#" @click="folder = 'archived'">
                <span class="icon">
                  <Icon name="mdi:archive" />
                </span>
                Archived ({{ archivedBookmarks?.length }})
              </a>
            </li>
          </ul>
        </nav>
      </div>

      <div class="column">
        <h1 class="title ">Bookmarks</h1>

        <nav class="level">
          <div class="level-left">
            <div class="level-item">
              <p class="subtitle is-5">
                <strong>{{ data?.length }}</strong> total
              </p>
            </div>
            <div class="level-item is-hidden-tablet-only">
              <div class="field has-addons">
                <p class="control">
                  <input class="input" type="text" placeholder="Title, description…">
                </p>
                <p class="control">
                  <button class="button">
                    Search
                  </button>
                </p>
              </div>
            </div>
          </div>

          <div class="level-right">
            <p class="level-item">
              <strong v-if="filter === 'all'">All</strong>
              <a v-else @click="filter = 'all'">All</a>
            </p>
            <p class="level-item">
              <strong v-if="filter === 'unread'">Unread</strong>
              <a v-else @click="filter = 'unread'">Unread</a>
            </p>
            <p class="level-item">
              <strong v-if="filter === 'read'">Read</strong>
              <a v-else @click="filter = 'read'">Read</a>
            </p>
          </div>
        </nav>

        <table class="table is-hoverable is-fullwidth">
          <thead>
            <tr>
              <th>
                <Icon name="material-symbols:star" />
              </th>
              <th>Title</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tfoot>
            <tr>
              <th>
                <Icon name="material-symbols:star" />
              </th>
              <th>Title</th>
              <th>Actions</th>
            </tr>
          </tfoot>
          <tbody>
            <tr v-for="bookmark in bookmarks" :key="bookmark.id">
              <td>
                <Icon name="material-symbols:star" v-if="bookmark.is_favorite" />
              </td>
              <td>
                <a :href="bookmark.url" target="_blank">{{ bookmark.title }}</a>
                <template v-if="bookmark.tags.length">
                  <span class="tag is-info is-light ml-1" v-for="tag in bookmark.tags">{{ tag.title }}</span>
                </template>
              </td>
              <td>
                <a class="button is-link is-small is-inverted"
                  :href="`${config.public.apiBase}/admin/bookmarks/bookmark/${bookmark.id}/change/`" target="_blank">
                  <Icon name="mdi:book-edit" />
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>
</template>

<style>
@import 'bulma/css/bulma.css'
</style> 