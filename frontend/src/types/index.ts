export type TSector = {
  description: string;
  id: number;
  name: string;
  parent_id?: number;
  source_id: number;
};

export type TCountry = {
  name: string;
  short_name: string;
  continent: string;
  legal_structure: string;
  legal_bodies: string;
  political_groups: string[];
  financial_status: string;
  gcri: number;
  emissions: number;
  laws: number;
  policies: number;
  cases: number;
  events: TEvent[];
  targets: TTarget[];
  documents: TAssociatedDocument[];
};

export type TTarget = {
  target: string;
  group: string;
  base_year: string;
  target_year: string;
};

export type TCategory = "Laws" | "Policies" | "Cases" | "Targets";

export type TEvent = {
  name: string;
  created_ts: string;
  description: string;
  category?: TCategory;
};

export type TAssociatedDocument = {
  country_code: string;
  country_name: string;
  description: string;
  name: string;
  publication_ts: string;
  related_id: number;
  category?: TCategory;
}
