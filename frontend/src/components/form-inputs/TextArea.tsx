import React from 'react';
import { useField } from 'formik';

interface TextAreaProps {
  id?: string;
  name: string;
  label: string;
  type: string;
  classes?: string;
}

const TextArea = ({ label, classes = '', ...props }: TextAreaProps) => {
  // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
  // which we can spread on <input>. We can use field meta to show an error
  // message if the field is invalid and it has been touched (i.e. visited)
  const [field, meta] = useField(props);

  return (
    <>
      <label htmlFor={props.id || props.name}>{label}</label>
      <textarea
        className={`p-2 text-lg border border-gray-300 rounded w-full appearance-none ${classes}`}
        type={props.type}
        {...field}
        {...props}
      />
      {meta.touched && meta.error ? (
        <div className="error">{meta.error}</div>
      ) : null}
    </>
  );
};

export default TextArea;
