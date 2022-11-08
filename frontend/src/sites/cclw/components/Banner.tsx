import { ExternalLink } from "@components/ExternalLink";

export const Banner = () => {
  return (
    <div className="bg-[#7cb4fa] w-full flex justify-center p-2 font-bold text-sm">
      <div>
        This is a preview and will soon be available on the climate-laws.org website,{" "}
        <ExternalLink className="underline" url="https://climatepolicyradar.org/latest/new-partnership-launches-ai-powered-global-climate-law-and-policy-database">see full announcement</ExternalLink>
      </div>
    </div>
  );
};
