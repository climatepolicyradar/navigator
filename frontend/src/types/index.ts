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
