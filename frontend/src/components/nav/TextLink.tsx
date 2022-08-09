import Link from 'next/link';

function TextLink({
  children,
  href = null,
  onClick = () => {},
  target = '_self',
}) {
  return (
    <>
      {href ? (
        <Link href={href}>
          <a
            target={target}
            className="text-blue-500 underline text-sm text-left mt-2 hover:text-indigo-600 transition duration-300"
          >
            {children}
          </a>
        </Link>
      ) : (
        <button
          className="ml-6 text-blue-500 underline text-sm text-left mt-2 hover:text-indigo-600 transition duration-300"
          onClick={onClick}
        >
          {children}
        </button>
      )}
    </>
  );
}
export default TextLink;
