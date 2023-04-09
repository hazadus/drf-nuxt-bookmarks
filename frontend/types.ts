export type ID = number;

/* 
NB: for interfaces to work correctly with useFetch, property names must match
exactly those set in backend serializers.
*/

export interface Folder {
  id: ID;
  user: ID;
  title: string;
}

export interface Tag {
  id: ID;
  title: string;
  bookmarks_qty?: number;
}

export interface Bookmark {
  id: ID;
  user: number;
  url: string;
  title: string;
  description: string;
  image_url: string;
  folder: Folder;
  tags: Tag[];
  is_favorite: boolean;
  is_read: boolean;
  is_archived: boolean;
  created: Date;
  updated: Date;
}