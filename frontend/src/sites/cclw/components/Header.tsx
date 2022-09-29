import { ExternalLink } from "@components/ExternalLink";
import Logo from "@components/svg/Logo";
import Image from "next/image";
import Link from "next/link";

// TODO: import config for menu items

const Header = () => {
  return (
    <header data-cy="header" className="bg-indigo-400 w-full border-b-2 border-grey-200">
      <div className="container">
        <div className="flex justify-between">
          <div className="my-6 mr-6">
            <Link href={`/`}>
              <a className="flex text-blue-400">
                <Image src="/cclw/CCLW_logo.jpg" alt="Climate Change Laws of the World logo" width={200} height={100} layout={"fixed"} priority />
              </a>
            </Link>
          </div>
          <div className="flex-1 flex flex-col mt-6 text-blue-400">
            <div className="font-bold md:text-xl lg:text-3xl">
              <Link href={`/`}>
                <a className="">Climate Change Laws of the World</a>
              </Link>
            </div>
            <nav className="mt-8 flex-1 text-white hidden md:block">
              <ul className="flex items-end gap-8 h-full text-sm lg:text-base">
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
          <div className="text-white items-end mb-6 hidden xl:flex">
            <div>
              <p>A project of... </p>
              <div className="flex gap-4">
                {/* Logos */}
                <ExternalLink className="flex" url="https://www.lse.ac.uk/">
                  <Image src="/images/partners/lse-logo.png" alt="LSE logo" width={60} height={60} layout={"fixed"} />
                </ExternalLink>
                <ExternalLink className="flex" url="https://www.lse.ac.uk/granthaminstitute/">
                  <Image src="/images/partners/grantham-logo.png" alt="GRI logo" width={232} height={60} layout={"fixed"} />
                </ExternalLink>
                <ExternalLink className="flex" url="https://www.climatepolicyradar.org">
                  <Logo />
                </ExternalLink>
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
