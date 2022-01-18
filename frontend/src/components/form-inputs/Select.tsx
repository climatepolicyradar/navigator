import React from 'react';
import { useField } from 'formik';

interface SelectProps {
  id?: string;
  name: string;
  label: string;
  children: React.ReactNode;
  classes?: string;
  required?: boolean;
}

const Select = ({
  label,
  children,
  required = false,
  classes = '',
  ...props
}: SelectProps) => {
  const [field, meta] = useField(props);
  return (
    <div className={`${classes}`}>
      <label htmlFor={props.id || props.name}>
        {label}
        {required ? <strong className="text-red-500"> *</strong> : null}
      </label>
      <select
        {...field}
        {...props}
        className={`${
          meta.touched && meta.error ? 'border-red-500' : 'border-gray-300'
        }`}
      >
        {children}
      </select>

      {meta.touched && meta.error ? (
        <div className="error text-red-500 mt-1">{meta.error}</div>
      ) : null}
    </div>
  );
};

export default Select;
