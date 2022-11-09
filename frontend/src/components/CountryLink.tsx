import { FC } from "react";
import Link from "next/link";
import useConfig from "@hooks/useConfig";
import { getCountrySlug } from "@helpers/getCountryFields";

type TCountryLink = {
  countryCode: string;
  className?: string;
};

export const CountryLink: FC<TCountryLink> = ({ countryCode, className = "", children }) => {
  const configQuery: any = useConfig("config");
  const { data: { countries = [] } = {} } = configQuery;

  const slug = getCountrySlug(countryCode, countries);
  if (!slug) return <>{children}</>;
  return (
    <Link href={`/geographies/${slug}`}>
      <a className={`flex items-center underline ${className}`}>{children}</a>
    </Link>
  );
};
