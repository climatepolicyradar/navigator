import DropdownMenuItem from './DropdownMenuItem';
import DropdownMenuWrapper from './DropdownMenuWrapper';

const DocumentMenu = ({ setShowMenu, setShowPDF, showPDF }) => {
  return (
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
          onClick={() => setShowPDF(true)}
        />
      )}

      <DropdownMenuItem title="View PDF in new tab" />
      <DropdownMenuItem title="Download PDF" />
      <DropdownMenuItem title="View document details" />
    </DropdownMenuWrapper>
  );
};
export default DocumentMenu;
