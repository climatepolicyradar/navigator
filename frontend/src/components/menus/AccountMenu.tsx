import DropdownMenuItem from './DropdownMenuItem';
import DropdownMenuWrapper from './DropdownMenuWrapper';

const AccountMenu = ({ setShowMenu, logout }) => {
  return (
    <DropdownMenuWrapper setShowMenu={setShowMenu}>
      <DropdownMenuItem first={true} href="/account" title="Account" />
      <DropdownMenuItem onClick={logout} title="Log out" />
    </DropdownMenuWrapper>
  );
};
export default AccountMenu;
