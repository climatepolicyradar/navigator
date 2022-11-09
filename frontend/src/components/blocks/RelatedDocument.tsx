import { convertDate } from "@utils/timedate";
import { TAssociatedDocument } from "@types";
import { DocumentListItem } from "@components/document/DocumentListItem";

interface RelatedDocumentProps {
  document: TAssociatedDocument;
}

export const RelatedDocument = ({ document }: RelatedDocumentProps) => {
  const { country_code, country_name, slug, publication_ts, category, description, name } = document;
  const [year] = convertDate(publication_ts);

  return (
    <DocumentListItem
      listItem={{
        slug: slug,
        name: name,
        country_code: country_code,
        document_year: year,
        description: description,
        category: category,
      }}
    />
  );
};
