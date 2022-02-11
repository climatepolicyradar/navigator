interface ProductNameProps {
  fixed: boolean;
}

const ProductName = ({ fixed }: ProductNameProps) => {
  return (
    <div data-cy="product-name" className="flex items-start -mt-1">
      <h1
        className={`${
          fixed
            ? 'text-indigo-600 text-2xl md:text-3xl lg:text-4xl'
            : 'text-white text-3xl md:text-4xl mt-4 md:mt-0 lg:text-h1 lg:leading-none'
        } text-white transition-all duration-300`}
      >
        Navigator
      </h1>
      <span
        data-cy="alpha"
        className={`${
          fixed ? 'mt-1 md:mt-2 lg:mt-3' : 'mt-6 md:mt-3 lg:mt-4'
        } bg-yellow-500 ml-2 text-xs text-indigo-600 px-1 rounded`}
      >
        alpha
      </span>
    </div>
  );
};
export default ProductName;
