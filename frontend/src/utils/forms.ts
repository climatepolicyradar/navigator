import { getIn } from 'formik';

export const isRequiredField = ({ validationSchema }, name) =>
  !!getIn(validationSchema.describe().fields, name).tests.find(
    (testName) => testName === 'required'
  );
