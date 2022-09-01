import { FC } from "react";
import Link from "next/link";
import useConfig from "@hooks/useConfig";
import { getCountryId } from "@helpers/getCountryId";

type TCountryLink = {
  countryCode: string;
};

export const CountryLink: FC<TCountryLink> = ({ countryCode, children }) => {
  const configQuery: any = useConfig("config");
  const { data: { countries = [] } = {} } = configQuery;

  const countryId = getCountryId(countryCode, countries);
  if (!countryId) return <>{children}</>;
  return (
    <Link href={`/geography/${countryId}`}>
      <a className="flex underline text-blue-600">{children}</a>
    </Link>
  );
};
