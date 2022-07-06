import React from "react";
import { FieldErrors } from "react-hook-form";
import FormFieldError from "../blocks/Error";

interface SelectProps {
  id?: string;
  name: string;
  label?: string;
  children: React.ReactNode;
  classes?: string;
  required?: boolean;
  errors: {};
  onChange?(event: any): any;
  register: any;
  "data-cy"?: string;
  multiple?: boolean;
}

const Select = ({ id, label = "", name, children, required = false, classes = "", onChange = () => {}, errors, register, "data-cy": dataCy, multiple = false }: SelectProps) => {
  return (
    <div className={`${classes}`}>
      <label htmlFor={id}>
        {label}
        {required && label ? <strong className="text-red-500"> *</strong> : null}
      </label>
      <div className="mt-1">
        <select
          selected
          multiple={multiple}
          data-cy={dataCy}
          className={`border ${errors[name] ? "border-red-500" : "border-gray-300"}`}
          {...register(name, { onChange: onChange })}
        >
          {children}
        </select>
      </div>

      {errors[name] ? <FormFieldError message={errors[name].message} /> : null}
    </div>
  );
};

export default Select;
