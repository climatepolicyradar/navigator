import DropdownMenuItem from "./DropdownMenuItem";
import DropdownMenuWrapper from "./DropdownMenuWrapper";

const DocumentMenu = ({ document, setShowMenu }) => {
  return (
    <>
      {/* TODO: translate titles */}
      {document ? (
        <DropdownMenuWrapper setShowMenu={setShowMenu}>
          <DropdownMenuItem href={`/pdf/${document.document_id}`} title="View PDF in full window" />
          <DropdownMenuItem href={document.document_url} title="Download PDF" />
          <DropdownMenuItem href={`/document/${document.document_id}`} title="View document details" />
        </DropdownMenuWrapper>
      ) : null}
    </>
  );
};
export default DocumentMenu;
