import { ExternalLink } from "@components/ExternalLink";
import Image from "next/legacy/image";
import { partners } from "../../constants/partners";

const Partners = () => {
  return (
    <div className="py-24">
      <div className="max-w-screen-lg mx-auto">
        <h2 className="text-indigo-500 mb-8 text-center">Our Partners</h2>
        <div className="grid grid-cols-1 gap-8 px-4 mb-8 md:flex md:flex-wrap md:gap-[3%] md:justify-center md:mb-0 xl:px-0">
          {partners.map((partner) => (
            <ExternalLink key={partner.link} className="block relative py-12 unset-img md:basis-[22%] md:mb-8" url={partner.link}>
              <Image src={`/images/partners/${partner.logo}`} alt={partner.name} layout="fill" className="custom-img" />
            </ExternalLink>
          ))}
        </div>
      </div>
    </div>
  );
};
export default Partners;
