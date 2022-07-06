import React, { useState } from "react";
import { FieldErrors } from "react-hook-form";
import FormFieldError from "../blocks/Error";
import { EyeIcon } from "@components/svg/Icons";

interface InputProps {
  label?: string;
  required?: boolean;
  errors: FieldErrors;
  name: string;
  placeholder?: string;
  className?: string;
  onChange?(event: any): any;
  register: any;
}

const PasswordInput = ({ label = "", required = false, errors, name, placeholder = "", className = "", onChange, register }: InputProps): JSX.Element => {
  const [passwordReveal, setPasswordReveal] = useState(false);

  const handleOnClick = () => {
    setPasswordReveal(!passwordReveal);
  };

  return (
    <div className={className}>
      <label className="">
        {label}
        {required && label ? <strong className="text-red-500"> *</strong> : null}
      </label>
      <div className="relative mt-1">
        <input
          type={passwordReveal ? "text" : "password"}
          placeholder={placeholder}
          className={`border ${errors[name] ? "border-red-500" : "border-gray-300"}`}
          onChange={onChange}
          {...register(name)}
        />
        <div
          className={`absolute inset-y-0 right-5 flex items-center cursor-pointer 
            ${passwordReveal ? "text-blue-500" : "text-black"}`}
          onClick={handleOnClick}
          title={`${passwordReveal ? "Hide" : "Show"} password`}
        >
          <EyeIcon height="24" width="24" />
        </div>
      </div>
      {errors[name] && <FormFieldError message={errors[name].message} />}
    </div>
  );
};

export default PasswordInput;
