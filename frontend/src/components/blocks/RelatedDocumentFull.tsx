import { convertDate } from "@utils/timedate";
import { TDocument } from "@types";
import { DocumentListItem } from "@components/document/DocumentListItem";

type TProps = {
  document: TDocument;
};

export const RelatedDocumentFull = ({ document }: TProps) => {
  const { document_country_code, document_country_english_shortname, document_id, document_date, document_description, document_name, document_category } = document;
  const [year] = convertDate(document_date);
  
  return (
    <DocumentListItem
      listItem={{
        id: document_id,
        name: document_name,
        country_code: document_country_code,
        country_name: document_country_english_shortname,
        document_year: year,
        description: document_description,
        category: document_category,
      }}
    />
  );
};
