import React from 'react';
import { FieldErrors, UseFormRegisterReturn } from 'react-hook-form';

interface TextAreaProps {
  id?: string;
  name: string;
  label: string;
  classes?: string;
  required?: boolean;
  placeholder?: string;
  errors: FieldErrors;
  register: any;
}

const TextArea = ({
  id = '',
  name,
  label,
  required = false,
  placeholder = '',
  errors,
  classes = '',
  register,
}: TextAreaProps) => {
  return (
    <div className={`${classes}`}>
      <label htmlFor={id} className="text-indigo-600">
        {label}
        {required ? <strong className="text-red-500"> *</strong> : null}
      </label>
      <textarea
        id={id}
        className={`border ${
          errors[name] ? 'border-red-500' : 'border-gray-300'
        }`}
        placeholder={placeholder}
        {...register(name)}
      />
      {errors[name] && (
        <div className="error w-full text-red-500">{errors[name].message}</div>
      )}
    </div>
  );
};

export default TextArea;
