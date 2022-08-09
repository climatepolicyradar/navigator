import React from 'react';
import { FieldErrors } from 'react-hook-form';
import FormFieldError from '../blocks/Error';

interface InputProps {
  label?: string;
  required?: boolean;
  errors: {};
  name: string;
  type?: string;
  placeholder?: string;
  accept?: string;
  className?: string;
  onChange?(event: any): any;
  register: any;
  icon?: React.ReactNode;
}

function TextInput({
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
  icon,
}: InputProps) {
  return (
    <div className={className}>
      <label className="">
        {label}
        {required && label ? (
          <strong className="text-red-500"> *</strong>
        ) : null}
      </label>
      <div className="relative mt-1">
        <input
          type={type}
          placeholder={placeholder}
          accept={accept}
          className={`border ${
            errors[name] ? 'border-red-500' : 'border-gray-300'
          }`}
          onChange={onChange}
          {...register(name)}
        />
        {icon && (
          <div className="absolute inset-y-0 right-5 flex items-center">
            {icon}
          </div>
        )}
      </div>
      {errors[name] && <FormFieldError message={errors[name].message} />}
    </div>
  );
}

export default TextInput;
