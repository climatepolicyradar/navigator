// You can include shared interfaces/types in a separate file
// and then use them in any component by importing them. For
// example, to import the interface below do:
//
// import { User } from 'path/to/interfaces';

export type User = {
  id: number;
  name: string;
};

export interface Document {
  name: string;
  language_id: string;
  source_url: string;
  s3_url: string;
  year: string;
  month: string;
  day: string;
}

export interface Action {
  action_source_id: string;
  name: string;
  description: string;
  year: string;
  month: string;
  day: string;
  geography_id: string;
  action_type_id: string;
  documents: Document[];
}

export interface Geography {
  country_code: string;
  english_shortname: string;
  french_shortname: string;
  geography_id: number;
}

export interface Language {
  language_id: number;
  language_code: string;
  part1_code: null;
  part2_code: null;
  name: string;
}

export interface ActionType {
  action_type_id: number;
  action_parent_type_id: number;
  type_name: string;
  type_description: string;
}

export interface Source {
  source_id: number;
  name: string;
}

export interface SearchCriteria {
  query_string: string; // required
  exact_match: boolean; // required
  max_passages_per_doc: number; // default 10
  keyword_filters: {
    action_geography_english_shortname: string[];
    action_source_name: string[];
    // more filter keys to be provided
  };
  year_range: [number, number];
  sort_field: string; // "title" or "date"
  sort_order: string; // "desc" or "asc"
  limit: number; // default 10
  offset: number;
}
