import Image from "next/image";
import Link from "next/link";

// TODO: import config for menu items

const Header = () => {
  return (
    <header data-cy="header" className="bg-indigo-400 w-full border-b-2 border-lightgray">
      <div className="container">
        <div className="flex justify-between">
          <div className="my-6 mr-6">
            <Link href={`/`}>
              <a className="flex text-blue-400">
                <Image src="/cclw/CCLW_logo.jpg" alt="Climate Change Laws of the World logo" width={200} height={100} layout={"fixed"} />
              </a>
            </Link>
          </div>
          <div className="flex-1 flex flex-col mt-6 text-blue-400">
            <div className="font-bold text-3xl">
              <Link href={`/`}>
                <a className="">Climate Change Laws of the World</a>
              </Link>
            </div>
            <nav className="mt-8 flex-1 text-white">
              <ul className="flex items-end h-full">
                <li>
                  <Link href="/">
                    <a>Home</a>
                  </Link>
                </li>
                <li>
                  <Link href="/">
                    <a>About</a>
                  </Link>
                </li>
                <li>
                  <Link href="/">
                    <a className="active">Methodology</a>
                  </Link>
                </li>
                <li>
                  <Link href="/">
                    <a>Acknowledgements</a>
                  </Link>
                </li>
              </ul>
            </nav>
          </div>
          <div className="text-white">
            <p>A project of... </p>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
