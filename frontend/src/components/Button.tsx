import React from 'react';

interface ButtonProps {
  children: React.ReactNode;
  type?: 'button' | 'submit' | 'reset';
  disabled?: boolean;
  onClick?(event: React.FormEvent<HTMLButtonElement>): void;
}

const Button = ({
  children,
  type = 'button',
  disabled = false,
  onClick = null,
}: ButtonProps) => {
  return (
    <button
      onClick={onClick}
      type={type}
      disabled={disabled}
      className="bg-gray-300 p-4 rounded"
    >
      {children}
    </button>
  );
};

export default Button;
