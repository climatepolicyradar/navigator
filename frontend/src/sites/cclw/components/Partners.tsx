/* eslint-disable @next/next/no-img-element */
import Image from "next/image";
import { ExternalLink } from "@components/ExternalLink";

const partners = [
  {
    link: "https://climate.law.columbia.edu",
    logo: "Sabin_logo.png",
    name: "The Sabin Centre for Climate Change Law at Columbia Law School",
  },
  {
    link: "https://www.filefoundation.org",
    logo: "File_logo.jpg",
    name: "Foundation for International Law and the Environment",
  },
  {
    link: "https://fossilfueltracker.org/app/ffnpt",
    logo: "FFNPT_logo.png",
    name: "Fossil Fuel Non-Proliferation Treaty Initiative",
  },
  {
    link: "https://www.ipu.org",
    logo: "IPU_logo.png",
    name: "Inter-Parliamentary Union",
  },
  {
    link: "https://www.law.ed.ac.uk/research/research-centres-and-networks/edinburgh-centre-constitutional-law/about",
    logo: "UoE_Law_logo.jpeg",
    name: "Edinburgh Centre for Constitutional Law, University of Edinburgh",
  },
];

export const Partners = () => {
  return (
    <div className="md:flex flex-wrap justify-center">
      {partners.map((partner) => (
        <div className="md:basis-1/2 lg:basis-1/3" key={partner.link}>
          <div className="m-4">
            <ExternalLink className="flex justify-center relative h-[96px]" url={partner.link}>
              <img src={`/cclw/partners/${partner.logo}`} alt={partner.name} className="h-full" />
            </ExternalLink>
          </div>
        </div>
      ))}
    </div>
  );
};
