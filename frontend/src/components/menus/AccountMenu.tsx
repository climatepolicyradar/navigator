import DropdownMenuItem from './DropdownMenuItem';
import DropdownMenuWrapper from './DropdownMenuWrapper';

const AccountMenu = ({ setShowMenu, logout }) => {
  return (
    <DropdownMenuWrapper setShowMenu={setShowMenu}>
      <DropdownMenuItem
        href="https://climatepolicyradar.org"
        title="About us"
        target="_blank"
        first={true}
      />
      <DropdownMenuItem href="/methodology" title="Methodology" />
      <DropdownMenuItem href="/account" title="My account" />

      <DropdownMenuItem onClick={logout} title="Sign out" />
    </DropdownMenuWrapper>
  );
};
export default AccountMenu;
