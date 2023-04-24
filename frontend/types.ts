export type ID = number;

/* 
NB: for interfaces to work correctly with useFetch, property names must match
exactly those set in backend serializers.
*/

export interface User {
  id: number;
  username: string;
  telegram_id: string;
  email: string;
  first_name: string;
  last_name: string;
  profile_image: string;
  is_active: boolean;
  is_staff: boolean;
  is_superuser: boolean;
  last_login: Date;
  date_joined: Date;
}

export interface Folder {
  id: ID;
  user: ID;
  title: string;
  bookmarks_qty?: number;
}

export interface Tag {
  id: ID;
  title: string;
  bookmarks_qty?: number;
}

export interface Download {
  id: ID;
  title: string;
  status: string;
  file: string;
  file_size: number;
  created: Date;
  updated: Date;
}

export interface Bookmark {
  id: ID;
  user: number;
  url: string;
  title: string;
  description: string;
  image_url: string;
  folder: Folder | undefined;
  tags: Tag[];
  download: Download | undefined;
  is_favorite: boolean;
  is_read: boolean;
  is_archived: boolean;
  created: Date;
  updated: Date;
}
