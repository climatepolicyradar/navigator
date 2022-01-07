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
  source_id: string;
  name: string;
  description: string;
  year: string;
  month: string;
  day: string;
  geography_id: string;
  type_id: string;
  documents: Document[];
}
