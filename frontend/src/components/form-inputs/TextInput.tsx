import React from 'react';
import { useField } from 'formik';

interface TextInputProps {
  id?: string;
  name: string;
  label: string;
  type: string;
}

const TextInput = ({ label, ...props }: TextInputProps) => {
  // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
  // which we can spread on <input>. We can use field meta to show an error
  // message if the field is invalid and it has been touched (i.e. visited)
  const [field, meta] = useField(props);
  // console.log(field);
  return (
    <>
      <label htmlFor={props.id || props.name}>{label}</label>
      <input
        className="w-full p-1 text-lg border border-gray-300 rounded"
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

export default TextInput;
