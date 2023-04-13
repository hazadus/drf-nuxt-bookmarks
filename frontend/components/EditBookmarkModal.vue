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
const selectedFolderID: Ref<number> = ref(0);

if (props.bookmark.folder?.id) {
  selectedFolderID.value = props.bookmark.folder.id;
} else {
  // This is to prevent weird 400 errors when patching with `null` value.
  editableBookmark.value.folder = undefined;
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
    url: editableBookmark.value.url,
    title: editableBookmark.value.title,
    description: editableBookmark.value.description,
    image_url: editableBookmark.value.image_url,
    folder: editableBookmark.value.folder,
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
    <div class="modal-card" style="width: calc(100vw - 100px) !important;">
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

            <div class="field">
              <label class="label">Description</label>
              <div class="control">
                <textarea class="textarea" placeholder="Bookmark description"
                  v-model="editableBookmark.description"></textarea>
              </div>
            </div>
          </div>

          <div class="column is-4">
            <!-- Cover image -->
            <figure class="image is-16by9 mt-6" v-if="editableBookmark.image_url">
              <img :src="editableBookmark.image_url">
            </figure>
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

                <BulmaTagList v-if="editableBookmark.tags.length">
                  <BulmaTag v-for="tag in editableBookmark.tags" :tag="tag" :hasDeleteButton="true"
                    :key="`assigned-tag-${tag.id}`">
                    {{ tag.title }}
                  </BulmaTag>
                </BulmaTagList>

              </div>
            </div>
          </div>

          <!-- Assigned Tags -->
          <div class="column is-4">
            <div class="field">
              <label class="label">Available Tags</label>
              <div class="control">

                <BulmaTagList v-if="allTags.length">
                  <BulmaTag v-for="tag in allTags" :tag="tag" :hasDeleteButton="false" :hasCounter="true"
                    :key="`all-tags-${tag.id}`">
                    {{ tag.title }}
                  </BulmaTag>
                </BulmaTagList>

              </div>
            </div>
          </div>

        </div>

      </section>
      <footer class="modal-card-foot">
        <button class="button" @click="closeModal">Cancel</button>
        <button class="button is-success" @click="onClickSaveChanges">Save changes</button>
      </footer>
    </div>
  </div>
</template>