import Link from 'next/link';

const BackLink = ({ text, href = null, onClick = () => {} }) => {
  return (
    <>
      {href ? (
        <Link href={href}>
          <a className="text-blue-500 underline text-sm text-left mt-2 hover:text-indigo-600 transition duration-300">
            <span className="text-lg">&laquo;</span> {text}
          </a>
        </Link>
      ) : (
        <button
          className="ml-6 text-blue-500 underline text-sm text-left mt-2 hover:text-indigo-600 transition duration-300"
          onClick={onClick}
        >
          <span className="text-lg">&laquo;</span> {text}
        </button>
      )}
    </>
  );
};
export default BackLink;
