import React from 'react';
import { useField } from 'formik';
import { Path, useForm, UseFormRegister, SubmitHandler } from 'react-hook-form';
import { getStaticProps } from '../../pages/users';

// interface TextInputProps {
//   id?: string;
//   name: string;
//   // label: string;
//   // type: string;
//   // required?: boolean;
//   // placeholder?: string;
// }
// type InputProps = {
//   label: Path<TextInputProps>;
//   register: UseFormRegister<TextInputProps>;
//   required: boolean;
//   placeholder: string;
// };
const TextInput = ({
  id = '',
  name,
  label,
  register,
  placeholder = '',
  errors,
  type = 'text',
  required = false,
  onChange = () => {},
}) => {
  return (
    <div>
      <label htmlFor={id} className="text-indigo-600">
        {label}
        {required ? <strong className="text-red-500"> *</strong> : null}
      </label>
      <input
        type={type}
        {...register(name)}
        className={`border ${
          errors[name] ? 'border-red-500' : 'border-gray-300'
        }`}
        onChange={onChange}
        placeholder={placeholder}
      />
      {errors[name] && (
        <div className="error w-full text-red-500">{errors[name].message}</div>
      )}
    </div>
  );
};

// const TextInput = ({
//   label,
//   required = false,
//   placeholder = '',
//   ...props
// }: TextInputProps) => {
//   // useField() returns [formik.getFieldProps(), formik.getFieldMeta()]
//   // which we can spread on <input>. We can use field meta to show an error
//   // message if the field is invalid and it has been touched (i.e. visited)
//   const [field, meta] = useField(props);

//   return (
//     <div>
//       <label htmlFor={props.id || props.name} className="text-indigo-600">
//         {label}
//         {required ? <strong className="text-red-500"> *</strong> : null}
//       </label>
//       <input
//         className={`w-full ${
//           meta.touched && meta.error ? 'border-red-500' : 'border-gray-300'
//         }`}
//         type={props.type}
//         placeholder={placeholder}
//         {...field}
//         {...props}
//       />
//       {meta.touched && meta.error ? (
//         <div className="error w-full text-red-500">{meta.error}</div>
//       ) : null}
//     </div>
//   );
// };

export default TextInput;
