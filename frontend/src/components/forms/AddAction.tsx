import { useState, useEffect } from 'react';
import { Form, Formik, Field, ErrorMessage } from 'formik';
import * as Yup from 'yup';
import Button from '../buttons/Button';
import TextInput from '../form-inputs/TextInput';
import TextArea from '../form-inputs/TextArea';
import { months, yearRange, daysInMonth } from '../../constants/timedate';
import Select from '../form-inputs/Select';
import { getData, postData } from '../../api';
import Overlay from '../Overlay';
import Popup from '../modals/Popup';
import AddDocument from './AddDocument';
import {
  Document,
  Action,
  Geography,
  Language,
  ActionType,
  Source,
} from '../../interfaces';
import LoaderOverlay from '../LoaderOverlay';
import { fakePromise } from '../../helpers';

interface AddActionProps {
  geographies: Geography[];
  languages: Language[];
  actionTypes: ActionType[];
  sources: Source[];
}

const AddAction = ({
  geographies,
  languages,
  actionTypes,
  sources,
}: AddActionProps) => {
  const [processing, setProcessing] = useState(false);
  const [days, setDays] = useState([]);
  const [popupActive, setPopupActive] = useState(false);
  const initialValues = {
    source_id: '',
    name: '',
    description: '',
    year: '',
    month: '',
    day: '',
    geography_id: '',
    type_id: '',
    documents: [],
  };

  const yearSelections = yearRange();

  const handleDateChange = (e, values) => {
    const today = new Date();
    const thisYear = today.getFullYear();
    let year = values.year ? values.year : thisYear;
    let month = values.month ? values.month : 1;

    if (e.target.name === 'year') {
      year = e.target.value;
    }
    if (e.target.name === 'month') {
      month = e.target.value;
    }
    // change available days in month
    const totalDays = daysInMonth(month, year);
    console.log(month, year);
    setDays(Array.from(Array(totalDays).keys()));
  };

  const processValues = (values) => {
    // React complains when using null values in form fields, so must do all of the below
    // to convert empty values to 1 or null before sending to api

    // unable to send null values for month and day, generates backend error
    if (values.month.length === 0) {
      values.month = 1;
    }
    if (values.day.length === 0) {
      values.day = 1;
    }
    values.documents.forEach((document) => {
      if (document.month.length === 0) {
        document.month = 1;
      }
      if (document.day.length === 0) {
        document.day = 1;
      }
      // need to send null values instead of empty strings otherwise generates backend error
      if (document.source_url.length === 0) {
        document.source_url = null;
      }
      if (document.s3_url.length === 0) {
        document.s3_url = null;
      }
    });
  };

  const submitForm = async (values, resetForm) => {
    setProcessing(true);
    processValues(values);
    let req = 'action';
    resetForm();
    await postData(req, values);
    setProcessing(false);
  };

  useEffect(() => {
    setDays(Array.from(Array(31).keys()));
  }, []);
  return (
    <>
      {processing ? (
        <>
          <LoaderOverlay />
        </>
      ) : null}
      <Overlay
        active={popupActive}
        onClick={() => {
          setPopupActive(false);
        }}
      />
      <div>
        <h1>Submit new action</h1>
        <Formik
          initialValues={initialValues}
          validationSchema={Yup.object({
            source_id: Yup.string().required('Please select a source.'),
            name: Yup.string().required('Required.'),
            year: Yup.string().required('Please select a year.'),
            geography_id: Yup.string().required('Please select a geography.'),
            type_id: Yup.string().required('Please select an action type.'),
            documents: Yup.array().min(
              1,
              'You must add at least one document.'
            ),
          })}
          onSubmit={(values, { setSubmitting, resetForm }) => {
            submitForm(values, resetForm);
          }}
        >
          {({
            values,
            errors,
            touched,
            handleSubmit,
            isSubmitting,
            setFieldValue,
          }) => (
            <>
              <Popup
                active={popupActive}
                onClick={() => {
                  setPopupActive(false);
                }}
              >
                <AddDocument
                  setPopupActive={setPopupActive}
                  days={days}
                  handleDateChange={handleDateChange}
                  yearSelections={yearSelections}
                  year={values.year}
                  month={values.month}
                  day={values.day}
                  languages={languages}
                  active={popupActive}
                />
              </Popup>
              <Form className="lg:w-1/2">
                <div className="form-row">
                  <Field as={Select} label="Source" name="source_id" required>
                    <option>Choose a source</option>
                    {sources.map((source, index) => (
                      <option key={`source${index}`} value={source.source_id}>
                        {source.name}
                      </option>
                    ))}
                  </Field>
                </div>
                <div className="form-row">
                  <TextInput
                    label="Action name"
                    name="name"
                    type="text"
                    required
                  />
                </div>
                <div className="form-row">
                  <TextArea
                    label="Description"
                    name="description"
                    type="text"
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
                      handleDateChange(e, values);
                    }}
                  >
                    <option value="" disabled>
                      Choose
                    </option>
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
                      handleDateChange(e, values);
                    }}
                  >
                    <option value="">Choose</option>
                    {months.map((month, index) => (
                      <option key={index} value={index + 1}>
                        {month}
                      </option>
                    ))}
                  </Field>
                  <Field as={Select} label="Day" name="day" classes="md:w-1/3">
                    <option value="">Choose</option>
                    {days.map((day, index) => (
                      <option key={index} value={day + 1}>
                        {day + 1}
                      </option>
                    ))}
                  </Field>
                </div>
                <div className="form-row">
                  <Field
                    as={Select}
                    label="Geography/Country"
                    name="geography_id"
                    required
                  >
                    <option>Choose a geography</option>
                    {/* TODO - implement input box with suggestions as in prototype */}
                    {geographies.map((geo: Geography) => (
                      <option
                        key={`geo${geo.geography_id}`}
                        value={geo.geography_id}
                      >
                        {geo.english_shortname}
                      </option>
                    ))}
                  </Field>
                </div>
                <div className="form-row">
                  <Field
                    as={Select}
                    label="Action type"
                    name="type_id"
                    required
                  >
                    <option>Choose an action type</option>
                    {actionTypes.map((type: ActionType) => (
                      <option
                        key={`type${type.action_type_id}`}
                        value={type.action_type_id}
                      >
                        {type.type_name}
                      </option>
                    ))}
                  </Field>
                </div>
                <div className="form-row">
                  <h2>Documents</h2>
                  <div className="mt-4">
                    {errors.documents && touched.documents ? (
                      <p className="text-red-500 mb-4">{errors.documents}</p>
                    ) : null}

                    {values.documents.length > 0 ? (
                      <ol
                        className="mb-4 list-decimal list-inside text-left"
                        role="list"
                      >
                        {values.documents.map((document, index) => (
                          <li key={index} className="my-2">
                            <span className="">{document.name}</span>
                          </li>
                        ))}
                      </ol>
                    ) : (
                      <p className="mb-4">No documents added.</p>
                    )}
                  </div>
                  <Button
                    id="cy-add-doc-modal"
                    type="submit"
                    onClick={(e) => {
                      e.preventDefault();
                      window.scrollTo(0, 0);
                      setPopupActive(true);
                    }}
                  >
                    Add a document
                  </Button>
                </div>
                <div className="my-4 flex border-t pt-8 mt-10 border-gray-300">
                  <Button type="submit" color="dark" disabled={isSubmitting}>
                    Submit
                  </Button>
                </div>
              </Form>
            </>
          )}
        </Formik>
      </div>
    </>
  );
};

export default AddAction;
