<script setup lang="ts">
import type { Bookmark, Tag, Folder } from './types';

const config = useRuntimeConfig();

const bookmarksPromise = await useFetch<Bookmark[]>(() => `${config.public.apiBase}/api/v1/bookmarks/`);
const tagsPromise = await useFetch<Tag[]>(() => `${config.public.apiBase}/api/v1/tags/`);
const userFoldersPromise = await useFetch<Folder[]>(() => `${config.public.apiBase}/api/v1/folders/`);

console.log("API base is " + config.public.apiBase);

let selectedFolder = ref("inbox");
let selectedFilter = ref("all");
let selectedUserFolderId = ref(1);

/*
  Bookmark-related properties
*/
const totalBookmarksQty = computed(() => {
  // Total number of bookmarks in DB
  return bookmarksPromise.data?.value?.length;
});

const inboxBookmarks = computed(() => {
  // Array of bookmarks with no folder assigned and not archived
  return bookmarksPromise.data.value?.filter((bookmark) => !bookmark.folder && !bookmark.is_archived);
});

const favoriteBookmarks = computed(() => {
  // Array of all "favorite" bookmarks in DB
  return bookmarksPromise.data.value?.filter((bookmark) => bookmark.is_favorite);
});

const archivedBookmarks = computed(() => {
  // Array of all "archived" bookmarks in DB
  return bookmarksPromise.data.value?.filter((bookmark) => bookmark.is_archived);
});

const bookmarksInSelectedFolder = computed(() => {
  if (selectedFolder.value === "inbox") {
    return inboxBookmarks.value;
  } else if (selectedFolder.value === "favorites") {
    return favoriteBookmarks.value;
  } else if (selectedFolder.value === "archived") {
    return archivedBookmarks.value;
  } else if (selectedFolder.value === "userFolder") {
    return bookmarksPromise.data.value?.filter(
      (bookmark) => bookmark.folder?.id === selectedUserFolderId.value && !bookmark.is_archived
    );
  }
});

const bookmarks = computed(() => {
  // This list we will render in the table.
  if (selectedFilter.value === "all") {
    return bookmarksInSelectedFolder.value;
  } else if (selectedFilter.value === "unread") {
    return bookmarksInSelectedFolder.value?.filter((bookmark) => !bookmark.is_read);
  } else if (selectedFilter.value === "read") {
    return bookmarksInSelectedFolder.value?.filter((bookmark) => bookmark.is_read);
  }
});

/*
  Tag-related properties
*/
const allTags = computed(() => {
  // List of all existing tags in DB
  return tagsPromise.data.value;
});

/*
  Folder-related properties
*/
const allUserFolders = computed(() => {
  // List of all user-created folders in DB
  return userFoldersPromise.data.value;
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
      <!-- Left Sidebar -->
      <div class="column sidebar is-4-tablet is-3-desktop is-2-widescreen">
        <!-- Built-in Folders list -->
        <nav class="menu">
          <p class="menu-label">
            Folders
          </p>
          <ul class="menu-list">
            <li>
              <a :class="selectedFolder === 'inbox' ? 'is-active' : ''" href="#" @click="selectedFolder = 'inbox'">
                <span class="icon">
                  <Icon name="mdi:inbox" />
                </span>
                Inbox ({{ inboxBookmarks?.length }})
              </a>
            </li>
            <li>
              <a :class="selectedFolder === 'favorites' ? 'is-active' : ''" href="#"
                @click="selectedFolder = 'favorites'">
                <span class="icon">
                  <Icon name="material-symbols:star" />
                </span>
                Favorites ({{ favoriteBookmarks?.length }})
              </a>
            </li>
            <li>
              <a :class="selectedFolder === 'archived' ? 'is-active' : ''" href="#" @click="selectedFolder = 'archived'">
                <span class="icon">
                  <Icon name="mdi:archive" />
                </span>
                Archived ({{ archivedBookmarks?.length }})
              </a>
            </li>
          </ul>
        </nav>

        <!-- User-created folders list -->
        <nav class="menu mt-4">
          <p class="menu-label">
            Your Folders
          </p>
          <ul class="menu-list">
            <li v-for="folder in allUserFolders" :key="folder.id">
              <a href="#"
                :class="selectedFolder === 'userFolder' && selectedUserFolderId === folder.id ? 'is-active' : ''" @click="{
                  selectedFolder='userFolder';
                  selectedUserFolderId=folder.id;
                }">
                <span class="icon">
                  <Icon name="mdi:folder" />
                </span>
                {{ folder.title }}
              </a>
            </li>
          </ul>
        </nav>

        <!-- Tags list -->
        <nav class="menu mt-5">
          <p class="menu-label mb-3">
            Tags
          </p>
        </nav>

        <div v-if="allTags?.length" class="field is-grouped is-grouped-multiline">
          <div class="control" v-for="tag in allTags">
            <div class="tags has-addons">
              <a class="tag is-info is-light">{{ tag.title }}</a>
              <a class="tag">{{ tag.bookmarks_qty }}</a>
            </div>
          </div>
        </div>

      </div>

      <div class="column">
        <h1 class="title ">Bookmarks</h1>

        <nav class="level">
          <!-- Search block -->
          <div class="level-left">
            <div class="level-item">
              <p class="subtitle is-5">
                <strong>{{ totalBookmarksQty }}</strong> total
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

          <!-- Filters right block -->
          <div class="level-right">
            <p class="level-item">Show:</p>
            <p class="level-item">
              <strong v-if="selectedFilter === 'all'">All</strong>
              <a v-else @click="selectedFilter = 'all'">All</a>
            </p>
            <p class="level-item">
              <strong v-if="selectedFilter === 'unread'">Unread</strong>
              <a v-else @click="selectedFilter = 'unread'">Unread</a>
            </p>
            <p class="level-item">
              <strong v-if="selectedFilter === 'read'">Read</strong>
              <a v-else @click="selectedFilter = 'read'">Read</a>
            </p>
          </div>
        </nav>

        <!-- Bookmarks list -->
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
@import 'bulma/css/bulma.css';

.sidebar {
  position: sticky;
  display: inline-block;
  vertical-align: top;
  max-height: 100vh;
  overflow-y: hidden;
  top: 0;
  bottom: 0;
  background-color: white;
  z-index: 1;
}
</style> 