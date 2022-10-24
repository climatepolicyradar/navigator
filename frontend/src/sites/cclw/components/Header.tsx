import { useRouter } from "next/router";
import Link from "next/link";
import Image from "next/image";
import { ExternalLink } from "@components/ExternalLink";
import Logo from "@components/svg/LogoMono";
import { SearchIcon } from "@components/svg/Icons";
import { useEffect, useState } from "react";

type TProps = {
  background?: boolean;
};

const Header = ({ background = true }) => {
  const { pathname } = useRouter();
  const [activePage, setActivePage] = useState("");

  useEffect(() => {
    setActivePage(pathname);
  }, [pathname]);

  const linkClass = (pageUrl: string) => {
    return activePage.toLowerCase() === pageUrl ? "active" : "";
  };

  return (
    <header data-cy="header" className={`${background ? "bg-secondary-700" : ""} w-full border-b-2 border-overlayWhite pt-6 lg:pt-0`}>
      <div className="container">
        <div className="flex flex-wrap lg:flex-nowrap justify-between">
          <div className="items-end flex flex-grow-0 xbasis-1/3 lg:basis-1/4">
            <ExternalLink className="flex" url="https://www.lse.ac.uk/">
              <Image src="/images/partners/lse-logo.png" alt="LSE logo" width={40} height={40} layout={"fixed"} />
            </ExternalLink>
            <ExternalLink className="flex" url="https://www.lse.ac.uk/granthaminstitute/">
              <Image src="/cclw/partners/gri_white_logo.svg" alt="GRI logo" width={180} height={40} layout={"fixed"} />
            </ExternalLink>
          </div>
          <div className="flex-1 flex justify-center items-end mt-6 text-white order-last lg:-order-none basis-full text-center lg:basis-auto mb-6 lg:mb-0">
            <div className="cclw-font font-bold text-xl md:text-3xl">
              <Link href={`/`}>
                <a className="">Climate Change Laws of the World</a>
              </Link>
            </div>
          </div>
          <div className="text-white items-end flex justify-end text-sm flex-grow-0 xbasis-1/3 md:basis-1/4">
            <div className="flex gap-2">
              <p>Powered by</p>
              <ExternalLink className="flex" url="https://www.climatepolicyradar.org">
                <Logo fixed />
              </ExternalLink>
            </div>
          </div>
        </div>
        <div className="flex">
          <nav className="mt-8 flex-1 text-white hidden md:block">
            <ul className="flex justify-center items-end gap-1 h-full text-sm lg:text-base font-bold">
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
      </div>
    </header>
  );
};

export default Header;
