<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { Bookmark, Tag, Folder } from '@/types';

// "auth" middleware redirects user to login page if not authenticated:
definePageMeta({
  middleware: "auth",
});

const authStore = useAuthStore();
const config = useRuntimeConfig();
console.log("API base is " + config.public.apiBase);

// All data fetched from API endpoints will be stored in these arrays:
const allBookmarks: Ref<Bookmark[] | null> = ref(null);
const allTags: Ref<Tag[] | null> = ref(null);
const allUserFolders: Ref<Folder[] | null> = ref(null);
const fetchErrors: Ref<string[]> = ref([]);

// App UI state:
const selectedFolder: Ref<string> = ref("inbox");
const selectedFilter: Ref<string> = ref("all");
const selectedUserFolderId: Ref<number> = ref(1);
const filterByTagsList: Ref<Tag[]> = ref([]);
const searchString: Ref<string> = ref("");

async function fetchData() {
  const { data: bookmarks, error: bookmarksError } = await useFetch<Bookmark[]>(() => `${config.public.apiBase}/api/v1/bookmarks/`, {
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ]
  });
  const { data: folders, error: foldersError } = await useFetch<Folder[]>(() => `${config.public.apiBase}/api/v1/folders/`, {
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ]
  });
  const { data: tags, error: tagsError } = await useFetch<Tag[]>(() => `${config.public.apiBase}/api/v1/tags/`, {
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ]
  });

  allBookmarks.value = bookmarks.value;
  allTags.value = tags.value;
  allUserFolders.value = folders.value;

  fetchErrors.value = [];

  if (bookmarksError.value) {
    fetchErrors.value.push(bookmarksError.value.message);
  }
  if (tagsError.value) {
    fetchErrors.value.push(tagsError.value.message);
  }
  if (foldersError.value) {
    fetchErrors.value.push(foldersError.value.message);
  }
}

const isDataFetched = computed(() => {
  // Whether all needed data fetched from API, or not:
  return allBookmarks.value && allTags.value && allUserFolders.value;
});

/*
  Bookmark-related properties
*/
const totalBookmarksQty = computed(() => {
  // Total number of bookmarks in DB
  return allBookmarks.value?.length;
});

const inboxBookmarks = computed(() => {
  // Array of bookmarks with no folder assigned and not archived
  return allBookmarks.value?.filter((bookmark) => !bookmark.folder && !bookmark.is_archived);
});

const favoriteBookmarks = computed(() => {
  // Array of all "favorite" bookmarks in DB
  return allBookmarks.value?.filter((bookmark) => bookmark.is_favorite);
});

const archivedBookmarks = computed(() => {
  // Array of all "archived" bookmarks in DB
  return allBookmarks.value?.filter((bookmark) => bookmark.is_archived);
});

const bookmarks = computed(() => {
  // Here we do ALL the filtering
  let filteredBookmarks: Bookmark[] = allBookmarks.value ? allBookmarks.value : [];

  // Filter by FOLDER
  if (selectedFolder.value === "inbox") {
    filteredBookmarks = filteredBookmarks.filter((bookmark) => !bookmark.folder && !bookmark.is_archived);
  } else if (selectedFolder.value === "favorites") {
    filteredBookmarks = filteredBookmarks.filter((bookmark) => bookmark.is_favorite);;
  } else if (selectedFolder.value === "archived") {
    filteredBookmarks = filteredBookmarks.filter((bookmark) => bookmark.is_archived);
  } else if (selectedFolder.value === "userFolder") {
    filteredBookmarks = filteredBookmarks.filter(
      (bookmark) => bookmark.folder?.id === selectedUserFolderId.value && !bookmark.is_archived
    );
  }

  // Filter by ALL, READ, UNREAD status
  if (selectedFilter.value === "unread") {
    filteredBookmarks = filteredBookmarks.filter((bookmark) => !bookmark.is_read);
  } else if (selectedFilter.value === "read") {
    filteredBookmarks = filteredBookmarks.filter((bookmark) => bookmark.is_read);
  }

  // Filter by TAGS selected
  if (filterByTagsList.value.length) {
    // Here we check each `selected` tag, if it is present in bookmark's tag list. If so, we pass this bookmark to list.
    filteredBookmarks = filteredBookmarks.filter((bookmark) => filterByTagsList.value.every((tag) => bookmark.tags.filter((bkmrkTag) => bkmrkTag.id === tag.id).length));
  }

  // Filter by search string, look for substring in bookmark's title:
  if (searchString.value?.trim().length >= 3) {
    filteredBookmarks = filteredBookmarks.filter((bookmark) => bookmark.title.toLowerCase().includes(searchString.value.toLowerCase()));
  }

  return filteredBookmarks;
});

/*
  Do the initial data fetching
*/
fetchData();
</script>

<template>
  <Title>Your Bookmarks | Bookmarks</Title>

  <BulmaNotification type="danger" v-if="fetchErrors.length">
    <strong>Some errors occured while trying to fetch data from API.</strong>
    <br>
    <template v-for="error in fetchErrors" :key="error">
      {{ error }}<br>
    </template>
  </BulmaNotification>

  <div class="columns" v-if="isDataFetched && !fetchErrors.length">
    <!-- Left Sidebar -->
    <div class="column sidebar is-4-tablet is-3-desktop is-2-widescreen">
      <!-- Built-in Folders list -->
      <nav class="menu">
        <p class="menu-label">
          Folders
        </p>
        <ul class="menu-list">
          <li>
            <a :class="selectedFolder === 'all' ? 'is-active' : ''" href="#" @click="selectedFolder = 'all'">
              <span class="icon">
                <Icon name="mdi:database" />
              </span>
              All ({{ totalBookmarksQty }})
            </a>
          </li>
          <li>
            <a :class="selectedFolder === 'inbox' ? 'is-active' : ''" href="#" @click="selectedFolder = 'inbox'">
              <span class="icon">
                <Icon name="mdi:inbox" />
              </span>
              Inbox ({{ inboxBookmarks?.length }})
            </a>
          </li>
          <li>
            <a :class="selectedFolder === 'favorites' ? 'is-active' : ''" href="#" @click="selectedFolder = 'favorites'">
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
          <li v-for="folder in allUserFolders" :key="`folder-id-${folder.id}`">
            <a href="#" :class="selectedFolder === 'userFolder' && selectedUserFolderId === folder.id ? 'is-active' : ''"
              @click="{
                selectedFolder='userFolder';
                selectedUserFolderId=folder.id;
              }">
              <span class="icon">
                <Icon name="mdi:folder" />
              </span>
              {{ folder.title }} ({{ folder.bookmarks_qty }})
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
              <strong>{{ bookmarks.length }}</strong> shown, {{ totalBookmarksQty }} total
            </p>
          </div>
          <div class="level-item is-hidden-tablet-only">
            <div class="field has-addons">
              <p class="control">
                <input class="input" type="text" placeholder="Start typing to search..." v-model="searchString">
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
              Look for:
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
        Sorry, there's no bookmarks matching applied filters.
      </BulmaNotification>
    </div>
  </div>
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
</style>