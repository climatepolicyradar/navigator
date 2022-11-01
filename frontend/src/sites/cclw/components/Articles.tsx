/* eslint-disable @next/next/no-img-element */
import Image from "next/image";
import { ExternalLink } from "@components/ExternalLink";

type TArticle = {
  url: string;
  type: string;
  title: string;
  imageUrl?: string;
  imageAlt?: string;
  countryCode?: string;
  meta?: string;
};

const ARTICLES: TArticle[] = [
  {
    url: "https://climate-laws.org/geographies/united-states-of-america/laws/inflation-reduction-act",
    type: "Legislation",
    title: "US Inflation Reduction Act",
    countryCode: "fra",
    meta: "USA | Filing | 2022",
  },
  {
    url: "https://climate-laws.org/geographies/european-union/policies/the-european-green-deal",
    type: "Legislation",
    title: "The European Green Deal",
    countryCode: "eur",
    meta: "EU | Published | 2019",
    imageUrl: "/cclw/images/eu.jpg",
    imageAlt: "European Union flag",
  },
  {
    url: "https://climate-laws.org/geographies/fiji/laws/climate-change-act-2021",
    type: "Legislation",
    title: "Fiji's Climate Change Act 2021",
    meta: "Fiji | Filing | 2019",
  },
  {
    url: "https://climate-laws.org/geographies/chile/laws/framework-law-on-climate-change-chile",
    type: "Legislation",
    title: "Framework Law on Climate Change - Chile",
    meta: "Chile | Published | 2022",
    imageUrl: "/cclw/images/chile.jpg",
    imageAlt: "Chile flag",
  },
  {
    url: "https://www.lse.ac.uk/granthaminstitute/publication/challenging-government-responses-to-climate-change-through-framework-litigation/",
    type: "Policy brief",
    title: "Challenging government responses to climate change through framework litigation",
    imageUrl: "/cclw/images/hague.jpg",
    imageAlt: "The Hague",
  },
];

export const Articles = () => {
  return (
    <div className="md:flex flex-wrap justify-center">
      {ARTICLES.map((article) => {
        return (
          <div className="p-4 text-primary-400 md:basis-1/2 lg:basis-1/3" key={article.title}>
            <ExternalLink url={article.url} className="block relative border border-grey-400 rounded h-full">
              <div className="absolute top-0 left-0 p-2 px-4 bg-secondary-500 rounded text-sm font-bold text-white z-10">{article.type}</div>
              <div className="text-center flex flex-col justify-center items-center min-h-[180px]">
                {article.imageUrl && (
                  <div className="w-full h-[120px] overflow-hidden relative">
                    <img src={article.imageUrl} alt={article.imageAlt} />
                  </div>
                )}
                <div className={`p-4 text-primary-400 flex-1 flex items-center text-lg font-bold ${article.imageUrl ? "" : "pt-8"}`}>{article.title}</div>
                {article.meta && (
                  <div className="flex items-center gap-2 mb-2 text-grey-700">
                    {article.countryCode && <span className={`rounded-sm border border-black flag-icon-background flag-icon-${article.countryCode} inline-block`} />}
                    <div className="">{article.meta}</div>
                  </div>
                )}
              </div>
            </ExternalLink>
          </div>
        );
      })}
    </div>
  );
};
