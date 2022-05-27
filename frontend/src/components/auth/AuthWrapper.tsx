import Link from 'next/link';
import Logo from '../svg/Logo';

interface AuthWrapperProps {
  heading: string;
  children?: React.ReactNode | string;
  description: string;
}
const AuthWrapper = ({
  heading,
  description,
  children = '',
}: AuthWrapperProps) => {
  return (
    <div className="sm:w-96 mx-auto flex flex-col justify-center items-center">
      <div className="text-white flex flex-col items-center w-full">
        <a href="https://climatepolicyradar.org">
          <Logo />
        </a>

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
