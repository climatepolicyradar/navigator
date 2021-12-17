const Button = ({ children, onClick }) => {
  return (
    <button onClick={onClick} className="bg-gray-300 p-4 rounded">
      {children}
    </button>
  );
};

export default Button;
