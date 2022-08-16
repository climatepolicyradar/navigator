import { TCountryGeoStats, TGeography } from "@types";
import useNestedLookups from "@hooks/useNestedLookups";
import Tooltip from "@components/tooltip";

type TProps = {
  country: TCountryGeoStats;
};

export const CountryHeader = ({ country }: TProps) => {
  const geosQuery = useNestedLookups("geographies", "", 2);
  const { data: { data: { level1: regions = [], level2: countries = [] } = {} } = {} } = geosQuery;

  const getCountryRegion = (countryName: string) => {
    const country = countries.find((c: TGeography) => c.display_value === countryName);
    if (!country) return "";
    const region = regions.find((r: TGeography) => r.id === country.parent_id);
    return region.display_value ?? "";
  };

  const { name, political_groups, federal, federal_details, worldbank_income_group, climate_risk_index, global_emissions_percent } = country;

  return (
    <div className="bg-offwhite border-solid border-blue-200 border-b py-6">
      <div className="container flex items-end justify-between overflow-hidden">
        <div className="md:max-w-lg flex-shrink-0">
          <h1>{name}</h1>
          <div className="grid grid-cols-2 gap-6 items-center">
            <div className="font-semibold text-blue-700 text-xl">{getCountryRegion(name)}</div>
            <div className="font-semibold text-blue-700 text-xl">
              {federal ? "Federative" : "Unitary"} {federal_details && <span className="font-light text-lg">({federal_details})</span>}
            </div>
            <div>
              <div className="text-blue-700 text-lg">Political groups</div>
              <div className="font-semibold text-blue-700 text-xl">{political_groups.split(";").join(", ")}</div>
            </div>
            <div className="font-semibold text-blue-700 text-xl">{worldbank_income_group}</div>
            <div>
              <div className="text-blue-700 text-lg">Global Climate Risk Index</div>
              <div className="font-semibold text-blue-700 text-xl flex">
                <div className="mr-1">{climate_risk_index}</div> <Tooltip id="country-gcri" tooltip="Global Climate Risk Index" icon="i" />
              </div>
            </div>
            <div>
              <div className="text-blue-700 text-lg">% Global Emissions</div>
              <div className="font-semibold text-blue-700 text-xl">{global_emissions_percent}%</div>
            </div>
          </div>
        </div>
        <div className="hidden place-items-center md:flex overflow-hidden">{/* <img src={`/images/countries/${country.short_name}.png`} alt={country.name} /> */}</div>
      </div>
    </div>
  );
};
