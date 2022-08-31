import { FC } from "react";
import Link from "next/link";
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
    <Link href={`/geography/${countryId}`}>
      <a className="flex underline text-blue-600">{children}</a>
    </Link>
  );
};
