import React from 'react';
import { FieldErrors, UseFormRegisterReturn } from 'react-hook-form';

interface InputProps {
  label: string;
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
  label,
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
      <label className="text-indigo-600">
        {label}
        {required ? <strong className="text-red-500"> *</strong> : null}
      </label>
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
      {errors[name] && (
        <div className="error w-full text-red-500">{errors[name].message}</div>
      )}
    </div>
  );
};

export default TextInput;
