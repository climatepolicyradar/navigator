import { convertDate } from "@utils/timedate";
import { TAssociatedDocument } from "@types";
import { DocumentListItem } from "@components/document/DocumentListItem";

interface RelatedDocumentProps {
  document: TAssociatedDocument;
}

export const RelatedDocument = ({ document }: RelatedDocumentProps) => {
  const { country_code, country_name, document_id, publication_ts, category, description, name } = document;
  const [year] = convertDate(publication_ts);

  return (
    <DocumentListItem
      listItem={{
        id: document_id,
        name: name,
        country_code: country_code,
        country_name: country_name,
        document_year: year,
        description: description,
        category: category,
      }}
    />
  );
};
