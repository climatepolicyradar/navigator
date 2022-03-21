import Logo from '../Logo';

interface AuthWrapperProps {
  heading: string;
  children: JSX.Element | string;
  description: string;
}
const AuthWrapper = ({ heading, description, children }) => {
  return (
    <div className="sm:w-96 mx-auto flex flex-col justify-center items-center absolute inset-0 z-10">
      <div className="text-white flex flex-col items-center">
        <Logo />
        <h2 className="font-medium mt-12 text-white">{heading}</h2>
        <p className="text-white mt-3">{description}</p>
      </div>

      {children}
    </div>
  );
};
export default AuthWrapper;
