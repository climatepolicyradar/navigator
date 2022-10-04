import { FC } from "react";
import Link from "next/link";
import useConfig from "@hooks/useConfig";
import { getCountryId } from "@helpers/getCountryId";

type TCountryLink = {
  countryCode: string;
  className?: string;
};

export const CountryLink: FC<TCountryLink> = ({ countryCode, className, children }) => {
  const configQuery: any = useConfig("config");
  const { data: { countries = [] } = {} } = configQuery;

  const countryId = getCountryId(countryCode, countries);
  if (!countryId) return <>{children}</>;
  return (
    <Link href={`/geographies/${countryId}`}>
      <a className={`flex items-center underline ${className}`}>{children}</a>
    </Link>
  );
};
