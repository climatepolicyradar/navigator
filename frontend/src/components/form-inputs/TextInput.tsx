import React from 'react';
import { FieldErrors, UseFormRegisterReturn } from 'react-hook-form';
import FormFieldError from '../blocks/Error';

interface InputProps {
  label?: string;
  required?: boolean;
  errors: FieldErrors;
  name: string;
  type?: string;
  placeholder?: string;
  accept?: string;
  className?: string;
  onChange?(event: any): any;
  register: any;
}

const TextInput = ({
  label = '',
  required = false,
  errors,
  name,
  type = 'text',
  placeholder = '',
  accept = '',
  className = '',
  onChange,
  register,
}: InputProps): JSX.Element => {
  return (
    <div className={className}>
      <label className="">
        {label}
        {required && label ? (
          <strong className="text-red-500"> *</strong>
        ) : null}
      </label>
      <input
        type={type}
        placeholder={placeholder}
        accept={accept}
        className={`mt-1 border ${
          errors[name] ? 'border-red-500' : 'border-gray-300'
        }`}
        onChange={onChange}
        {...register(name)}
      />
      {errors[name] && <FormFieldError message={errors[name].message} />}
    </div>
  );
};

export default TextInput;
