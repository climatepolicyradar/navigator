import ToggleAccountMenu from '../menus/ToggleAccountMenu';
import { useAuth } from '../../api/auth';

const LandingPageHeader = () => {
  const { logout } = useAuth();
  return (
    <header
      data-cy="header"
      className={`absolute bg-transparent w-full top-0 left-0 transition duration-300 z-30`}
    >
      <div className="container my-4">
        <div className="flex items-start justify-end">
          <div>
            <ToggleAccountMenu logout={logout} />
          </div>
        </div>
      </div>
    </header>
  );
};
export default LandingPageHeader;
