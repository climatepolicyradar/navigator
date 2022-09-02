import Link from "next/link";
import { truncateString } from "../../helpers";
import { getCategoryIcon } from "@helpers/getCatgeoryIcon";
import { convertDate } from "@utils/timedate";
import { TAssociatedDocument } from "@types";
import { CountryLink } from "@components/CountryLink";

interface RelatedDocumentProps {
  document: TAssociatedDocument;
}

export const RelatedDocument = ({ document }: RelatedDocumentProps) => {
  const { country_code, country_name, document_id, publication_ts, category, description, name } = document;
  const [year] = convertDate(publication_ts);
  return (
    <div className="relative">
      <div className="flex justify-between items-start">
        <h2 className="leading-none flex items-start">
          <Link href={`/document/${document_id}`}>
            <a className="text-left text-blue-500 font-medium text-lg transition duration-300 hover:text-indigo-600 leading-tight underline">{truncateString(name, 80)}</a>
          </Link>
        </h2>
      </div>
      <div className="flex text-sm text-indigo-400 mt-3">
        {category && <div className="mr-3">{getCategoryIcon(category, "20")}</div>}
        <CountryLink countryCode={country_code}>
          <div className={`rounded-sm border border-black flag-icon-background flag-icon-${country_code.toLowerCase()}`} />
          <span className="ml-2">{country_name}</span>
        </CountryLink>
        <span>, {year}</span>
      </div>
      <p className="text-indigo-400 mt-3">{truncateString(description.replace(/(<([^>]+)>)/gi, ""), 250)}</p>
    </div>
  );
};
