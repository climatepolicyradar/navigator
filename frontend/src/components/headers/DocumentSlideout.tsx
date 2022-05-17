import Link from 'next/link';
import ToggleDocumentMenu from '../menus/ToggleDocumentMenu';
import TextLink from '../nav/TextLink';

const DocumentSlideout = ({
  document,
  showPDF,
  setShowPDF,
  setPassageIndex,
}) => {
  return (
    <>
      {document ? (
        <>
          <div className="border-b border-blue-200 pb-4 flex justify-between relative">
            <div className="pl-6 pr-10 mt-2">
              <Link href={`/document/${document.document_id}`}>
                <a>
                  <h1 className="text-lg text-blue-500 font-medium">
                    {document.document_name}
                  </h1>
                </a>
              </Link>

              {/* TODO: translate below text, how to handle plurals? */}
              <p className="text-indigo-500 text-sm">
                {document.document_passage_matches.length}{' '}
                {`match${
                  document.document_passage_matches.length === 1 ? '' : 'es'
                }`}{' '}
                in document.
              </p>
            </div>
            <ToggleDocumentMenu
              setShowPDF={setShowPDF}
              showPDF={showPDF}
              document={document}
              setPassageIndex={setPassageIndex}
            />
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
