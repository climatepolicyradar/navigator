import MainMenu from "../menus/MainMenu";
import AlphaLogoSmall from "../logo/AlphaLogoSmall";

const Header = () => {
  return (
    <header data-cy="header" className="absolute bg-transparent w-full top-0 left-0 transition duration-300">
      <div className="container my-4">
        <div className="flex items-center justify-between">
          <AlphaLogoSmall />
          <div>
            <MainMenu />
          </div>
        </div>
      </div>
    </header>
  );
};
export default Header;
