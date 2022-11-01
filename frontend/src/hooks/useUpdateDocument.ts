import { QueryClient, useMutation, useQueryClient } from "react-query";
import { v4 as uuidv4 } from "uuid";
import { TDocument } from "@types";
import { Updater } from "react-query/types/core/utils";

type TSearchResultsDocuments = {
  data: {
    documents: TDocument[];
  };
};

const switchDocuments = (queryClient: QueryClient, slug: string) => {
  const {
    data: { documents },
  }: TSearchResultsDocuments = queryClient.getQueryData<TSearchResultsDocuments>("searches");

  const document = documents.find((item) => item.slug === slug);

  // add fileid for Adobe PDF embed
  const newDocument = { ...document, document_fileid: uuidv4() };

  queryClient.setQueryData("document", 
    (old : Updater<TDocument, TDocument>) => ({...old, ...newDocument,})
  );
}

export default function useUpdateDocument() {
  const queryClient = useQueryClient();

  return useMutation(
    async (slug: string) => switchDocuments(queryClient, slug)
  );
}
