/* eslint-disable @next/next/no-img-element */
import { ExternalLink } from "@components/ExternalLink";
import Link from "next/link";

type TArticle = {
  url: string;
  type: string;
  title: string;
  imageUrl?: string;
  imageAlt?: string;
  countryCode?: string;
  meta?: string;
  external?: boolean;
};

const ARTICLES: TArticle[] = [
  {
    url: "/document/united-states-of-america_2022_inflation-reduction-act_10699_5931",
    type: "Legislation",
    title: "US Inflation Reduction Act",
    countryCode: "usa",
    meta: "USA | Filing | 2022",
  },
  {
    url: "/document/european-union_2019_the-european-green-deal_9369_3236",
    type: "Legislation",
    title: "The European Green Deal",
    countryCode: "eur",
    meta: "EU | Published | 2019",
    imageUrl: "/cclw/images/eu.jpg",
    imageAlt: "European Union flag",
  },
  {
    url: "/document/fiji_2021_climate-change-act-2021_10190_4775",
    type: "Legislation",
    countryCode: "fji",
    title: "Fiji's Climate Change Act 2021",
    meta: "Fiji | Filing | 2019",
  },
  {
    url: "/document/chile_2022_framework-law-on-climate-change-chile_9772_5709",
    type: "Legislation",
    title: "Framework Law on Climate Change - Chile",
    meta: "Chile | Published | 2022",
    countryCode: "chl",
    imageUrl: "/cclw/images/chile.jpg",
    imageAlt: "Chile flag",
  },
  {
    url: "https://www.lse.ac.uk/granthaminstitute/publication/challenging-government-responses-to-climate-change-through-framework-litigation/",
    external: true,
    type: "Policy brief",
    title: "Challenging government responses to climate change through framework litigation",
    imageUrl: "/cclw/images/hague.jpg",
    imageAlt: "The Hague",
  },
];

export const Articles = () => {
  const renderArticleContent = (article) => {
    return (
      <>
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
      </>
    );
  };

  return (
    <div className="md:flex flex-wrap justify-center">
      {ARTICLES.map((article) => {
        return (
          <div className="p-4 text-primary-400 md:basis-1/2 lg:basis-1/3" key={article.title}>
            {article.external ? (
              <ExternalLink url={article.url} className="block relative border border-grey-400 rounded h-full">
                {renderArticleContent(article)}
              </ExternalLink>
            ) : (
              <Link href={article.url}>
                <a className="block relative border border-grey-400 rounded h-full">{renderArticleContent(article)}</a>
              </Link>
            )}
          </div>
        );
      })}
    </div>
  );
};
