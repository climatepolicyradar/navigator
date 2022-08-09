interface FormFieldErrorProps {
  message: string;
}

function FormFieldError({ message }: FormFieldErrorProps) {
  return <div className="error w-full text-red-500 mt-1">{message}</div>;
}

export default FormFieldError;
