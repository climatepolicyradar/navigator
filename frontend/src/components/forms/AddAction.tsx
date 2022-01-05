import { useState, useRef } from 'react';
import { Form, Formik, Field, ErrorMessage } from 'formik';
import axios from 'axios';
import Button from '../Button';
import * as Yup from 'yup';
import TextInput from '../form-inputs/TextInput';
import TextArea from '../form-inputs/TextArea';
import { months, yearRange, daysInMonth } from '../../constants/timedate';
import Select from '../form-inputs/Select';

const AddAction = () => {
  const [days, setDays] = useState(31);
  // const [action, setAction] = useState({
  //   name: '',
  //   description: '',
  //   year: '',
  //   month: '',
  //   day: '',
  //   geography_id: '',
  //   languages: [],
  //   type_id: '',
  //   documents: [],
  // });
  const initialValues = {
    name: '',
    description: '',
    year: '',
    month: '',
    day: '',
    geography_id: '',
    languages: [],
    type_id: '',
    documents: [],
  };

  const yearSelections = yearRange();
  const monthRef = useRef<HTMLSelectElement>(null);
  const yearRef = useRef<HTMLSelectElement>(null);

  const handleDateChange = (e) => {
    console.log('date changed');
    console.log(daysInMonth(e.target.value, 2022));
    setDays(daysInMonth(e.target.value, 2022));
  };

  const postData = async (req: string, data): Promise<any> => {
    return await axios.post(req).then((response) => {
      return response.statusText == 'OK'
        ? response.data
        : Promise.reject(Error('Unsuccessful response'));
    });
  };

  const submitForm = async (values) => {
    let req = 'http://localhost:8000/api/policies';
    console.log(values);
    // setAction(values);
    // return await postData(req, values);
  };
  return (
    <div>
      <h1>Submit new action</h1>
      <Formik
        initialValues={initialValues}
        validationSchema={Yup.object({
          name: Yup.string().required('Required'),
        })}
        onSubmit={(values, { setSubmitting }) => {
          submitForm(values);
        }}
      >
        {({ values, handleSubmit, isSubmitting }) => (
          <Form className="lg:w-1/2">
            <div className="form-row">
              <TextInput label="Action name" name="name" type="text" />
            </div>
            <div className="form-row">
              <TextArea label="Description" name="description" type="text" />
            </div>
            <div className="form-row">
              <Select
                label="Year"
                name="year"
                ref={yearRef}
                onChange={handleDateChange}
              >
                {yearSelections.map((year, index) => (
                  <option key={index} value={index}>
                    {year}
                  </option>
                ))}
              </Select>
            </div>
            <div className="form-row">
              <Select
                label="Month"
                name="month"
                ref={monthRef}
                onChange={handleDateChange}
              >
                {months.map((month, index) => (
                  <option key={index} value={index + 1}>
                    {month}
                  </option>
                ))}
              </Select>
            </div>
            {/* <div className="my-4 flex">
              <label className="w-1/4">Year</label>
              <input
                className="ml-4 w-3/4"
                type="number"
                name="year"
                value={values.year}
              />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Month</label>
              <input
                className="ml-4 w-3/4"
                type="number"
                name="month"
                value={values.month}
              />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Day</label>
              <input
                className="ml-4 w-3/4"
                type="number"
                name="day"
                value={values.day}
              />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Geography</label>
              <input
                className="ml-4 w-3/4"
                type="text"
                name="geography_id"
                value={values.geography_id}
              />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Languages</label>
              <input
                className="ml-4 w-3/4"
                type="text"
                name="languages"
                value={values.languages}
              />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Action type</label>
              <input
                className="ml-4 w-3/4"
                type="text"
                name="type_id"
                value={values.type_id}
              />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Documents</label>
              <input
                className="ml-4 w-3/4"
                type="file"
                name="documents"
                multiple
              />
            </div>
            <div className="my-4 flex">
              <label className="w-1/4">Document URLs</label>
              <input className="ml-4 w-3/4" type="text" name="url" />
            </div> */}
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
