import Link from "next/link";
import ToggleDocumentMenu from "../menus/ToggleDocumentMenu";
import TextLink from "../nav/TextLink";

const DocumentSlideout = ({ document, showPDF, setShowPDF, setPassageIndex }) => {

  if (!document) return null;

  const year = document?.document_date.split('/')[2] ?? '';

  return (
    <>
      {document ? (
        <>
          <div className="border-b border-blue-200 pb-4 flex justify-between relative">
            <div className="pl-6 pr-10 mt-2">
              <Link href={`/document/${document.document_id}`}>
                <a>
                  <h1 className="text-lg text-blue-500 font-medium">{document.document_name}</h1>
                </a>
              </Link>
              <div className="flex flex-wrap lg:flex-nowrap text-sm text-indigo-400 my-2 items-center">
                <div className={`rounded-sm border border-black flag-icon-background flag-icon-${document.document_country_code.toLowerCase()}`} />
                <span className="ml-2">
                  {document.document_country_english_shortname}, {year}
                </span>
              </div>

              {/* TODO: translate below text, how to handle plurals? */}
              <h3 className="text-indigo-500 text-xl">
                Document {`match${document.document_passage_matches.length === 1 ? "" : "es"}`} ({document.document_passage_matches.length})
              </h3>
            </div>
            <ToggleDocumentMenu setShowPDF={setShowPDF} showPDF={showPDF} document={document} setPassageIndex={setPassageIndex} />
          </div>
          {showPDF && (
            // TODO: translate below text
            <TextLink onClick={() => setShowPDF(false)}>
              <span className="text-lg">&laquo;</span>Back to passage matches
            </TextLink>
          )}
        </>
      ) : null}
    </>
  );
};
export default DocumentSlideout;
