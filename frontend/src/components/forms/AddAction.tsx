import { useState, useEffect } from 'react';
import { Form, Formik, Field, ErrorMessage } from 'formik';
import axios from 'axios';
import Button from '../Button';
import * as Yup from 'yup';
import TextInput from '../form-inputs/TextInput';
import TextArea from '../form-inputs/TextArea';
import { months, yearRange, daysInMonth } from '../../constants/timedate';
import Select from '../form-inputs/Select';
import { postData } from '../../api';

const AddAction = () => {
  const [days, setDays] = useState([]);

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

  const handleDateChange = (e) => {
    console.log(daysInMonth(e.target.value, 2022));
    const totalDays = daysInMonth(e.target.value, 2022);
    setDays(Array.from(Array(totalDays).keys()));
  };

  const submitForm = async (values, resetForm) => {
    if (values.month.length === 0) {
      values.month = null;
    }
    if (values.day.length === 0) {
      values.day = null;
    }
    let req = 'action';
    console.log(values);
    resetForm();
    return await postData(req, values);
  };

  useEffect(() => {
    setDays(Array.from(Array(31).keys()));
  }, []);
  return (
    <div>
      <h1>Submit new action</h1>
      <Formik
        initialValues={initialValues}
        validationSchema={Yup.object({
          source_id: Yup.string().required('Please select a source'),
          name: Yup.string().required('Required'),
          year: Yup.string().required('Please select a year'),
          geography_id: Yup.string().required('Please select a geography'),
          type_id: Yup.string().required('Please select an action type'),
        })}
        onSubmit={(values, { setSubmitting, resetForm }) => {
          submitForm(values, resetForm);
        }}
      >
        {({ values, handleSubmit, isSubmitting, setFieldValue }) => (
          <Form className="lg:w-1/2">
            <div className="form-row">
              <Field as={Select} label="Source" name="source_id" required>
                <option>Choose a source</option>
                {/* TODO - get sources from API when it's ready */}
                <option value="1">CCLW</option>
                <option value="2">CPD</option>
              </Field>
            </div>
            <div className="form-row">
              <TextInput label="Action name" name="name" type="text" required />
            </div>
            <div className="form-row">
              <TextArea label="Description" name="description" type="text" />
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
            <div className="form-row md:flex">
              <Field
                as={Select}
                label="Geography/Country"
                name="geography_id"
                classes="mr-4"
                required
              >
                <option>Choose a geography</option>
                {/* TODO - get geographies from API when it's ready */}
                <option value="1">United Kingdom</option>
                <option value="2">United States</option>
              </Field>
              <Field as={Select} label="Action type" name="type_id" required>
                <option>Choose an action type</option>
                {/* TODO - get action types from API when it's ready */}
                <option value="1">Policy</option>
                <option value="2">Law</option>
              </Field>
            </div>
            <div className="my-4 flex">
              <Button type="submit" disabled={isSubmitting}>
                Submit
              </Button>
            </div>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default AddAction;
