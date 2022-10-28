import { FC } from "react";
import Link from "next/link";
import { TEventCategory } from "@types";
import { truncateString } from "@helpers/index";
import { getCategoryIcon } from "@helpers/getCatgeoryIcon";
import { CountryLink } from "@components/CountryLink";
// import getSite from "@utils/getSite";
import { useContext } from "react";
import { ThemeContext } from "@context/ThemeContext";

type TProps = {
  listItem: {
    id: number;
    country_code: string;
    country_name: string;
    description: string;
    name: string;
    document_year: string;
    category?: TEventCategory;
  };
};

export const DocumentListItem: FC<TProps> = ({ children, listItem }) => {
  const { id, country_code, country_name, description, name, document_year, category } = listItem;
  // const site = getSite();
  const theme = useContext(ThemeContext);

  return (
    <div className="relative">
      <div className="flex justify-between items-start">
        <h2 className="leading-none flex items-start">
          <Link href={`/document/${id}`}>
            <a className={`text-left text-blue-500 font-medium text-lg transition duration-300 leading-tight hover:underline ${theme === "cpr" ? "underline" : ""}`}>{name}</a>
          </Link>
        </h2>
      </div>
      <div className="flex flex-wrap text-sm text-indigo-400 mt-4 items-center font-medium">
        {category && (
          <div className="mr-3" title={category}>
            {getCategoryIcon(category, "20")}
          </div>
        )}
        <CountryLink countryCode={country_code}>
          <div className={`rounded-sm border border-black flag-icon-background flag-icon-${country_code.toLowerCase()}`} />
          <span className="ml-2">{country_name}</span>
        </CountryLink>
        <span>, {document_year}</span>
        {children}
      </div>
      <p className="text-indigo-400 mt-3 text-content">{truncateString(description.replace(/(<([^>]+)>)/gi, ""), 375)}</p>
    </div>
  );
};
