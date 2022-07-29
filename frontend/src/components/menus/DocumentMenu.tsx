import { TDocument } from "@types";
import DropdownMenuItem from "./DropdownMenuItem";
import DropdownMenuWrapper from "./DropdownMenuWrapper";

type TProps = {
  document: TDocument;
  setShowMenu: (show?: boolean) => void;
};

const DocumentMenu = ({ document, setShowMenu }: TProps) => {
  return (
    <>
      {/* TODO: translate titles */}
      {document ? (
        <DropdownMenuWrapper setShowMenu={setShowMenu}>
          <DropdownMenuItem href={`/pdf/${document.document_id}`} title="View PDF in full window" first />
          <DropdownMenuItem href={document.document_url} title="Download PDF" />
          <DropdownMenuItem href={`/document/${document.document_id}`} title="View document details" />
        </DropdownMenuWrapper>
      ) : null}
    </>
  );
};
export default DocumentMenu;
