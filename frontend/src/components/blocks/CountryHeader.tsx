import { TCountry } from "@types";
import Tooltip from "@components/tooltip";

type TProps = {
  country: TCountry;
};

export const CountryHeader = ({ country }: TProps) => {
  const { short_name, continent, legal_structure, legal_bodies, political_groups, financial_status, gcri, emissions } = country;

  return (
    <div className="bg-offwhite border-solid border-blue-200 border-b py-6">
      <div className="container flex items-end justify-between overflow-hidden">
        <div className="md:max-w-lg flex-shrink-0">
          <h1>{short_name}</h1>
          <div className="grid grid-cols-2 gap-2 items-center">
            <div className="font-semibold text-blue-700 text-xl">{continent}</div>
            <div className="font-semibold text-blue-700 text-xl">
              {legal_structure} <span className="font-light text-lg">({legal_bodies})</span>
            </div>
            <div>
              <div className="text-blue-700 text-lg">Political groups</div>
              <div className="font-semibold text-blue-700 text-xl">{political_groups.join(", ")}</div>
            </div>
            <div className="font-semibold text-blue-700 text-xl">{financial_status}</div>
            <div>
              <div className="text-blue-700 text-lg">Global Climate Risk Index</div>
              <div className="font-semibold text-blue-700 text-xl flex">
                <div className="mr-1">{gcri}</div> <Tooltip id="country-gcri" tooltip="Global Climate Risk Index" icon="i" />
              </div>
            </div>
            <div>
              <div className="text-blue-700 text-lg">% Global Emissions</div>
              <div className="font-semibold text-blue-700 text-xl">{emissions}%</div>
            </div>
          </div>
        </div>
        <div className="hidden place-items-center md:flex overflow-hidden">
          <img src={`/images/countries/${country.short_name}.png`} alt={country.name} />
        </div>
      </div>
    </div>
  );
};
