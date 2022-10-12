import { useRouter } from "next/router";
import Link from "next/link";
import Image from "next/image";
import { ExternalLink } from "@components/ExternalLink";
import Logo from "@components/svg/Logo";
import { SearchIcon } from "@components/svg/Icons";
import { useEffect, useState } from "react";

// TODO: import config for menu items

const Header = () => {
  const { pathname } = useRouter();
  const [activePage, setActivePage] = useState("");

  useEffect(() => {
    setActivePage(pathname);
  }, [pathname]);

  const linkClass = (pageUrl: string) => {
    return activePage.toLowerCase() === pageUrl ? "active" : "";
  };

  return (
    <header data-cy="header" className="bg-secondary-700 w-full border-b-2 border-overlayWhite">
      <div className="container">
        <div className="flex justify-between">
          <div className="flex-1 flex flex-col mt-6 text-blue-400">
            <div className="font-bold md:text-xl lg:text-3xl">
              <Link href={`/`}>
                <a className="">Climate Change Laws of the World</a>
              </Link>
            </div>
            <nav className="mt-8 flex-1 text-white hidden md:block">
              <ul className="flex items-end gap-8 h-full text-sm lg:text-base font-bold">
                <li>
                  <Link href="/">
                    <a className={linkClass("/")}>Home</a>
                  </Link>
                </li>
                <li>
                  <Link href="/about">
                    <a className={linkClass("/about")}>About</a>
                  </Link>
                </li>
                <li>
                  <Link href="/methodology">
                    <a className={linkClass("/methodology")}>Methodology</a>
                  </Link>
                </li>
                <li>
                  <Link href="/acknowledgements">
                    <a className={linkClass("/acknowledgements")}>Acknowledgements</a>
                  </Link>
                </li>
                <li>
                  <Link href="/search">
                    <a className={linkClass("/search") + " flex gap-2"}>
                      Search{" "}
                      <span className="mt-[-2px]">
                        <SearchIcon height="24" width="24" />
                      </span>
                    </a>
                  </Link>
                </li>
              </ul>
            </nav>
          </div>
          <div className="text-white items-end mb-6 hidden xl:flex text-sm">
            <div>
              <p>A project of... </p>
              <div className="flex xflex-col gap-4 mt-2">
                {/* <div className="flex gap-4"> */}
                <ExternalLink className="flex" url="https://www.lse.ac.uk/">
                  <Image src="/images/partners/lse-logo.png" alt="LSE logo" width={40} height={40} layout={"fixed"} />
                </ExternalLink>
                <ExternalLink className="flex" url="https://www.lse.ac.uk/granthaminstitute/">
                  <Image src="/cclw/partners/gri_white_logo.svg" alt="GRI logo" width={180} height={40} layout={"fixed"} />
                </ExternalLink>
                {/* </div> */}
                {/* <div> */}
                <ExternalLink className="flex" url="https://www.climatepolicyradar.org">
                  <Logo fixed />
                </ExternalLink>
                {/* </div> */}
              </div>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
