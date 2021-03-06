import Link from 'next/link';
import { truncateString } from '../../helpers';
import { convertDate } from '../../utils/timedate';

interface RelatedDocumentProps {
  document: any;
}

const RelatedDocument = ({ document }: RelatedDocumentProps) => {
  const [year] = convertDate(document?.publication_ts);
  return (
    <div className="relative">
      <div className="flex justify-between items-start">
        <h2 className="leading-none flex items-start">
          <Link href={`/document/${document.related_id}`}>
            <a className="text-left text-blue-500 font-medium text-lg transition duration-300 hover:text-indigo-600 leading-tight">
              {truncateString(document.name, 80)}
            </a>
          </Link>
        </h2>
      </div>
      <div className="flex text-sm text-indigo-400 mt-3">
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
