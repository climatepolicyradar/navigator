import { useState, useEffect } from 'react';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useForm } from 'react-hook-form';
import { useTranslation } from 'react-i18next';
import { postFile } from '../../api';
import { months } from '../../constants/timedate';
import { Document, Language } from '../../interfaces';
import Button from '../buttons/Button';
import TextInput from '../form-inputs/TextInput';
import Select from '../form-inputs/Select';
import LoaderOverlay from '../LoaderOverlay';
import '../../pages/i18n';

interface AddDocumentsProps {
  setPopupActive(value: boolean): void;
  days: number[];
  handleDateChange(e: any): void;
  yearSelections: number[];
  languages: Language[];
  active: boolean;
  getValues: Function;
  setValue: any;
}

function AddDocuments({
  setPopupActive,
  days,
  handleDateChange,
  yearSelections,
  languages,
  active,
  getValues,
  setValue,
}: AddDocumentsProps) {
  const [fileobj, setFileObj] = useState(null);

  const { t, i18n, ready } = useTranslation([
    'addDocument',
    'formErrors',
    'common',
  ]);

  const values = getValues();

  const {
 year, month, day, documents 
} = values;

  const initialValues = {
    name: '',
    language_id: '',
    source_url: '',
    s3_url: '',
    year,
    month,
    day,
    file: '',
  };

  const schema = Yup.object({
    name: Yup.string().required(t('Required', { ns: 'formErrors' })),
    year: Yup.string().required(
      t('Please select a year', { ns: 'formErrors' }),
    ),
    language_id: Yup.string().required(
      t('addDocument.Please select a language.', { ns: 'formErrors' }),
    ),
    source_url: Yup.lazy(() => Yup.string().when('file', {
        is: (file) => file === undefined,
        then: Yup.string().required(
          t('addDocument.Please either enter a file URL or select a file.', {
            ns: 'formErrors',
          }),
        ),
      }),
    ),
    file: Yup.lazy(() => Yup.string().when('source_url', {
        is: (source_url) => source_url === undefined,
        then: Yup.string().required(),
      }),
    ),
  });

  const {
    register,
    handleSubmit,
    formState: { isSubmitting },
    formState: { errors },
    reset,
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: initialValues,
  });

  const submitDocument = async (data) => {
    window.scrollTo(0, 0);
    if (!fileobj) {
      closePopup(data);
      return;
    }

    const req = 'document';
    const formData = new FormData();
    formData.append('file', fileobj);
    const response = await postFile(req, formData);
    data.s3_url = response.url;
    closePopup(data);
  };

  const addDocumentToAction = (document: Document) => {
    documents.push(document);
    setValue('documents', documents);
  };

  const closePopup = (data) => {
    addDocumentToAction(data);
    setPopupActive(false);
    reset();
  };

  return (
    <div
      data-cy="add-document-form"
      className={`relative mt-8 ${active ? 'is-active' : ''}`}
    >
      {isSubmitting ? (
        <>
          <div className="inset-0 fixed" />
          <LoaderOverlay />
        </>
      ) : null}
      <h2>{t('Add a document to this action')}</h2>

      <form onSubmit={handleSubmit(submitDocument)}>
        <div className="form-row">
          <TextInput
            label={t('form.Document name')}
            type="text"
            errors={errors}
            name="name"
            register={register}
            required
          />
        </div>
        <div className="form-row">
          <Select
            data-cy="selectLanguages"
            label={t('form.Language')}
            name="language_id"
            errors={errors}
            register={register}
            required
          >
            <option value="">{t('form.Choose a language')}</option>
            {languages.map((language: Language) => (
              <option
                key={`language${language.language_id}`}
                value={language.language_id}
              >
                {language.name}
              </option>
            ))}
          </Select>
        </div>
        <div className="form-row">
          <TextInput
            label={t('form.Enter URL')}
            type="text"
            placeholder="http://example.com/document.pdf"
            errors={errors}
            name="source_url"
            register={register}
          />
          <p className="mt-8">{t('form.or')}</p>
        </div>
        <div className="form-row">
          <TextInput
            label="Select file"
            accept=".pdf"
            type="file"
            className="w-full"
            errors={errors}
            name="file"
            register={register}
            onChange={(event) => {
              setFileObj(event.currentTarget.files[0]);
            }}
          />
          <div className="text-sm text-gray-400 mt-1">
            150Mb {t('form.maximum')}
          </div>
        </div>
        <div className="form-row md:flex items-start">
          <Select
            label={t('Year', { ns: 'common' })}
            name="year"
            classes="md:w-1/3 md:mr-4"
            required
            errors={errors}
            register={register}
            onChange={handleDateChange}
          >
            <option value="">{t('Choose', { ns: 'common' })}</option>
            {yearSelections.map((year, index) => (
              <option key={index} value={year}>
                {year}
              </option>
            ))}
          </Select>
          <Select
            label={t('Month', { ns: 'common' })}
            name="month"
            classes="md:w-1/3 md:mr-4"
            errors={errors}
            register={register}
            onChange={handleDateChange}
          >
            <option value="">{t('Choose', { ns: 'common' })}</option>
            {months.map((month, index) => (
              <option key={index} value={index + 1}>
                {month}
              </option>
            ))}
          </Select>
          <Select
            label={t('Day', { ns: 'common' })}
            name="day"
            classes="md:w-1/3"
            errors={errors}
            register={register}
          >
            <option value="">{t('Choose', { ns: 'common' })}</option>
            {days.map((day, index) => (
              <option key={index} value={day + 1}>
                {day + 1}
              </option>
            ))}
          </Select>
        </div>
        <div className="form-row">
          <Button
            data-cy="close-add-document-form"
            color="clear"
            extraClasses="mb-4 md:mb-0 md:mr-2"
            onClick={() => {
              setPopupActive(false);
            }}
          >
            {t('Cancel', { ns: 'common' })}
          </Button>
{' '}
          <Button data-cy="submit-add-document-form" type="submit">
            {t('Add', { ns: 'common' })}
          </Button>
        </div>
      </form>
    </div>
  );
}

export default AddDocuments;
