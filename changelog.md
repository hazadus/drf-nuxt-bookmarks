## 30.04.2023, Sun

- 12:50 - Frontend: added i18n to `AddFolderMenuItem` component.
- 13:05 - Frontend: refactored "Search" field on "Bookmarks" page.
- 14:40 - Frontend: created home page with basic app feature list.

## 29.04.2023, Sat

- 17:30 - Frontend: added disk usage info to user profile.
- 19:50 - Frontend: added "Upload profile picture" form on "User profile"/"Edit profile" page. It works without any 
  changes on the backend!

## 27.04.2023, Thu

- 18:00 - Backend: extended `CustomUser` model and `CustomUserSerializer` with `disk_quota`, `disk_space_used` 
  fields. Fields added to test (`test_logged_in_user_detail_api`).
- 20:00 - Frontend: added meaningful messages on server errors (i.e. not enough quota) when starting download.
- 20:30 - Backend: added test to ensure that download won't start if user has no disk quota.

## 26.04.2023, Wed

- 22:10 - Tests: added "Edit user profile" functional test.

## 25.04.2023, Tue

- 15:00 - Tests: functional test extended.
- 21:45 - Tests: added YouTube video download to functional test, and refactored it to several methods.
- 22:30 - Tests: added bookmark editing to functional test and refactored it.

## 24.04.2023, Mon

- 10:30 - Backend: refactor video download-related code and comments. Used Celery's built-in tools for retrying 
  failed tasks.
- 14:00 - Frontend: refactored key-related code for better reactive UI updates.
- 18:00 - Tests: created basic functional test using Selenium.

## 23.04.2023, Sun

- 18:20 - Front + Back: "Download" button on the frontend is more or less working.
- 18:30 - Backend: `Download.bookmark` type changed to `OneToOneField`.
- 18:40 - Front + Back: refactored according to new `Download.bookmark` type.
- 19:40 - Backend: added retries to `download_from_youtube()` because of `pytube` bug.

## 22.04.2023, Sat

- 10:25 - Backend: added `IsOwnerOnly` permission to (almost) all views in `bookmarks/views.py`.
- 10:40 - Backend: created `BookmarkDeleteView` (`bookmarks/delete/<int:pk>/`) endpoint.
- 11:10 - Frontend: added "Delete" button in bookmark edit modal, wired up with backend.
- 13:00 - Backend: created `Download` model. Updated download task.
- 14:30 - Backend: fixed issue when downloaded video file wasn't deleted with the model instance.
- 17:15 - Backend: added Download model serializer.
- 18:45 - Frontend: modified Bookmark editor modal to show Downloads-related stuff.
- 19:00 - Backend: created endpoint to start content download.

## 21.04.2023, Fri

- 09:50 - Frontend: Footer translated.
- 10:15 - Frontend: NavBar translated.
- 10:45 - Frontend: "Sign up" page translated.
- 11:05 - Frontend: "Log in" page translated.
- 11:30 - Frontend: "Add Bookmark" page translated.
- 14:15 - Frontend: "User profile" page translated.
- 16:00 - Frontend: "Folders" page translated.
- 16:35 - Frontend: "Bookmarks" page translated.
- 17:15 - Backend: added Redis.
- 17:30 - Backend: added Celery.

## 20.04.2023, Thu

