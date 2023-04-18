<script setup lang="ts">
import { useAuthStore } from '@/stores/AuthStore';
import type { Bookmark, Tag, Folder } from '@/types';

const props = defineProps({
  bookmark: {
    type: Object as PropType<Bookmark>,
    required: true,
  },
  allTags: {
    type: Array as PropType<Array<Tag>>,
    required: true,
  },
  allFolders: {
    type: Array as PropType<Array<Folder>>,
    required: true,
  },
});

const emit = defineEmits<{
  (e: "close", isVisible: boolean): void;
  (e: "updated", isUpdated: boolean): void;
}>();

const authStore = useAuthStore();
const config = useRuntimeConfig();

const editableBookmark: Ref<Bookmark> = ref(props.bookmark);
const assignedTags: Ref<Tag[]> = ref(props.bookmark.tags);
const selectedFolderID: Ref<number> = ref(0);

if (props.bookmark.folder?.id) {
  selectedFolderID.value = props.bookmark.folder.id;
} else {
  // This is to prevent weird 400 errors when patching with `null` value.
  editableBookmark.value.folder = undefined;
}

const availableTags = computed(() => {
  // All site tags except tags already assigned to the bookmark
  return props.allTags.filter((tag) => assignedTags.value.filter((assignedTag) => assignedTag.id === tag.id).length === 0);
});

async function onClickShare() {
  navigator.share({
    title: props.bookmark.title,
    text: props.bookmark.description,
    url: props.bookmark.url,
  });
}

function closeModal() {
  emit("close", false);
}

async function onClickSaveChanges() {
  /*
    Send updated bookmark data to API using "PATCH" method (partial update).
  */

  if (selectedFolderID.value) {
    // Find folder object with selected id
    const selectedFolder = props.allFolders.filter((folder) => folder.id === selectedFolderID.value)[0];
    editableBookmark.value.folder = selectedFolder;
  } else {
    editableBookmark.value.folder = undefined;
  }

  const formData = {
    // NB: DRF won't accept URLs with spaces and stuff, hence `encodeURI`:
    url: editableBookmark.value.url.trim().length ? encodeURI(editableBookmark.value.url) : "",
    title: editableBookmark.value.title,
    description: editableBookmark.value.description,
    image_url: editableBookmark.value.image_url.trim().length ? encodeURI(editableBookmark.value.image_url) : "",
    folder: editableBookmark.value.folder,
    tags: assignedTags.value,
    is_favorite: editableBookmark.value.is_favorite,
    is_read: editableBookmark.value.is_read,
    is_archived: editableBookmark.value.is_archived,
  }

  const { data: bookmarkData, error: bookmarkUpdateError } = await useFetch(() => `${config.public.apiBase}/api/v1/bookmarks/update/${props.bookmark.id}/`, {
    method: "PATCH",
    headers: [
      ["Authorization", "Token " + authStore.token,],
    ],
    body: formData,
  });

  if (bookmarkUpdateError.value) {
    console.error("Error updating bookmark data: " + bookmarkUpdateError.value?.message);
    alert("Something went wrong. Please try again!");
    return;
  }

  emit("updated", true);
  closeModal();
}
</script>

<template>
  <div class="modal">
    <div class="modal-background" @click="closeModal"></div>
    <div class="modal-card the-card">
      <section class="modal-card-body">
        <!-- Content ... -->
        <div class="columns">
          <div class="column is-8">
            <div class="field">
              <label class="label">Title</label>
              <div class="control">
                <input class="input" type="text" placeholder="Bookmark title" v-model="editableBookmark.title">
              </div>
            </div>

            <div class="field">
              <label class="label">Bookmark URL</label>
              <div class="control">
                <input class="input" type="text" placeholder="Cover image URL" v-model="editableBookmark.url">
              </div>
            </div>

            <div class="field">
              <label class="label">Image URL</label>
              <div class="control">
                <input class="input" type="text" placeholder="Cover image URL" v-model="editableBookmark.image_url">
              </div>
            </div>

          </div>

          <div class="column is-4 cover-image ">
            <!-- Cover image -->
            <figure class="image is-16by9 " v-if="editableBookmark.image_url">
              <img :src="editableBookmark.image_url">
            </figure>
          </div>
        </div>

        <div class="field">
          <label class="label">Description</label>
          <div class="control">
            <textarea class="textarea" placeholder="Bookmark description"
              v-model="editableBookmark.description"></textarea>
          </div>
        </div>

        <div class="columns">
          <!-- Folder & checkboxes -->
          <div class="column is-4">
            <div class="field">
              <label class="label">Folder</label>
              <div class="control">
                <div class="select">

                  <select v-model="selectedFolderID">
                    <option value="0">
                      None
                    </option>
                    <option v-for="folder in allFolders" v-bind:value="folder.id" :key="`folder-id-${folder.id}`">
                      {{ folder.title }}
                    </option>
                  </select>

                </div>
              </div>
            </div>

            <!-- Checkboxes -->
            <div class="field">
              <label class="label">Status</label>
              <div class="control">
                <label class="checkbox mr-2">
                  <input type="checkbox" v-model="editableBookmark.is_favorite">
                  Favorite
                </label>
                <label class="checkbox mr-2">
                  <input type="checkbox" v-model="editableBookmark.is_read">
                  Read
                </label>
                <label class="checkbox">
                  <input type="checkbox" v-model="editableBookmark.is_archived">
                  Archived
                </label>
              </div>
            </div>
          </div>

          <!-- Assigned Tags -->
          <div class="column is-4">
            <div class="field">
              <label class="label">Assigned Tags</label>
              <div class="control">

                <BulmaTagList v-if="assignedTags.length">
                  <BulmaTag v-for="tag in assignedTags" :tag="tag" :hasDeleteButton="true" :key="`assigned-tag-${tag.id}`"
                    @delete="assignedTags = assignedTags.filter((tag) => tag.id != $event.id)">
                    {{ tag.title }}
                  </BulmaTag>
                </BulmaTagList>

              </div>
            </div>
          </div>

          <!-- Available Tags -->
          <div class="column is-4">
            <div class="field">
              <label class="label">Available Tags</label>
              <div class="control">

                <BulmaTagList v-if="availableTags.length">
                  <BulmaTag v-for="tag in availableTags" :tag="tag" :hasDeleteButton="false" :hasCounter="true"
                    :key="`all-tags-${tag.id}`" @clickTag="assignedTags.push(tag)">
                    {{ tag.title }}
                  </BulmaTag>
                </BulmaTagList>

              </div>
            </div>
          </div>

        </div>

      </section>
      <footer class="modal-card-foot">
        <button class="button mr-5" @click="onClickShare">
          <span>Share</span>
          <Icon name="material-symbols:share" />
        </button>
        <button class="button" @click="closeModal">Cancel</button>
        <button class="button is-success" @click="onClickSaveChanges">Save changes</button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.the-card {
  width: calc(100vw - 100px) !important;
}

.cover-image {
  margin-top: 36px;
}

@media (max-width: 768px) {
  .the-card {
    width: calc(100vw - 10px) !important;
    margin-left: 0 !important;
    margin-right: 0 !important;
  }

  .cover-image {
    margin-top: 0;
  }
}
</style>