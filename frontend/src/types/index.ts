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
};

export type TTarget = {
  target: string;
  group: string;
  base_year: string;
  target_year: string;
};

type TEvent = {
  name: string;
  created_ts: string;
  date: string;
  description: string;
};
