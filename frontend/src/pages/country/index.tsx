import { TCountry, TTarget, TEvent } from "@types";
import Layout from "@components/layouts/Main";
import { SingleCol } from "@components/SingleCol";
import Event from "@components/blocks/Event";
import { Timeline } from "@components/blocks/Timeline";
import { CountryHeader } from "@components/blocks/CountryHeader";
import { KeyDetail } from "@components/KeyDetail";
import { RelatedDocument } from "@components/blocks/RelatedDocument";
import { LawIcon, PolicyIcon, CaseIcon, TargetIcon } from "@components/svg/Icons";

type TTargets = {
  targets: TTarget[];
};

const Targets = ({ targets }: TTargets) => {
  return (
    <ul className="ml-4 list-disc list-outside">
      {targets.map((target) => (
        <li className="mb-4" key={target.target}>
          <span className="text-blue-700 text-lg">{target.target}</span>
          <span className="block">
            <span className="font-semibold mr-1">{target.group}: ???</span>
            <span>
              | Base year: {target.base_year} | Target year: {target.target_year}
            </span>
          </span>
        </li>
      ))}
    </ul>
  );
};

const CountryPage = () => {
  // TODO: replace with API lookup
  const country = COUNTRY;
  return (
    <Layout title={`Climate Policy Radar | ${country.name}`}>
      <section className="mb-8">
        <CountryHeader country={country} />
        <SingleCol>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-px rounded">
            <KeyDetail detail="Laws" amount={country.laws} icon={<LawIcon />} />
            <KeyDetail detail="Policies" amount={country.policies} icon={<PolicyIcon />} />
            <KeyDetail detail="Cases" amount={country.cases} icon={<CaseIcon />} />
          </div>
          <section className="mt-8">
            <h3 className="mb-4">Events</h3>
            <Timeline>
              {country.events.map((event: TEvent, index: number) => (
                <Event event={event} key={`event-${index}`} index={index} last={index === country.events.length - 1 ? true : false} />
              ))}
            </Timeline>
          </section>
          {country.targets.length && (
            <div className="mt-8">
              <h3 className="flex mb-4">
                <span className="mr-2">
                  <TargetIcon />
                </span>
                Targets ({country.targets.length})
              </h3>
              <Targets targets={country.targets} />
            </div>
          )}
          <section>
            <h3 className="mt-8">Documents</h3>
            {country.documents.map((doc) => (
              <div key={doc.related_id} className="my-4">
                <RelatedDocument document={doc} />
              </div>
            ))}
          </section>
        </SingleCol>
      </section>
    </Layout>
  );
};

export default CountryPage;

const COUNTRY: TCountry = {
  name: "United States of America",
  short_name: "USA",
  continent: "North America",
  legal_structure: "Federal",
  legal_bodies: "50 states",
  political_groups: ["OECD", "EU"],
  financial_status: "High Income",
  gcri: 155.67,
  emissions: 0.13,
  laws: 12,
  policies: 4,
  cases: 11,
  events: [
    {
      name: "Policy event happened",
      created_ts: "2016-01-28T00:00:00+00:00",
      description: "Description test",
      category: "Policies",
    },
    {
      name: "Case made",
      description: "The publication date",
      created_ts: "2016-01-12T00:00:00+00:00",
      category: "Cases",
    },
    {
      name: "Law passed",
      description: "Imported by CPR loader",
      created_ts: "2016-12-01T00:00:00+00:00",
      category: "Laws",
    },
    {
      name: "Target: Net zero by 2050",
      description: "Imported by CPR loader",
      created_ts: "2017-06-08T00:00:00+00:00",
      category: "Targets",
    },
    {
      name: "End of timeline - no category provided",
      description: "Imported by CPR loader",
      created_ts: "2017-10-08T00:00:00+00:00",
    },
  ],
  targets: [
    {
      target: "80% GHG emission reduction by 2050 compared with a baseline",
      group: "Group label",
      base_year: "2008",
      target_year: "2030",
    },
    {
      target: "Another target",
      group: "Group label",
      base_year: "2020",
      target_year: "2025",
    },
  ],
  documents: [
    {
      country_code: "JPN",
      country_name: "Japan",
      description: "This Act obliges electric utilities to purchase electricity generated from renewable energy sources (solar PV, wind power, hydraulic power, geothermal and biomass) based on a fixed-period contract with a fixed price. Costs incurred by the utility in purchasing renewable energy sourced electricity shall be transferred to all electricity customers, who pay the 'surcharge for renewable energy' in general proportional to electricity usage. Utility companies users that had been severely affected by the 2011 tsunami and earthquakes are exempted.  A committee to calculate purchasing price is established under this law, which consists of 5 members with expertise in electricity business and economy, appointed by the Minister of Economy, Trade and Industry upon approval of both chambers of the Parliament.The Act was amended on June 12, 2020, by the Act on Partial Amendment of the Electricity Business Act and Other Acts for Establishing Resilient and Sustainable Electricity Supply Systems. This document establishes 1) a Feed-in-Premium (FIP) scheme in addition to the existing FIT scheme 2) a system in which part of the expenditures for fortifying electricity grids necessary for expanding the introduction of renewable energy into businesses, e.g., regional interconnection lines, which regional electricity transmission/distribution businesses bear under the current Act, is to be supported based on the surcharge system across Japan, 3) obligations on renewable energy generators to establish an external reserve fund for the expenditures for discarding their facilities for generating renewable energy as a measure for addressing concerns over inappropriate discarding of PV facilities, 4) the obligation to maintain funds for decommissioning purposes, and 5) a modification of the FIT scheme.",
      name: "Cabinet Decision on the Bill for the Act of Partial Revision of the Electricity Business Act and Other Acts for Establishing Resilient and Sustainable Electricity Supply Systems",
      publication_ts: "2020-01-01T00:00:00",
      related_id: 12379,
      category: "Laws"
    }
  ],
};
