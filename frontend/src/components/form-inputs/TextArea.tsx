import React from 'react';
import { useField } from 'formik';

interface TextAreaProps {
  id?: string;
  name: string;
  label: string;
  type: string;
  classes?: string;
  required?: boolean;
}

// const TextArea = ({
//   label,
//   required = false,
//   classes = '',
//   ...props
// }: TextAreaProps) => {
//   // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
//   // which we can spread on <input>. We can use field meta to show an error
//   // message if the field is invalid and it has been touched (i.e. visited)
//   const [field, meta] = useField(props);

//   return (
//     <div className={`${classes}`}>
//       <label htmlFor={props.id || props.name} className="text-indigo-600">
//         {label}
//         {required ? <strong className="text-red-500"> *</strong> : null}
//       </label>
//       <textarea
//         className={`${
//           meta.touched && meta.error ? 'border-red-500' : 'border-gray-300'
//         }`}
//         type={props.type}
//         {...field}
//         {...props}
//       />
//       {meta.touched && meta.error ? (
//         <div className="error">{meta.error}</div>
//       ) : null}
//     </div>
//   );
// };

const TextArea = ({
  id = '',
  name,
  label,
  register,
  required = false,
  placeholder = '',
  errors,
  classes = '',
  ...props
}) => {
  return (
    <div className={`${classes}`}>
      <label htmlFor={id} className="text-indigo-600">
        {label}
        {required ? <strong className="text-red-500"> *</strong> : null}
      </label>
      <textarea
        {...register(name)}
        className={`border ${
          errors[name] ? 'border-red-500' : 'border-gray-300'
        }`}
      />
      {errors[name] && (
        <div className="error w-full text-red-500">{errors[name].message}</div>
      )}
    </div>
  );
};

export default TextArea;
