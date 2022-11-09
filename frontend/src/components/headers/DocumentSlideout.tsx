import Link from "next/link";
import { TDocument } from "@types";
import DocumentMenu from "../menus/DocumentMenu";
import TextLink from "../nav/TextLink";
import { getDocumentTitle } from "@helpers/getDocumentTitle";

type TProps = {
  document: TDocument;
  searchTerm: string;
  showPDF: boolean;
  setShowPDF: (show?: boolean) => void;
};

const DocumentSlideout = ({ document, searchTerm, showPDF, setShowPDF }: TProps) => {
  if (!document) return null;

  const year = document?.document_date.split("/")[2] ?? "";

  return (
    <>
      {document ? (
        <>
          <div className="border-b border-lineBorder pb-4 flex justify-between relative">
            <div className="pl-6 pr-10 mt-2">
              <Link href={`/document/${document.document_slug}`}>
                <a>
                  <h1 className="text-lg text-blue-500 font-medium">{getDocumentTitle(document.document_name, document.document_postfix)}</h1>
                </a>
              </Link>
              <div className="flex flex-wrap lg:flex-nowrap text-sm text-indigo-400 my-2 items-center">
                <div className={`rounded-sm border border-black flag-icon-background flag-icon-${document.document_geography.toLowerCase()}`} />
                <span className="ml-2">
                  {document.document_country_english_shortname}, {year}
                </span>
              </div>

              {/* TODO: translate below text, how to handle plurals? */}
              <h3 className="text-indigo-500 text-xl">
                Document {`match${document.document_passage_matches.length === 1 ? "" : "es"}`} ({document.document_passage_matches.length}) for "{searchTerm}"
              </h3>
            </div>
            <DocumentMenu document={document} />
          </div>
          {showPDF && (
            // TODO: translate below text
            <div className="md:hidden ml-6">
              <TextLink onClick={() => setShowPDF(false)}>
                <span className="text-lg">&laquo;</span>Back to passage matches
              </TextLink>
            </div>
          )}
        </>
      ) : null}
    </>
  );
};
export default DocumentSlideout;
