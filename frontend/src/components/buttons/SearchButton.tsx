const SearchButton = ({ children }) => {
  return (
    <button className="bg-indigo-600 text-white uppercase p-2 rounded-full hover:bg-blue-500 transtion duration-300 w-24 font-medium">
      {children}
    </button>
  );
};

export default SearchButton;
