import { FC } from "React";
import { TCountry, TTarget } from "@types";
import Layout from "@components/layouts/Main";
import Tooltip from "@components/tooltip";
import { LawIcon, PolicyIcon, CaseIcon, TargetIcon } from "@components/svg/Icons";

const SingleColumn: FC = ({ children }) => {
  return <div className="mt-8 mx-auto max-w-screen-lg">{children}</div>;
};

type TKeyDetail = {
  detail: string;
  amount: number;
  icon?: JSX.Element;
};

const KeyDetail = ({ detail, amount, icon }: TKeyDetail) => {
  return (
    <div className="bg-blue-600 text-white flex h-[90px] items-center justify-center">
      {icon && (
        <div>
          <div className="p-1 bg-white text-blue-600 rounded-full w-[54px] h-[54px] flex items-center justify-center">{icon}</div>
        </div>
      )}
      <div className="text-lg ml-2">{detail}</div>
      <div className="ml-3 text-2xl font-bold drop-shadow-sm">{amount}</div>
    </div>
  );
};

type TTargets = {
  targets: TTarget[];
};

const Targets = ({ targets }: TTargets) => {
  return (
    <ul className="ml-4 list-disc list-outside">
      {targets.map((target) => (
        <li className="mb-4">
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

type TCountryHeader = {
  country: TCountry;
};

const CountryHeader = ({ country }: TCountryHeader) => {
  const { short_name, continent, legal_structure, legal_bodies, political_groups, financial_status, gcri, emissions } = country;

  return (
    <div className="bg-offwhite border-solid border-blue-200 border-b py-6">
      <div className="container">
        <div className="md:max-w-lg">
          <h1>{short_name}</h1>
          <div className="grid grid-cols-2 gap-2 items-center">
            <div className="font-semibold text-blue-700 text-xl">{continent}</div>
            <div className="font-semibold text-blue-700 text-xl">
              {legal_structure} ({legal_bodies})
            </div>
            <div>
              <div className="text-blue-700 text-lg">Political groups</div>
              <div className="font-semibold text-blue-700 text-xl">{political_groups.join(", ")}</div>
            </div>
            <div className="font-semibold text-blue-700 text-xl">{financial_status}</div>
            <div>
              <div className="text-blue-700 text-lg">Global Climate Risk Index</div>
              <div className="font-semibold text-blue-700 text-xl flex">
                <div className="mr-1">{gcri}</div> <Tooltip id="country-gcri" tooltip="Global Climate Risk Index" />
              </div>
            </div>
            <div>
              <div className="text-blue-700 text-lg">% Global Emissions</div>
              <div className="font-semibold text-blue-700 text-xl">{emissions}%</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const CountryPage = () => {
  const country = COUNTRY;
  return (
    <Layout title={`Climate Policy Radar | ${country.name}`}>
      <section className="mb-8">
        <CountryHeader country={country} />
        <SingleColumn>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-px rounded">
            <KeyDetail detail="Laws" amount={country.laws} icon={<LawIcon />} />
            <KeyDetail detail="Policies" amount={country.policies} icon={<PolicyIcon />} />
            <KeyDetail detail="Cases" amount={country.cases} icon={<CaseIcon />} />
          </div>
          <div className="mt-8">
            <h3 className="flex mb-4">
              <span className="mr-2">
                <TargetIcon />
              </span>
              Targets ({country.targets.length})
            </h3>
            <Targets targets={country.targets} />
          </div>
        </SingleColumn>
      </section>
    </Layout>
  );
};

export default CountryPage;

const COUNTRY: TCountry = {
  name: "United States of American",
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
  events: [],
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
