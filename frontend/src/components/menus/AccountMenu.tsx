import DropdownMenuItem from "./DropdownMenuItem";
import DropdownMenuWrapper from "./DropdownMenuWrapper";

const AccountMenu = ({ setShowMenu }) => {
  return (
    <DropdownMenuWrapper>
      <DropdownMenuItem href="https://climatepolicyradar.org" title="About us" target="_blank" first={true} setShowMenu={setShowMenu} />
      <DropdownMenuItem href="/methodology" title="Methodology" setShowMenu={setShowMenu} />
    </DropdownMenuWrapper>
  );
};
export default AccountMenu;
