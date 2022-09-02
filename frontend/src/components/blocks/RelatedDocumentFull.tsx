import Link from "next/link";
import { truncateString } from "../../helpers";
import { convertDate } from "@utils/timedate";
import { getCategoryIcon } from "@helpers/getCatgeoryIcon";
import { TDocument } from "@types";
import { CountryLink } from "@components/CountryLink";

type TProps = {
  document: TDocument;
};

export const RelatedDocumentFull = ({ document }: TProps) => {
  const { document_country_code, document_country_english_shortname, document_id, document_date, document_description, document_name, document_category } = document;
  const [year] = convertDate(document_date);
  return (
    <div className="relative">
      <div className="flex justify-between items-start">
        <h2 className="leading-none flex items-start">
          <Link href={`/document/${document_id}`}>
            <a className="text-left text-blue-500 font-medium text-lg transition duration-300 hover:text-indigo-600 leading-tight underline">{truncateString(document_name, 80)}</a>
          </Link>
        </h2>
      </div>
      <div className="flex text-sm text-indigo-400 mt-3">
        {document_category && <div className="mr-3" title={document_category}>{getCategoryIcon(document_category, "20")}</div>}
        <CountryLink countryCode={document_country_code}>
          <div className={`rounded-sm border border-black flag-icon-background flag-icon-${document_country_code.toLowerCase()}`} />
          <span className="ml-2">{document_country_english_shortname}</span>
        </CountryLink>
        <span>, {year}</span>
      </div>
      <p className="text-indigo-400 mt-3">{truncateString(document_description.replace(/(<([^>]+)>)/gi, ""), 250)}</p>
    </div>
  );
};
