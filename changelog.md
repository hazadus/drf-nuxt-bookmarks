## 15.04.2023, Sat

- 00:10 - Frontend: created "Add new bookmark" page.
- 00:50 - Front + Back: wired up to create new bookmarks via web page.

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
