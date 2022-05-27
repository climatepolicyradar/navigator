import DropdownMenuItem from './DropdownMenuItem';
import DropdownMenuWrapper from './DropdownMenuWrapper';

const DocumentMenu = ({
  document,
  setShowMenu,
  setShowPDF,
  showPDF,
  setPassageIndex,
}) => {
  return (
    <>
      {/* TODO: translate titles */}
      {document ? (
        <DropdownMenuWrapper setShowMenu={setShowMenu}>
          {showPDF ? (
            <DropdownMenuItem
              first={true}
              title="View passage matches"
              onClick={() => setShowPDF(false)}
            />
          ) : (
            <DropdownMenuItem
              first={true}
              title="View PDF"
              onClick={() => {
                setPassageIndex(null);
                setShowPDF(true);
              }}
            />
          )}
          <DropdownMenuItem
            href={`/pdf/${document.document_id}`}
            title="View PDF in full window"
          />
          <DropdownMenuItem href={document.document_url} title="Download PDF" />
          <DropdownMenuItem
            href={`/document/${document.document_id}`}
            title="View document details"
          />
        </DropdownMenuWrapper>
      ) : null}
    </>
  );
};
export default DocumentMenu;
