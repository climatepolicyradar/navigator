import DropdownMenuItem from './DropdownMenuItem';
import DropdownMenuWrapper from './DropdownMenuWrapper';

const DocumentMenu = ({ setShowMenu }) => {
  return (
    <DropdownMenuWrapper setShowMenu={setShowMenu}>
      <DropdownMenuItem first={true} title="View PDF" />
      <DropdownMenuItem title="View PDF in new tab" />
      <DropdownMenuItem title="Download PDF" />
      <DropdownMenuItem title="View document details" />
    </DropdownMenuWrapper>
  );
};
export default DocumentMenu;
