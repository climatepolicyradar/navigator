import DropdownMenuItem from './DropdownMenuItem';
import DropdownMenuWrapper from './DropdownMenuWrapper';

const AccountMenu = ({ setShowMenu, logout }) => {
  return (
    <DropdownMenuWrapper setShowMenu={setShowMenu}>
      <DropdownMenuItem first={true} href="/account" title="My account" />
      <DropdownMenuItem
        href="https://climatepolicyradar.org"
        title="About us"
      />
      <DropdownMenuItem onClick={logout} title="Sign out" />
    </DropdownMenuWrapper>
  );
};
export default AccountMenu;
