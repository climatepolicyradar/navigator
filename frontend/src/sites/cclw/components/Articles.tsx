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
    url: "google.com",
    type: "Litigation",
    title: "Greenpeace France and Others v. TotalEnergies SE and TotalEnergies Electricité et Gaz France",
    countryCode: "fra",
    meta: "France | Filing | 2022",
  },
  {
    url: "google.com",
    type: "Legislation",
    title: "The European Green Deal",
    countryCode: "eur",
    meta: "EU | Published | 2019",
    imageUrl: "/cclw/images/eu.jpg",
    imageAlt: "European Union flag",
  },
  {
    url: "google.com",
    type: "Litigation",
    title: "Petition of Torres Strait Islanders to the United Nations Human Rights Committee Alleging Violations Stemming from ...",
    meta: "International | Filing | 2019",
  },
  {
    url: "google.com",
    type: "Legislation",
    title: "Framework Law on Climate Change - Chile",
    meta: "Chile | Published | 2022",
    imageUrl: "/cclw/images/chile.jpg",
    imageAlt: "Chile flag",
  },
  {
    url: "google.com",
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
                    <Image src={article.imageUrl} alt={article.imageAlt} layout="fill" objectFit="cover" />
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