- 20:30 - Frontend: added loading indicator on "Refresh" button (issue #35).
- 20:45 - Frontend: added loading indicator on "Save changes" button (issue #35).
- 21:00 - Frontend: added loading indicator on the Bookmarks page on initial data fetch (issue #35).
- 22:00 - Frontend: `nuxt/i18n` configured.

## 19.04.2023, Wed

- 22:30 - Frontend: added loading indicator when adding new bookmark (issue #35).

## 18.04.2023, Tue
- 14:00 - Frontend: UI tweaks, see issue #35.

## 17.04.2023, Mon

- 15:00 - Frontend: implemented "Manage folders" page UI.
- 19:40 - Backend: created endpoints to create, update and delete user folders.
- 20:30 - Frontend: wired up to create, edit and delete user folders.

## 16.04.2023, Sun

- 22:00 - Frontend: created "Add new folder" component UI for "Bookmarks" page sidebar.

## 15.04.2023, Sat

- 00:10 - Frontend: created "Add new bookmark" page.
- 00:50 - Front + Back: wired up to create new bookmarks via web page.
- 16:00 - Frontend: "Add bookmark" page UI tweaks.
- 22:30 - Backend: added some tests. Total test coverage is 100%! Fixed some bugs along the way.
- 22:50 - Backend: fixed all `flake8` warnings.

## 14.04.2023, Fri

- 18:00 - Backend: added Sentry integration.
- 18:30 - Frontend: tags can be added and removed in Bookmark editor (only existing tags).
- 19:15 - Backend: tags now saved in DB.
- 21:40 - Frontend: UI tweaks and fixes for mobile screens.

## 13.04.2023, Thu

- 19:00 - Frontend: implemented modal form for bookmark editing (tags only displayed for now, can't be changed 
  removed or added).
- 19:20 - Backend: `BookmarkUpdateView` (`bookmarks/update/<int:pk>/`) endpoint created.
- 21:20 - Front + Back: Bookmark edit form wired with API.

## 12.04.2023, Wed

- 20:30 - Frontend: "Edit profile" form and buttons created.
- 22:05 - Backend: added `/user/<int:pk>` endpoint for partial user profile updates with `PATCH` method.
- 23:00 - Backend + Frontend: profile update form wired with API.

## 11.04.2023, Tue

- 19:10 - Frontend: login page now redirects authenticated users to profile page.
- 21:00 - Frontend: sign up page implemented.
- 23:10 - Frontend: UI fixes (icons in sidebar,drop-down menu in navbar). "About" page updated.
- 23:59 - Bot: more detailed bot's replies.

## 10.04.2023, Mon

- 13:00 - Frontend: Basic Login page created.
- 13:40 - Backend: `UserDetailView` (`/user/details/`) endpoint added.
- 15:00 - Frontend: login page wired with backend. "Auth" middleware added.
- 16:00 - Frontend: added auth token to bookmarks, folders fetches.
- 16:55 - Front + Back: only tags applied to user's bookmarks are listed.
- 17:05 - Front + Back: added count of bookmarks in each user folder. Archived bookmarks excluded from counting.
- 17:55 - Frontend: added basic user profile page.

### 09.04.2023, Sun

- 01:30 - Frontend: created bookmark filter by tags.
- 19:30 - `bookmarks.vue` significantly refactored.
- 19:50 - Added bookmark search by it's title.
- 23:50 - Pinia integrated into project.

### 08.04.2023, Sat

- 00:15 - Endpoints `tags/` and `folders/` added.
- 01:00 - Frontend: added list of user-created folders and tags in sidebar.
- 22:00 - Frontend: App.vue refactored to some components and pages.

### 07.04.2023, Fr

- 11:00 - App deployed to Timeweb.cloud.
- 16:00 - Admin section for Bookmarks tweaked.
- 16:10 - `Bookmark` model extended with `is_read` field.
- 16:50 - `Tag`s added to `Bookmark`s. Serializers adjusted.
- 19:30 - Created basic Nuxt frontend, added Node to Compose.
- 22:10 - Frontend: buttons in left sidebar (Inbox, Favorites, Archived) and filters (All, Unread, Read) were implemented.
- 23:00 - Frontend: added button with a link to admin view for each bookmark in the list.

### 06.04.2023, Thu

- 22:00 - Basic Telegram bot features implemented.
- 23:00 - Added Docker Compose config.

### 05.04.2023, Wed

- 12:50 - Created `users` app with `CustomUser` model.
- 14:00 - Created `bookmarks` app with `Folder` and `Bookmark` models.
- 19:00 - Built DRF API endpoints `bookmarks` and `bookmarks/create_from_telegram`.
- 19:30 - Simple page "meta" content parser added.
- 22:30 - Telegram bot prototype created.

### 03.04.2023, Mo

- 23:15 - project started.
