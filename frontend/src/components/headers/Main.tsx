import { useAuth } from "@api/auth";
import ToggleAccountMenu from "../menus/ToggleAccountMenu";
import AlphaLogoSmall from "../logo/AlphaLogoSmall";

const Header = () => {
  const { user, logout } = useAuth();

  return (
    <header data-cy="header" className="absolute bg-transparent w-full top-0 left-0 transition duration-300 z-10">
      <div className="container my-4">
        <div className="flex items-center justify-between">
          <AlphaLogoSmall />

          <div>
            <ToggleAccountMenu logout={logout} user={user} />
          </div>
        </div>
      </div>
    </header>
  );
};
export default Header;
