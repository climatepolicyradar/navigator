import DropdownMenuItem from "./DropdownMenuItem";
import DropdownMenuWrapper from "./DropdownMenuWrapper";

const AccountMenu = ({ setShowMenu, logout, user }) => {
  return (
    <DropdownMenuWrapper>
      <DropdownMenuItem href="https://climatepolicyradar.org" title="About us" target="_blank" first={true} setShowMenu={setShowMenu} />
      <DropdownMenuItem href="/methodology" title="Methodology" setShowMenu={setShowMenu} />
      {!!user ? (
        <>
          <DropdownMenuItem href="/account" title="My account" setShowMenu={setShowMenu} />
          <DropdownMenuItem onClick={logout} title="Sign out" setShowMenu={setShowMenu} />
        </>
      ) : (
        <DropdownMenuItem href="/auth/sign-in" title="Sign in" setShowMenu={setShowMenu} />
      )}
    </DropdownMenuWrapper>
  );
};
export default AccountMenu;
