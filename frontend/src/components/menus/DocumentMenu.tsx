import { useState, useRef } from "react";
import { TDocument } from "@types";
import useOutsideAlerter from "@hooks/useOutsideAlerter";
import Kebab from "../buttons/Kebab";
import DropdownMenuItem from "./DropdownMenuItem";
import DropdownMenuWrapper from "./DropdownMenuWrapper";

type TProps = {
  document: TDocument;
};

const ToggleDocumentMenu = ({ document }: TProps) => {
  const [showMenu, setShowMenu] = useState(false);
  const menuRef = useRef(null);
  useOutsideAlerter(menuRef, () => setShowMenu(false));

  const toggleMenu = (e) => {
    e.preventDefault();
    setShowMenu(!showMenu);
  };

  return (
    <div ref={menuRef} className="flex-shrink-0 mr-4">
      <Kebab onClick={toggleMenu} />
      <div className={`${!showMenu ? "hidden" : ""} absolute top-0 right-0 mt-12 mr-4 z-50`}>
        <DropdownMenuWrapper>
          <DropdownMenuItem href={`/pdf/${document.document_id}`} title="View PDF in full window" first setShowMenu={setShowMenu} />
          <DropdownMenuItem href={document.document_url} title="Download PDF" setShowMenu={setShowMenu} />
          <DropdownMenuItem href={`/document/${document.document_id}`} title="View document details" setShowMenu={setShowMenu} />
        </DropdownMenuWrapper>
      </div>
    </div>
  );
};
export default ToggleDocumentMenu;
