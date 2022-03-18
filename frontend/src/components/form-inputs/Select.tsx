import React from 'react';
import { useField } from 'formik';

interface SelectProps {
  id?: string;
  name: string;
  label: string;
  children: React.ReactNode;
  classes?: string;
  required?: boolean;
  errors: Object;
  register: any;
  onChange?: any;
}

const Select = ({
  id,
  label,
  name,
  register,
  children,
  required = false,
  classes = '',
  onChange = () => {},
  errors,
}: SelectProps) => {
  return (
    // <div className={`${classes}`}>
    //   <label htmlFor={props.id || props.name} className="text-indigo-600">
    //     {label}
    //     {required ? <strong className="text-red-500"> *</strong> : null}
    //   </label>
    //   <select
    //     {...field}
    //     {...props}
    //     className={`${
    //       meta.touched && meta.error ? 'border-red-500' : 'border-gray-300'
    //     }`}
    //   >
    //     {children}
    //   </select>

    //   {meta.touched && meta.error ? (
    //     <div className="error text-red-500 mt-1">{meta.error}</div>
    //   ) : null}
    // </div>
    <div className={`${classes}`}>
      <label htmlFor={id} className="text-indigo-600">
        {label}
        {required ? <strong className="text-red-500"> *</strong> : null}
      </label>
      <select
        {...register(name)}
        onChange={onChange}
        className={`border ${
          errors[name] ? 'border-red-500' : 'border-gray-300'
        }`}
      >
        {children}
      </select>

      {errors[name] ? (
        <div className="error text-red-500 mt-1">{errors[name].message}</div>
      ) : null}
    </div>
  );
};

export default Select;
