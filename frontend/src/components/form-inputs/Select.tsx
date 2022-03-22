import React from 'react';
import { FieldErrors, UseFormRegisterReturn } from 'react-hook-form';
import FormFieldError from '../text-blocks/Error';

interface SelectProps {
  id?: string;
  name: string;
  label: string;
  children: React.ReactNode;
  classes?: string;
  required?: boolean;
  errors: FieldErrors;
  onChange?(event: any): any;
  register: any;
  'data-cy'?: string;
}

const Select = ({
  id,
  label,
  name,
  children,
  required = false,
  classes = '',
  onChange = () => {},
  errors,
  register,
  'data-cy': dataCy,
}: SelectProps) => {
  return (
    <div className={`${classes}`}>
      <label htmlFor={id} className="text-indigo-600">
        {label}
        {required ? <strong className="text-red-500"> *</strong> : null}
      </label>
      <select
        data-cy={dataCy}
        onChange={onChange}
        className={`border ${
          errors[name] ? 'border-red-500' : 'border-gray-300'
        }`}
        {...register(name)}
      >
        {children}
      </select>

      {errors[name] ? <FormFieldError message={errors[name].message} /> : null}
    </div>
  );
};

export default Select;
