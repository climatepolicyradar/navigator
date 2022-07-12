import React from 'react';
import { FieldErrors, UseFormRegisterReturn } from 'react-hook-form';

interface CheckboxProps {
  id?: string;
  name: string;
  label: string;
  required?: boolean;
  value: string;
  errors: {};
  onClick?(event: any): any;
  register: any;
  // checked: boolean;
}

const Checkbox = ({
  id,
  label,
  name,
  required = false,
  value,
  errors,
  register,
  // checked,
  onClick = () => {},
}: CheckboxProps) => {
  return (
    <div>
      <label className="checkbox-input" htmlFor={id}>
        <input
          className="text-white border-blue-500 rounded"
          id={id}
          type="checkbox"
          value={value}
          {...register(name)}
          // ref={register(name)}
          // checked={checked}
          onClick={onClick}
        />
        <span className="pl-2">{label}</span>
      </label>
    </div>
  );
};

export default Checkbox;
