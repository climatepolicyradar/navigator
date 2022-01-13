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
  let colorClasses = 'bg-gray-800 text-white border border-gray-800';
  switch (color) {
    case 'light':
      colorClasses = 'bg-gray-300 border border-gray-300';
      break;
    case 'clear':
      colorClasses = 'bg-white border border-gray-500';
      break;
  }
  return (
    <button
      onClick={onClick}
      type={type}
      disabled={disabled}
      id={id}
      data-cy={props['data-cy']}
      className={`${colorClasses} px-4 py-2 rounded w-full md:w-auto md:px-8 pointer-events-auto ${extraClasses}`}
    >
      {children}
    </button>
  );
};

export default Button;
