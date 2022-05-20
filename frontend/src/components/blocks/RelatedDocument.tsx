import { useRouter } from 'next/router';
import { truncateString } from '../../helpers';
import { convertDate } from '../../utils/timedate';

interface RelatedDocumentProps {
  document: any;
  onClick(): void;
}

const RelatedDocument = ({ document, onClick }: RelatedDocumentProps) => {
  const router = useRouter();
  const [year, day, month] = convertDate(document?.publication_ts);
  return (
    <div className="relative">
      <div className="flex justify-between items-start">
        <h2 className="leading-none flex items-start">
          <button
            onClick={onClick}
            className="text-left text-blue-500 font-medium text-lg transition duration-300 hover:text-indigo-600 leading-tight"
          >
            {truncateString(document.name, 80)}
          </button>
        </h2>
      </div>
      <div className="flex text-xs text-indigo-400 mt-3">
        <div
          className={`rounded-sm border border-black flag-icon-background flag-icon-${document.country_code.toLowerCase()}`}
        />
        <span className="ml-2">{document.country_name}</span>
        <span className="ml-6">{year}</span>
      </div>
      <p className="text-indigo-400 mt-3">
        {truncateString(document.description.replace(/(<([^>]+)>)/gi, ''), 250)}
      </p>
    </div>
  );
};
export default RelatedDocument;
