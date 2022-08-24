type TErrorDetail = {
  loc: string[];
  msg: string;
  type: string;
};

export type TError = {
  detail: TErrorDetail[];
};

export type TSector = {
  description: string;
  id: number;
  name: string;
  parent_id?: number;
  source_id: number;
};

export type TPassageBlockCoords = [number, number];

export type TPassage = {
  text: string;
  text_block_coords: TPassageBlockCoords[];
  text_block_id: string;
  text_block_page: number;
};

export type TDocument = {
  document_content_type: string;
  document_country_code: string;
  document_country_english_shortname: string;
  document_date: string;
  document_description: string;
  document_description_match: boolean;
  document_id: number;
  document_name: string;
  document_passage_matches: TPassage[];
  document_source_name: string;
  document_source_url: string;
  document_title_match: boolean;
  document_type: string;
  document_url: string;
};

export type TGeography = {
  id: number;
  display_value: string;
  value: string;
  type: string;
  parent_id: number | null;
};

export type TTarget = {
  target: string;
  group: string;
  base_year: string;
  target_year: string;
};

export type TGeographyStats = {
  id: number;
  name: string;
  geography_id: number;
  legislative_process: string;
  federal: boolean;
  federal_details: string;
  political_groups: string;
  global_emissions_percent: number;
  climate_risk_index: number;
  worldbank_income_group: string;
  visibility_status: string;
};

export type TGeographySummary = {
  document_counts: { Law: number; Policy: number; Case: number };
  events: TEvent[];
  targets: string[];
  top_documents: { Law: TDocument[]; Policy: TDocument[]; Case: TDocument[] };
};

export type TCategory = "Law" | "Policy" | "Case";
export type TDisplayCategory = "All" | "Legislative" | "Executive" | "Litigation";

export type TEventCategory = TCategory | "Target";

export type TEvent = {
  name: string;
  created_ts: string;
  description: string;
  category?: TEventCategory;
};

export type TAssociatedDocument = {
  country_code: string;
  country_name: string;
  description: string;
  name: string;
  publication_ts: string;
  related_id: number;
  category?: TCategory;
};
