import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  onClick?(event: React.FormEvent<HTMLButtonElement>): void;
  color?: 'dark' | 'light';
}

const Button = ({
  children,
  type = 'button',
  disabled = false,
  onClick = null,
  color = 'light',
}: ButtonProps) => {
  return (
    <button
      onClick={onClick}
      type={type}
      disabled={disabled}
      className={`${
        color === 'light' ? 'bg-gray-300' : 'bg-gray-800 text-white'
      } px-4 py-2 rounded w-full md:w-auto md:px-8`}
    >
      {children}
    </button>
  );
};

export default Button;
