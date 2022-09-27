import Image from "next/image";
import Link from "next/link";

// TODO: import config for menu items

const Header = () => {
  return (
    <header data-cy="header" className="bg-indigo-400 w-full">
      <div className="container">
        <div className="flex justify-between">
          <div className="my-6 mr-6">
            <Link href={`/`}>
              <a className="flex text-blue-400">
                <Image src="/cclw/CCLW_logo.jpg" alt="Climate Change Laws of the World logo" width={200} height={100} layout={"fixed"} />
              </a>
            </Link>
          </div>
          <div className="flex-1 flex flex-col text-white mt-6">
            {/* Title and nav */}
            <div className="font-bold text-3xl">
              <Link href={`/`}>
                <a className="">Climate Change Laws of the World</a>
              </Link>
            </div>
            <nav className="mt-5 flex-1">
              <ul className="flex h-full">
                <li className="mr-8">
                  <Link href="/">
                    <a className="h-full block">Home</a>
                  </Link>
                </li>
                <li className="mr-8">
                  <Link href="/">
                    <a className="h-full block">About</a>
                  </Link>
                </li>
                <li className="mr-8 border-b-4 border-blue-400 text-blue-400">
                  <Link href="/">
                    <a className="h-full block">Methodology</a>
                  </Link>
                </li>
                <li className="mr-8">
                  <Link href="/">
                    <a className="h-full block">Acknowledgements</a>
                  </Link>
                </li>
              </ul>
            </nav>
          </div>
          <div>{/* Partners */}</div>
        </div>
      </div>
    </header>
  );
};

export default Header;
