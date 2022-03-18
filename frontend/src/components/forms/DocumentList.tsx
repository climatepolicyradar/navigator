import { useState, useEffect } from 'react';
import '../../pages/i18n';
import { useTranslation } from 'react-i18next';

const DocumentList = ({ documents = [] }) => {
  const { t, i18n, ready } = useTranslation([
    'addAction',
    'formErrors',
    'common',
  ]);

  return documents.length > 0 ? (
    <ol
      data-cy="document-list"
      className="mb-4 list-decimal list-inside text-left"
      role="list"
    >
      {documents.map((document, index) => (
        <li key={index} className="my-2">
          <span className="">{document.name}</span>
        </li>
      ))}
    </ol>
  ) : (
    <p className="mb-4">{t('form.No documents added.')}</p>
  );
};

export default DocumentList;
