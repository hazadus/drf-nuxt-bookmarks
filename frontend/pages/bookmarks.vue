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
const isEditBookmarkModalVisible: Ref<boolean> = ref(true);
const selectedBookmark: Ref<Bookmark | null> = ref(null);

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

function onClickEditBookmark(bookmark: Bookmark) {
  selectedBookmark.value = bookmark;
  isEditBookmarkModalVisible.value = true;
}

/*
  Do the initial data fetching
*/
fetchData();
</script>

<template>
  <Title>Your Bookmarks | Bookmarks</Title>

  <!-- NB: `:key="selectedBookmark.id"` is to re-render component on each `selectedBookmark` change. -->
  <EditBookmarkModal v-if="selectedBookmark && allTags && allUserFolders" :bookmark="selectedBookmark" :allTags="allTags"
    :allFolders="allUserFolders" :key="selectedBookmark.id" :class="isEditBookmarkModalVisible ? 'is-active' : ''"
    @close="isEditBookmarkModalVisible = $event" @updated="fetchData()" />

  <BulmaNotification type="danger" v-if="fetchErrors.length">
    <strong>Some errors occured while trying to fetch data from API.</strong>
    <br>
    <template v-for="error in fetchErrors" :key="error">
      {{ error }}<br>
    </template>
  </BulmaNotification>

  <div class="columns" v-if="isDataFetched && !fetchErrors.length">
    <!-- Left Sidebar -->
    <div class="column sidebar p-0 mt-3 is-3-tablet is-3-desktop is-2-widescreen is-2-fullhd">
      <!-- Built-in Folders list -->
      <nav class="menu">
        <p class="menu-label">
          Folders
        </p>
        <ul class="menu-list">
          <li>
            <a :class="selectedFolder === 'all' ? 'is-active' : ''" href="#" @click="selectedFolder = 'all'">
              <span class="icon-text">
                <span class="icon">
                  <Icon name="mdi:database" />
                </span>
                <span class="mr-3">
                  All
                </span>
                <span class="tag is-light" :key="`totalBookmarksQty-${totalBookmarksQty}`">
                  {{ totalBookmarksQty }}
                </span>
              </span>
            </a>
          </li>
          <li>
            <a :class="selectedFolder === 'inbox' ? 'is-active' : ''" href="#" @click="selectedFolder = 'inbox'">
              <span class="icon-text">
                <span class="icon">
                  <Icon name="mdi:inbox" />
                </span>
                <span class="mr-3">
                  Inbox
                </span>
                <span class="tag is-light" :key="`inboxBookmarks-${inboxBookmarks?.length}`">
                  {{ inboxBookmarks?.length }}
                </span>
              </span>
            </a>
          </li>
          <li>
            <a :class="selectedFolder === 'favorites' ? 'is-active' : ''" href="#" @click="selectedFolder = 'favorites'">
              <span class="icon-text">
                <span class="icon">
                  <Icon name="material-symbols:star" />
                </span>
                <span class="mr-3">
                  Favorites
                </span>
                <span class="tag is-light" :key="`favoriteBookmarks-${favoriteBookmarks?.length}`">
                  {{ favoriteBookmarks?.length }}
                </span>
              </span>
            </a>
          </li>
          <li>
            <a :class="selectedFolder === 'archived' ? 'is-active' : ''" href="#" @click="selectedFolder = 'archived'">
              <span class="icon-text">
                <span class="icon">
                  <Icon name="mdi:archive" />
                </span>
                <span class="mr-3">
                  Archived
                </span>
                <span class="tag is-light" :key="`archivedBookmarks-${archivedBookmarks?.length}`">
                  {{ archivedBookmarks?.length }}
                </span>
              </span>
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
              <span class="icon-text">
                <span class="icon">
                  <Icon name="mdi:folder" />
                </span>
                <span class="mr-3">
                  {{ folder.title }}
                </span>
                <span class="tag is-light" :key="`folder-bookmarks_qty-${folder.bookmarks_qty}`">
                  {{ folder.bookmarks_qty }}
                </span>
              </span>
            </a>
          </li>
        </ul>
      </nav>

      <!-- Tags list -->
      <nav class="menu mt-5">
        <p class="menu-label mb-3">
          Your Tags
        </p>
      </nav>
      <BulmaTagList v-if="allTags?.length">
        <BulmaTag v-for="tag in allTags" :key="`all-tags-tag-id-${tag.id}`" :tag="tag" :hasDeleteButton="false"
          :hasCounter="true" @click="filterByTagsList.push(tag)" />
      </BulmaTagList>
    </div>

    <div class="column bookmarks">
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
        <div class="level-right is-hidden-mobile">
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
            <th class="cell-favorite">
              <Icon name="material-symbols:star" />
            </th>
            <th class="cell-title">Title</th>
            <th class="cell-actions">Actions</th>
          </tr>
        </thead>
        <tfoot>
          <tr>
            <th class="cell-favorite">
              <Icon name="material-symbols:star" />
            </th>
            <th class="cell-title">Title</th>
            <th class="cell-actions">Actions</th>
          </tr>
        </tfoot>
        <tbody>
          <tr v-for="bookmark in bookmarks" :key="`bookmark-id-${bookmark.id}`">
            <td class="cell-favorite has-text-centered">
              <Icon name="material-symbols:star" v-if="bookmark.is_favorite" />
            </td>
            <td class="cell-title">
              <a :href="bookmark.url" target="_blank">{{ bookmark.title }}</a>
              <template v-if="bookmark.tags.length">
                <span class="tag is-info is-light ml-1" v-for="tag in bookmark.tags"
                  :key="`bkmrk-${bookmark.id}-tag-${tag.id}`">
                  {{ tag.title }}
                </span>
              </template>
            </td>
            <td class="cell-actions">
              <button class="button is-link is-small is-inverted" @click="onClickEditBookmark(bookmark)">
                <Icon name="mdi:book-edit" />
              </button>
              <a class="button is-link is-small is-inverted" v-if="authStore.user?.is_superuser"
                :href="`${config.public.apiBase}/admin/bookmarks/bookmark/${bookmark.id}/change/`" target="_blank">
                <Icon name="mdi:cogs" />
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
  /* Won't stick without vh: */
  max-height: 100vh;
  overflow-y: hidden;
  top: 0;
  bottom: 0;
  background-color: white;
  z-index: 1;
}


.cell-favorite {
  width: 24px;
  padding-left: 12px;
  padding-right: 0;
  text-align: center;
}

.cell-actions {
  width: 94px;
  padding-left: 0;
  padding-right: 0;
  text-align: center !important;
}

@media (max-width: 768px) {
  .sidebar {
    /* 
      "Unstick" sidebar on mobile screens.
      Otherwise, it will hinder the content.
    */
    position: relative;
  }

  .bookmarks {
    padding-top: 24px;
    padding-left: 0;
    padding-right: 0;
  }

  .cell-favorite {
    padding-left: 0;
  }

  .cell-title {
    padding-right: 0;
    padding-top: 12px;
    padding-bottom: 12px;
  }

  .cell-actions {
    width: 64px;
  }
}
</style>