import React from 'react';
import { useField } from 'formik';

interface SelectProps {
  id?: string;
  name: string;
  label: string;
  children: React.ReactNode;
  onChange?(e: any): void;
}

const Select = React.forwardRef(
  (
    { label, children, onChange = () => {}, ...props }: SelectProps,
    ref: any
  ) => {
    const [field, meta] = useField(props);
    return (
      <div>
        <label htmlFor={props.id || props.name}>{label}</label>
        <select
          {...field}
          {...props}
          onChange={onChange}
          ref={ref}
          className="border border-gray-300 rounded p-2 text-lg"
        >
          {children}
        </select>

        {meta.touched && meta.error ? (
          <div className="error">{meta.error}</div>
        ) : null}
      </div>
    );
  }
);

Select.displayName = 'Select';

export default Select;
