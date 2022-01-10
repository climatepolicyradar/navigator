import { useState, useEffect } from 'react';
import { Form, Formik, Field, connect, validateYupSchema } from 'formik';
import * as Yup from 'yup';
import { postData } from '../../api';
import { months } from '../../constants/timedate';
import { Document } from '../../interfaces';
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
}

const AddDocuments = ({
  setPopupActive,
  days,
  handleDateChange,
  yearSelections,
  ...props
}) => {
  const [processing, setProcessing] = useState(false);

  let { formik, year, month, day } = props;
  let {
    values: { documents },
  } = formik;
  const initialValues = {
    name: '',
    language_id: '',
    source_url: '',
    s3_url: null,
    year: year,
    month: month,
    day: day,
    file: '',
  };

  const submitDocument = async (values, resetForm) => {
    let req = 'document';
    setProcessing(true);
    // await postData(req, values.file);
    await fakePromise(2000, 'done');
    console.log(values);
    // below lines will execute after api request fulfilled sucessfully
    addDocumentToAction(values);
    setPopupActive(false);
    setProcessing(false);
    resetForm();
  };

  const addDocumentToAction = (document: Document) => {
    documents.push(document);
  };

  return (
    <div className="relative mt-8">
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
                  'Please either select a file or enter a file URL'
                ),
              })
            ),
            file: Yup.lazy(() =>
              Yup.string().when('source_url', {
                is: (source_url) => {
                  return source_url === undefined;
                },
                then: Yup.string().required(
                  'Please either select a file or enter a file URL'
                ),
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
            {console.log(errors)}
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
                {/* TODO - get languages from API when it's ready */}
                <option value="1">English</option>
                <option value="2">French</option>
              </Field>
            </div>
            <div className="form-row">
              <TextInput label="Enter URL" name="source_url" type="text" /> or
            </div>
            <div className="form-row">
              <Field
                label="Select file"
                name="file"
                accept=".pdf"
                type="file"
              />
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
              <Button type="submit">Add</Button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default connect(AddDocuments);
