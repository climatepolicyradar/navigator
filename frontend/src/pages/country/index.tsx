import { FC } from "React";
import { TCountry, TTarget, TEvent } from "@types";
import Layout from "@components/layouts/Main";
import { SingleCol } from "@components/SingleCol";
import Event from "@components/blocks/Event";
import { Timeline } from "@components/blocks/Timeline";
import { CountryHeader } from "@components/blocks/CountryHeader";
import { KeyDetail } from "@components/KeyDetail";
import { LawIcon, PolicyIcon, CaseIcon, TargetIcon } from "@components/svg/Icons";

type TTargets = {
  targets: TTarget[];
};

const Targets = ({ targets }: TTargets) => {
  return (
    <ul className="ml-4 list-disc list-outside">
      {targets.map((target) => (
        <li className="mb-4" key={target.target}>
          <span className="text-blue-700">{target.target}</span>
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
          <div className="mt-8">
            <h3 className="flex mb-4">
              <span className="mr-2">
                <TargetIcon />
              </span>
              Targets ({country.targets.length})
            </h3>
            <Targets targets={country.targets} />
          </div>
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
      name: "Test event 1",
      created_ts: "2016-01-28T00:00:00+00:00",
      description: "Description test",
      category: "Policies",
    },
    {
      name: "Publication",
      description: "The publication date",
      created_ts: "2016-01-12T00:00:00+00:00",
    },
    {
      name: "Law passed",
      description: "Imported by CPR loader",
      created_ts: "2016-12-01T00:00:00+00:00",
    },
    {
      name: "Target: Net zero by 2050",
      description: "Imported by CPR loader",
      created_ts: "2017-06-08T00:00:00+00:00",
      category: "Targets",
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
};
