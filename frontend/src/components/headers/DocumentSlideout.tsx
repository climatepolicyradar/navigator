import ToggleDocumentMenu from '../menus/ToggleDocumentMenu';

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
              <h1 className="text-lg text-blue-500 font-medium">
                {document.document_name}
              </h1>
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
            <button
              className="ml-6 text-blue-500 underline text-sm text-left mt-2 hover:text-indigo-600 transition duration-300"
              onClick={() => {
                setShowPDF(false);
              }}
            >
              &laquo; Back
            </button>
          )}
        </>
      ) : null}
    </>
  );
};
export default DocumentSlideout;
