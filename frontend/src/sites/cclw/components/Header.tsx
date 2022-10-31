import { useRouter } from "next/router";
import Link from "next/link";
import Image from "next/image";
import { ExternalLink } from "@components/ExternalLink";
import Logo from "@components/svg/LogoMono";
import { SearchIcon } from "@components/svg/Icons";
import { useState } from "react";
import Button from "@components/buttons/Button";

const Header = ({ background = true }) => {
  const { pathname } = useRouter();
  const [menuOpen, setMenuOpen] = useState(false);

  const linkClass = (pageUrl: string) => {
    return pathname.toLowerCase() === pageUrl ? "active" : "";
  };

  const isHome = pathname.toLowerCase() === "/";

  return (
    <header data-cy="header" className={`${background ? "bg-secondary-700" : ""} w-full border-b-2 pt-6 lg:pt-0`}>
      <div className="container">
        <div className={`flex flex-wrap lg:flex-nowrap justify-between ${isHome ? "lg:mb-6" : ""}`}>
          <div className="items-end flex flex-grow-0 lg:basis-1/5">
            <ExternalLink className="flex" url="https://www.lse.ac.uk/">
              <Image src="/images/partners/lse-logo.png" alt="LSE logo" width={40} height={40} layout={"fixed"} />
            </ExternalLink>
            <ExternalLink className="flex" url="https://www.lse.ac.uk/granthaminstitute/">
              <Image src="/cclw/partners/gri_white_logo.svg" alt="GRI logo" width={180} height={40} layout={"fixed"} />
            </ExternalLink>
          </div>
          <div
            className={`flex-1 flex justify-center items-end text-white order-last lg:-order-none basis-full text-center lg:basis-auto mb-6 lg:mb-0 ${isHome ? "mt-10" : "mt-6"}`}
          >
            <div className="cclw-font font-bold text-2xl md:text-4xl lg:text-3xl xl:text-4xl">
              <Link href={`/`}>
                <a className="">Climate Change Laws of the World</a>
              </Link>
            </div>
          </div>
          <div className="text-white items-end flex justify-end text-sm flex-grow-0 lg:basis-1/5">
            <div className="flex gap-2">
              <p>Powered by</p>
              <ExternalLink className="flex" url="https://www.climatepolicyradar.org">
                <Logo fixed />
              </ExternalLink>
            </div>
          </div>
        </div>
        <div className="flex flex-col">
          <Button
            thin
            onClick={() => {
              setMenuOpen(!menuOpen);
            }}
            extraClasses="mb-6 text-sm font-normal md:hidden"
          >
            {menuOpen ? <>Hide menu &#x25B2;</> : <>Show menu &#x25BC;</>}
          </Button>
          <nav className={`mt-8 flex-1 text-white transition duration-300 ${menuOpen ? "" : "hidden md:block"}`}>
            <ul className="grid grid-cols-2 md:flex justify-center items-end gap-1 h-full text-sm lg:text-base font-bold">
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
                  <a className={linkClass("/search") + " !flex gap-2"}>
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
