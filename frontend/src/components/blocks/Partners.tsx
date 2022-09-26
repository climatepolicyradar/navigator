import { ExternalLink } from "@components/ExternalLink";
import Image from "next/image";
import { partners } from "../../constants/partners";

const Partners = () => {
  return (
    <div className="py-24">
      <div className="max-w-screen-lg mx-auto">
        <h2 className="text-indigo-500 mb-8 text-center">Our Partners</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 md:gap-16 px-4 xl:px-0 mb-8 md:mb-0">
          {partners.map((partner) => (
            <ExternalLink key={partner.link} className="block relative py-12 unset-img" url={partner.link}>
              <Image src={`/images/partners/${partner.logo}`} alt={partner.name} layout="fill" className="custom-img" />
            </ExternalLink>
          ))}
        </div>
      </div>
    </div>
  );
};
export default Partners;
