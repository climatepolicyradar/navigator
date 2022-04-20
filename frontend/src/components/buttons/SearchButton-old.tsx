const SearchButton = ({ children }) => {
  return (
    <button
      type="submit"
      className="bg-indigo-600 text-white uppercase p-2 rounded-full hover:bg-blue-500 transtion duration-300 w-16 md:w-24 shrink-0 font-medium"
    >
      {children}
    </button>
  );
};

export default SearchButton;
