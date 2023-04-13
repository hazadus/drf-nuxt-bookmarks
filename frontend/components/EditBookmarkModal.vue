<script setup lang="ts">
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
}>();

const editableBookmark: Ref<Bookmark> = ref(props.bookmark);
const selectedFolder: Ref<number> = ref(0);

if (props.bookmark.folder?.id) {
  selectedFolder.value = props.bookmark.folder.id;
}

function closeModal() {
  emit("close", false);
}

function onClickSaveChanges() {
  /*
    Send updated bookmark data to API using "PATCH" method (partial update).
  */

  if (selectedFolder.value) {
    /*
      If a folder was selected, save it's `id` in bookmark object. We don't care
      about user id and folder title because backend will refer to folder id (which is unique)
      to get it from the DB and assign to the bookmark.
    */
    editableBookmark.value.folder = {
      id: selectedFolder.value,
      user: 0,
      title: "",
    }
  }

  console.log("editableBookmark = ", editableBookmark.value);
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
            <figure class="image is-3by2 mt-6" v-if="editableBookmark.image_url">
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

                  <select v-model="selectedFolder">
                    <option value="0">
                      None
                    </option>
                    <option v-for="folder in allFolders" v-bind:value="folder.id">
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
                  <BulmaTag v-for="tag in editableBookmark.tags" :tag="tag" :hasDeleteButton="true">
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
                  <BulmaTag v-for="tag in allTags" :tag="tag" :hasDeleteButton="false" :hasCounter="true">
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