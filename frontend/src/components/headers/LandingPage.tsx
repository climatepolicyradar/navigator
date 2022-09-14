import ToggleAccountMenu from "../menus/ToggleAccountMenu";

const LandingPageHeader = () => {
  return (
    <header data-cy="header" className={`absolute bg-transparent w-full top-0 left-0 transition duration-300 z-30`}>
      <div className="container my-4">
        <div className="flex items-start justify-end">
          <div>
            <ToggleAccountMenu />
          </div>
        </div>
      </div>
    </header>
  );
};
export default LandingPageHeader;
