import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  onClick?(event: React.FormEvent<HTMLButtonElement>): void;
  color?: 'dark' | 'light' | 'clear' | 'light-hover-dark';
  id?: string;
  extraClasses?: string;
  'data-cy'?: string;
  fullWidth?: boolean;
  thin?: boolean;
}

const Button = ({
  children,
  type = 'button',
  disabled = false,
  onClick = null,
  color = 'light',
  id,
  extraClasses = '',
  fullWidth = false,
  thin = false,
  ...props
}: ButtonProps) => {
  let colorClasses =
    'bg-indigo-600 text-white border border-indigo-600 hover:bg-white hover:border-white hover:text-indigo-600';
  switch (color) {
    case 'light':
      colorClasses =
        'bg-blue-500 border border-blue-500 text-white hover:bg-white hover:border-white hover:text-indigo-600';
      break;
    case 'light-hover-dark':
      colorClasses =
        'bg-blue-500 border border-blue-500 text-white hover:bg-indigo-600 hover:border-indigo-600 hover:text-white';
      break;
    case 'clear':
      colorClasses = !disabled
        ? 'clear bg-white border border-indigo-600 text-indigo-600 hover:bg-indigo-100 disabled:border-indigo-300 disabled:text-indigo-300 disabled:hover:bg-white'
        : '';
      break;
  }

  return (
    <button
      id={id}
      onClick={onClick}
      type={type}
      disabled={disabled}
      data-cy={props['data-cy']}
      className={`${colorClasses} ${
        thin ? 'py-1' : 'py-3'
      } button transition duration-300 px-4 rounded-3xl md:px-8 pointer-events-auto w-full ${
        disabled
          ? 'pointer-events-none bg-indigo-300 text-indigo-200 border-indigo-300 hover:bg-indigo-300 hover:text-indigo-200 hover:border-indigo-300'
          : ''
      } ${extraClasses} ${!fullWidth ? 'md:w-auto' : ''}`}
      {...props}
    >
      {children}
    </button>
  );
};

export default Button;
