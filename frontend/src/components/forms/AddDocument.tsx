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

  const submitDocument = async (values, resetForm) => {
    setProcessing(true);

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
      id="cy-add-document-form"
      className={`relative mt-8 ${active ? 'is-active' : ''}`}
    >
      {processing ? (
        <>
          <div className="inset-0 fixed"></div>
          <LoaderOverlay />
        </>
      ) : null}
      <h2>Add a document to this action</h2>
      <Formik
        initialValues={initialValues}
        validationSchema={Yup.object(
          {
            name: Yup.string().required('Required'),
            year: Yup.string().required('Please select a year'),
            language_id: Yup.string().required('Please select a language'),
            source_url: Yup.lazy(() =>
              Yup.string().when('file', {
                is: (file) => {
                  return file === undefined;
                },
                then: Yup.string().required(
                  'Please either enter a file URL or select a file.'
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
          },
          ['file', 'source_url']
        )}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          submitDocument(values, resetForm);
        }}
        enableReinitialize
      >
        {({ values, errors, handleSubmit, isSubmitting, setFieldValue }) => (
          <Form>
            <div className="form-row">
              <TextInput
                label="Document name"
                name="name"
                type="text"
                required
              />
            </div>
            <div className="form-row">
              <Field as={Select} label="Language" name="language_id" required>
                <option>Choose a language</option>
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
                label="Enter URL"
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
              <div className="text-sm text-gray-400 mt-1">150Mb maximum</div>
            </div>
            <div className="form-row md:flex items-start">
              <Field
                as={Select}
                label="Year"
                name="year"
                classes="md:w-1/3 md:mr-4"
                required
                onChange={(e) => {
                  setFieldValue('year', e.target.value);
                  handleDateChange(e);
                }}
              >
                <option>Choose</option>
                {yearSelections.map((year, index) => (
                  <option key={index} value={year}>
                    {year}
                  </option>
                ))}
              </Field>
              <Field
                as={Select}
                label="Month"
                name="month"
                classes="md:w-1/3 md:mr-4"
                onChange={(e) => {
                  setFieldValue('month', e.target.value);
                  handleDateChange(e);
                }}
              >
                <option>Choose</option>
                {months.map((month, index) => (
                  <option key={index} value={index + 1}>
                    {month}
                  </option>
                ))}
              </Field>
              <Field as={Select} label="Day" name="day" classes="md:w-1/3">
                <option>Choose</option>
                {days.map((day, index) => (
                  <option key={index} value={day + 1}>
                    {day + 1}
                  </option>
                ))}
              </Field>
            </div>
            <div className="form-row">
              <Button
                id="cy-close-add-document-form"
                color="clear"
                extraClasses="mb-4 md:mb-0 md:mr-2"
                onClick={() => {
                  setPopupActive(false);
                }}
              >
                Cancel
              </Button>{' '}
              <Button id="cy-submit-add-document-form" type="submit">
                Add
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default connect(AddDocuments);
