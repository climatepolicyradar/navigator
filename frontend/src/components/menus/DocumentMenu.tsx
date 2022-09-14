import { TDocument } from "@types";
import DropdownMenuItem from "./DropdownMenuItem";
import DropdownMenuWrapper from "./DropdownMenuWrapper";

type TProps = {
  document: TDocument;
  setShowMenu: (show?: boolean) => void;
};

const DocumentMenu = ({ document, setShowMenu }: TProps) => {
  if (!document) return null;
  
  return (
    <DropdownMenuWrapper>
      <DropdownMenuItem href={`/pdf/${document.document_id}`} title="View PDF in full window" first setShowMenu={setShowMenu} />
      <DropdownMenuItem href={document.document_url} title="Download PDF" setShowMenu={setShowMenu} />
      <DropdownMenuItem href={`/document/${document.document_id}`} title="View document details" setShowMenu={setShowMenu} />
    </DropdownMenuWrapper>
  );
};

export default DocumentMenu;
