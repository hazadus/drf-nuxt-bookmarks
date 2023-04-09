<script setup lang="ts">
import type { Bookmark, Tag, Folder } from '@/types';
import { _AsyncData } from 'nuxt/dist/app/composables/asyncData';
import { FetchError } from 'ofetch';

const config = useRuntimeConfig();

// Some code redundancy here, but I want to make them typed and reactive same time:
let bookmarksPromise: _AsyncData<Bookmark[], FetchError<any> | null> = await useFetch<Bookmark[]>(() => `${config.public.apiBase}/api/v1/bookmarks/`);
let tagsPromise: _AsyncData<Tag[], FetchError<any> | null> = await useFetch<Tag[]>(() => `${config.public.apiBase}/api/v1/tags/`);
let userFoldersPromise: _AsyncData<Folder[], FetchError<any> | null> = await useFetch<Folder[]>(() => `${config.public.apiBase}/api/v1/folders/`);

console.log("API base is " + config.public.apiBase);

let selectedFolder: Ref<string> = ref("inbox");
let selectedFilter: Ref<string> = ref("all");
let selectedUserFolderId: Ref<number> = ref(1);
let filterByTagsList: Ref<Tag[]> = ref([]);
let searchString: Ref<string> = ref("");

async function fetchData() {
  bookmarksPromise = await useFetch<Bookmark[]>(() => `${config.public.apiBase}/api/v1/bookmarks/`);
  tagsPromise = await useFetch<Tag[]>(() => `${config.public.apiBase}/api/v1/tags/`);
  userFoldersPromise = await useFetch<Folder[]>(() => `${config.public.apiBase}/api/v1/folders/`);
}

const isDataFetched = computed(() => {
  // Whether all needed data fetched from API, or not:
  return bookmarksPromise?.data.value && userFoldersPromise?.data.value && tagsPromise?.data.value;
});

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

const bookmarksFiltered = computed(() => {
  // This list we will render in the table.
  if (selectedFilter.value === "all") {
    return bookmarksInSelectedFolder.value;
  } else if (selectedFilter.value === "unread") {
    return bookmarksInSelectedFolder.value?.filter((bookmark) => !bookmark.is_read);
  } else if (selectedFilter.value === "read") {
    return bookmarksInSelectedFolder.value?.filter((bookmark) => bookmark.is_read);
  }
});

const bookmarks = computed(() => {
  // Filter only bookmarks which have all selected tags
  if (!filterByTagsList.value.length) {
    return bookmarksFiltered.value;
  } else {
    // Here we check each `selected` tag, if it is present in bookmark's tag list. If so, we pass this bookmark to list.
    return bookmarksFiltered.value?.filter((bookmark) => filterByTagsList.value.every((tag) => bookmark.tags.filter((bkmrkTag) => bkmrkTag.id === tag.id).length));
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

  <section class="section bookmarks" v-if="isDataFetched">
    <div class="container is-widescreen">
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
                <a :class="selectedFolder === 'archived' ? 'is-active' : ''" href="#"
                  @click="selectedFolder = 'archived'">
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
              <li v-for="folder in allUserFolders" :key="`folder-id-${folder.id}`">
                <a href="#"
                  :class="selectedFolder === 'userFolder' && selectedUserFolderId === folder.id ? 'is-active' : ''"
                  @click="{
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
              All Tags
            </p>
          </nav>
          <BulmaTagList v-if="allTags?.length">
            <BulmaTag v-for="tag in allTags" :key="`tag-id-${tag.id}`" :tag="tag" :hasDeleteButton="false"
              @click="filterByTagsList.push(tag)" />
          </BulmaTagList>
        </div>

        <div class="column">
          <h1 class="title ">Bookmarks</h1>

          <!-- Level = search, filters -->
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
                    <input class="input" type="text" placeholder="Title, description…" v-model="searchString">
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
              <p class="level-item">
                <button class="button is-info" @click="fetchData">Refresh</button>
              </p>
            </div>
          </nav>

          <!-- Level = show search string -->
          <nav class="level" v-if="searchString.trim().length >= 3">
            <!-- Left side -->
            <div class="level-left">
              <div class="level-item">
                <p class="subtitle is-5">
                  Filter by:
                </p>
              </div>
              <div class="level-item">
                {{ searchString }}
              </div>
            </div>

            <!-- Right side -->
            <div class="level-right">
              <p class="level-item">
                <button class="button is-warning" @click="searchString = ''">Reset</button>
              </p>
            </div>
          </nav>


          <!-- Level = filter by tags -->
          <nav class="level" v-if="filterByTagsList.length">
            <!-- Left side -->
            <div class="level-left">
              <div class="level-item">
                <p class="subtitle is-5">
                  Filter by:
                </p>
              </div>
              <div class="level-item">
                <BulmaTagList>
                  <BulmaTag v-for="tag in filterByTagsList" :key="`tag-filter-id-${tag.id}`" :tag="tag"
                    :hasDeleteButton="true"
                    @delete="filterByTagsList = filterByTagsList.filter((tag) => tag.id != $event.id)" />
                </BulmaTagList>
              </div>
            </div>

            <!-- Right side -->
            <div class="level-right">
              <p class="level-item">
                <button class="button is-warning" @click="filterByTagsList = []">Reset</button>
              </p>
            </div>
          </nav>

          <!-- Bookmarks list or notification if list is empty -->
          <table class="table is-hoverable is-fullwidth" v-if="bookmarks?.length">
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
              <tr v-for="bookmark in bookmarks" :key="`bookmark-id-${bookmark.id}`">
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
          <BulmaNotification v-else>
            Sorry, the folder you selected is empty.
          </BulmaNotification>
        </div>
      </div>
    </div>
  </section>

  <section v-else class="section errors">
    <div class="container is-widescreen">
      <BulmaNotification type="danger">
        <strong>Some errors occured while trying to fetch data from API.</strong>
        <template v-if="bookmarksPromise?.error.value">
          <br>{{ bookmarksPromise.error.value }}
        </template>
        <template v-if="userFoldersPromise?.error.value">
          <br>{{ userFoldersPromise.error.value }}
        </template>
        <template v-if="tagsPromise?.error.value">
          <br>{{ tagsPromise.error.value }}
        </template>
      </BulmaNotification>
    </div>
  </section>
</template>

<style scoped>
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

.bookmarks,
.errors {
  min-height: calc(100vh - 52px - 168px);
}
</style>