import { FC } from "react";
import useNestedLookups from "@hooks/useNestedLookups";
import { getCountryId } from "@helpers/getCountryId";

type TCountryLink = {
  countryCode: string;
};

export const CountryLink: FC<TCountryLink> = ({ countryCode, children }) => {
  const geosQuery = useNestedLookups("geographies", "", 2);
  const { data: { data: { level2: countries = [] } = {} } = {} } = geosQuery;
  const countryId = getCountryId(countryCode, countries);
  if (!countryId) return <>{children}</>;
  return (
    <a className="flex underline text-blue-600" href={`/country/${countryId}`}>
      {children}
    </a>
  );
};
