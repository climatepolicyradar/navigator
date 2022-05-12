import Logo from '../svg/Logo';

interface AuthWrapperProps {
  heading: string;
  children: JSX.Element | string;
  description: string;
}
const AuthWrapper = ({ heading, description, children }) => {
  return (
    <div className="sm:w-96 mx-auto flex flex-col justify-center items-center">
      <div className="text-white flex flex-col items-center w-full">
        <Logo />
        <h2 className="font-medium mt-12 text-white">{heading}</h2>
        <p
          className="text-white mt-3 text-center"
          dangerouslySetInnerHTML={{ __html: description }}
        />
      </div>

      {children}
    </div>
  );
};
export default AuthWrapper;
