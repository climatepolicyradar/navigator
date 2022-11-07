/* eslint-disable @next/next/no-img-element */
import { FC } from "react";
import Link from "next/link";
import Image from "next/image";
import Layout from "@components/layouts/Main";
import { ExternalLink } from "@components/ExternalLink";

type TAcknowledgement = {
  partnerImage?: {
    url: string;
    imageUrl: string;
    imageAlt: string;
  };
};

const Acknowledgement: FC<TAcknowledgement> = ({ partnerImage, children }) => {
  return (
    <div className="mb-12">
      {partnerImage && (
        <div className="flex mb-6">
          <div className="w-full max-w-full md:w-1/3">
            <ExternalLink className="flex relative h-[96px]" url={partnerImage.url}>
              <img src={`/cclw/partners/${partnerImage.imageUrl}`} alt={partnerImage.imageAlt} className="h-full" />
            </ExternalLink>
          </div>
        </div>
      )}
      {children}
    </div>
  );
};

const Acknowledgements = () => {
  return (
    <Layout title={"Acknowledgements"}>
      <section>
        <div className="text-content px-4 container mb-12">
          <h1 className="my-8">Acknowledgements</h1>
          <p>
            The Climate Change Laws of the World project is made possible through the work of many contributors. In particular, the Grantham Research Institute at LSE would like to
            acknowledge the contributions of the following key partners:
          </p>
          <Acknowledgement
            partnerImage={{ url: "https://climate.law.columbia.edu", imageUrl: "Sabin_logo.png", imageAlt: "Sabin Center for Climate Change Law at Columbia Law School logo" }}
          >
            <h4>The Sabin Centre for Climate Change Law at Columbia Law School</h4>
            <p>
              The Sabin Center for Climate Change Law at Columbia Law School develops and promulgates legal techniques to address climate change and trains the next generation of
              lawyers who will be leaders in the field. The Sabin Center is an affiliate of the Earth Institute and the Columbia Climate School. Climate Change Laws of the World
              builds on more than a decade of data collection by the Grantham Research Institute at LSE and the Sabin Center at Columbia Law School. More details about our
              collaboration with the Sabin Center can be found in our “About page” and in our <Link href="/methodology#litigation">"Litigation methodology"</Link>. Work to identify
              cases is now supported by a Global Network of Peer Reviewers, coordinated by the Sabin Center.
            </p>
          </Acknowledgement>
          <Acknowledgement
            partnerImage={{ url: "https://www.filefoundation.org/", imageUrl: "FILE_logo.jpg", imageAlt: "Foundation for International Law and the Environment logo" }}
          >
            <h4>Foundation for International Law and the Environment</h4>
            <p>
              FILE is a global philanthropic foundation supporting legal innovation to address the climate crisis. The Grantham Institute would like to thank FILE for its generous
              support for developments to the database.
            </p>
          </Acknowledgement>
          <Acknowledgement>
            <h4>Climate Policy Radar</h4>
            <p>
              Climate Policy Radar is a not-for-profit, data-led climate startup, on a mission to map and analyse the global climate policy landscape. The organisation is led by a
              team of leading experts in international climate law and policy, machine learning and natural language processing. Climate Policy Radar’s innovative data tools now
              power the Climate Change Laws of the World platform. Through the Grantham Research Institute’s partnership with Climate Policy Radar, we are continuing to work to
              develop new digital approaches to enhance and accelerate the process of gathering and analysing data on developments in global climate change law and policy.
            </p>
          </Acknowledgement>
          <Acknowledgement partnerImage={{ url: "https://www.ipu.org/", imageUrl: "IPU_logo.png", imageAlt: "Inter-Parliamentary Union logo" }}>
            <h4>Inter-Parliamentary Union</h4>
            <p>
              The Inter-Parliamentary Union (IPU) is the global organisation of national parliaments. It began in 1889 as a small group of parliamentarians, dedicated to promoting
              peace through parliamentary diplomacy and dialogue, and has since grown into a truly global organisation of national parliaments. Through the Grantham Research
              Institute’s ongoing partnership with IPU, we work to develop timely and relevant outputs on climate change legislation and policy that can inform the work of IPU’s
              members.
            </p>
          </Acknowledgement>
          <Acknowledgement
            partnerImage={{
              url: "https://www.law.ed.ac.uk/research/research-centres-and-networks/edinburgh-centre-constitutional-law/about",
              imageUrl: "UoE_Law_logo.jpeg",
              imageAlt: "Edinburgh Centre for Constitutional Law logo",
            }}
          >
            <h4>Edinburgh Centre for Constitutional Law, University of Edinburgh</h4>
            <p>
              The Edinburgh Centre for Constitutional Law (ECCL) provides a focal point for staff and postgraduate research students working in all areas of Scots and UK public
              law, Commonwealth and comparative constitutional law, human rights law, environmental law and climate change law, democratisation and transitional constitutionalism,
              and constitutional theory. Data on climate-relevant constitutions found in the Climate Change Laws of the World database is gathered and maintained through an ongoing
              collaboration with ECCL.
            </p>
          </Acknowledgement>
          <Acknowledgement
            partnerImage={{
              url: "https://fossilfueltracker.org/app/ffnpt",
              imageUrl: "FFNPT_logo.png",
              imageAlt: "Fossil Fuel Non-Proliferation Treaty Initiative logo",
            }}
          >
            <h4>Fossil Fuel Non-Proliferation Treaty Initiative</h4>
            <p>
              Based on the best practices of former treaty campaigns and existing struggles led by frontline communities, the Fossil Fuel Non-Proliferation Treaty Initiative
              started in 2019 through a Climate Breakthrough Project award. The Initiative promotes international action to phase out fossil fuel production based on the principles
              of non-proliferation, a fair phase out, and a just transition. LSE collaborates with researchers at the University of Sussex supporting the non-proliferation
              initiative to exchange information on national level laws and policies regarding moratoria, bans, and limits placed on fossil fuel use and/or divestment from fossil
              fuels.
            </p>
          </Acknowledgement>
          <Acknowledgement>
            <h4>JUMA</h4>
            <p>
              The <ExternalLink url="https://www.juma.nima.puc-rio.br/en/base-dados-litigancia-climatica-no-brasil">Brazilian Climate Litigation Platform (JUMA)</ExternalLink> is a
              database dedicated to gathering information on Brazilian climate litigation cases. We collaborate with JUMA to identify cases in Brazil.
            </p>
          </Acknowledgement>
          <Acknowledgement>
            <h4>Interamerican Association for Environmental Defense (AIDA)</h4>
            <p>
              The <ExternalLink url="https://litigioclimatico.com/es/sobre-la-plataforma">Interamerican Association for Environmental Defense (AIDA)</ExternalLink> launched the
              Climate Litigation Platform for Latin America and the Caribbean in 2021. The website provides information on the main climate litigation in Latin America and the
              Caribbean. The platform is a collaborative project led by AIDA with the support of several Latin American organiszations that work for climate justice in the region.
              We collaborate with AIDA to identify climate cases in Latin America and the Caribbean.
            </p>
          </Acknowledgement>
          <Acknowledgement>
            <h4>Melbourne Climate Futures</h4>
            <p>
              <ExternalLink url="https://www.unimelb.edu.au/climate">Melbourne Climate Futures (MCF)</ExternalLink> drives the University of Melbourne’s leadership role on climate
              change, bringing together research and expertise from across the University. MCF's mission is to become a guiding voice for policymakers, industry, the public, and
              the University of Melbourne’s community in Australia and the Indo-Pacific region, to enact real change. <br /> We collaborate with MCF to identify climate cases in
              Australia and the Indo-Pacific region.
            </p>
          </Acknowledgement>
        </div>
      </section>
    </Layout>
  );
};
export default Acknowledgements;
