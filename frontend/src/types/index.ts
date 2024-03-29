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

export type TRedirect = {
  source: string;
  destination: string;
  permanent: boolean;
};

export type TPassageBlockCoords = [number, number];

export type TPassage = {
  text: string;
  text_block_coords: TPassageBlockCoords[];
  text_block_id: string;
  text_block_page: number;
};

export type TDocument = {
  document_category: TEventCategory;
  document_content_type: string;
  document_geography: string;
  document_country_english_shortname: string;
  document_date: string;
  document_description: string;
  document_description_match: boolean;
  document_slug: string;
  document_name: string;
  document_postfix: string;
  document_passage_matches: TPassage[];
  document_source_name: string;
  document_source_url: string;
  document_title_match: boolean;
  document_type: string;
  document_url: string;
  document_fileid?: string;
};

export type TGeography = {
  id: number;
  display_value: string;
  value: string;
  type: string;
  parent_id: number | null;
  slug: string;
};

export type TTarget = {
  target: string;
  group: string;
  base_year: string;
  target_year: string;
};

export type TGeographyConfigNode = {
  id: number;
  display_value: string;
  value: string;
  type: string;
  parent_id: number;
  slug: string;
};

export type TGeographyConfig = {
  node: TGeographyConfigNode;
  children: TGeographyConfig[];
};

export type TGeographyStats = {
  name: string;
  geography_slug: string;
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
  postfix: string;
  slug: string;
  publication_ts: string;
  category?: TCategory;
};
