import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  onClick?(event: React.FormEvent<HTMLButtonElement>): void;
  color?: 'dark' | 'light' | 'clear';
  id?: string;
  extraClasses?: string;
  'data-cy'?: string;
}

const Button = ({
  children,
  type = 'button',
  disabled = false,
  onClick = null,
  color = 'light',
  id = '',
  extraClasses = '',
  ...props
}: ButtonProps) => {
  let colorClasses =
    'bg-indigo-600 text-white border border-indigo-600 hover:bg-white hover:border-white hover:text-indigo-600';
  switch (color) {
    case 'light':
      colorClasses =
        'bg-blue-500 border border-blue-500 text-white hover:bg-white hover:border-white hover:text-indigo-600';
      break;
    case 'clear':
      colorClasses =
        'clear bg-white border border-indigo-600 text-indigo-600 hover:bg-indigo-100';
      break;
  }
  return (
    <button
      onClick={onClick}
      type={type}
      disabled={disabled}
      id={id}
      data-cy={props['data-cy']}
      className={`${colorClasses} button transition duration-300 px-4 py-2 rounded-3xl w-full md:w-auto md:px-8 pointer-events-auto ${extraClasses}`}
    >
      {children}
    </button>
  );
};

export default Button;
