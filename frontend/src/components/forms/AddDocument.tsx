import { useState, useEffect } from 'react';
import { Form, Formik, Field, connect } from 'formik';
import * as Yup from 'yup';
import { postFile } from '../../api';
import { months } from '../../constants/timedate';
import { Document, Language } from '../../interfaces';
import Button from '../buttons/Button';
import TextInput from '../form-inputs/TextInput';
import Select from '../form-inputs/Select';
import LoaderOverlay from '../LoaderOverlay';
import { fakePromise } from '../../helpers';
import '../../pages/i18n';
import { useTranslation } from 'react-i18next';

interface AddDocumentsProps {
  setPopupActive(): void;
  days: number;
  handleDateChange(): void;
  yearSelections: number[];
  languages: Language[];
  active: boolean;
}

const AddDocuments = ({
  setPopupActive,
  days,
  handleDateChange,
  yearSelections,
  languages,
  active,
  ...props
}) => {
  const [processing, setProcessing] = useState(false);
  const [fileobj, setFileObj] = useState(null);

  let { formik, year, month, day } = props;
  let {
    values: { documents },
  } = formik;
  const initialValues = {
    name: '',
    language_id: '',
    source_url: '',
    s3_url: '',
    year: year,
    month: month,
    day: day,
    file: '',
  };

  const { t, i18n, ready } = useTranslation([
    'addDocument',
    'formErrors',
    'common',
  ]);

  const submitDocument = async (values, resetForm) => {
    setProcessing(true);
    window.scrollTo(0, 0);
    if (!fileobj) {
      closePopup(values, resetForm);
      return;
    }

    const req = 'document';
    let formData = new FormData();
    formData.append('file', fileobj);
    const response = await postFile(req, formData);
    values.s3_url = response.url;
    closePopup(values, resetForm);
  };

  const addDocumentToAction = (document: Document) => {
    documents.push(document);
  };

  const closePopup = (values, resetForm) => {
    addDocumentToAction(values);
    setPopupActive(false);
    setProcessing(false);
    resetForm();
  };

  return (
    <div
      data-cy="add-document-form"
      className={`relative mt-8 ${active ? 'is-active' : ''}`}
    >
      {processing ? (
        <>
          <div className="inset-0 fixed"></div>
          <LoaderOverlay />
        </>
      ) : null}
      <h2>{t('summary')}</h2>
      <Formik
        initialValues={initialValues}
        validationSchema={Yup.object({
          name: Yup.string().required(t('required', { ns: 'formErrors' })),
          year: Yup.string().required(t('year', { ns: 'formErrors' })),
          language_id: Yup.string().required(
            t('addDocument.language', { ns: 'formErrors' })
          ),
          source_url: Yup.lazy(() =>
            Yup.string().when('file', {
              is: (file) => {
                return file === undefined;
              },
              then: Yup.string().required(
                t('addDocument.file', { ns: 'formErrors' })
              ),
            })
          ),
          file: Yup.lazy(() =>
            Yup.string().when('source_url', {
              is: (source_url) => {
                return source_url === undefined;
              },
              then: Yup.string().required(),
            })
          ),
        })}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          submitDocument(values, resetForm);
        }}
        enableReinitialize
      >
        {({ values, errors, handleSubmit, isSubmitting, setFieldValue }) => (
          <Form>
            <div className="form-row">
              <TextInput
                label={t('form.documentName')}
                name="name"
                type="text"
                required
              />
            </div>
            <div className="form-row">
              <Field
                as={Select}
                data-cy="selectLanguages"
                label={t('form.language')}
                name="language_id"
                required
              >
                <option>{t('form.languageDefault')}</option>
                {languages.map((language: Language) => (
                  <option
                    key={`language${language.language_id}`}
                    value={language.language_id}
                  >
                    {language.name}
                  </option>
                ))}
              </Field>
            </div>
            <div className="form-row">
              <TextInput
                label={t('form.url')}
                name="source_url"
                type="text"
                placeholder="http://example.com/document.pdf"
              />
              <p className="mt-8">or</p>
            </div>
            <div className="form-row">
              <Field
                label="Select file"
                name="file"
                accept=".pdf"
                type="file"
                className="w-full"
                onChange={(event) => {
                  console.log(event.currentTarget.files[0]);
                  setFieldValue('file', event.currentTarget.value);
                  setFileObj(event.currentTarget.files[0]);
                }}
              />
              <div className="text-sm text-gray-400 mt-1">
                {t('form.maxMb')}
              </div>
            </div>
            <div className="form-row md:flex items-start">
              <Field
                as={Select}
                label={t('year', { ns: 'common' })}
                name="year"
                classes="md:w-1/3 md:mr-4"
                required
                onChange={(e) => {
                  setFieldValue('year', e.target.value);
                  handleDateChange(e, values);
                }}
              >
                <option>{t('choose', { ns: 'common' })}</option>
                {yearSelections.map((year, index) => (
                  <option key={index} value={year}>
                    {year}
                  </option>
                ))}
              </Field>
              <Field
                as={Select}
                label={t('month', { ns: 'common' })}
                name="month"
                classes="md:w-1/3 md:mr-4"
                onChange={(e) => {
                  setFieldValue('month', e.target.value);
                  handleDateChange(e, values);
                }}
              >
                <option>{t('choose', { ns: 'common' })}</option>
                {months.map((month, index) => (
                  <option key={index} value={index + 1}>
                    {month}
                  </option>
                ))}
              </Field>
              <Field
                as={Select}
                label={t('day', { ns: 'common' })}
                name="day"
                classes="md:w-1/3"
              >
                <option>{t('choose', { ns: 'common' })}</option>
                {days.map((day, index) => (
                  <option key={index} value={day + 1}>
                    {day + 1}
                  </option>
                ))}
              </Field>
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
                {t('cancel', { ns: 'common' })}
              </Button>{' '}
              <Button data-cy="submit-add-document-form" type="submit">
                {t('add', { ns: 'common' })}
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default connect(AddDocuments);
