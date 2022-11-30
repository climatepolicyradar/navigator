import Link from "next/link";

const TextLink = ({ children, href = null, onClick = () => {}, target = "_self" }) => {
  return <>
    {href ? (
      (<Link
        href={href}
        target={target}
        className="text-blue-500 underline text-sm text-left mt-2 hover:text-indigo-600 transition duration-300">

        {children}

      </Link>)
    ) : (
      <button className="text-blue-500 underline text-sm text-left mt-2 hover:text-indigo-600 transition duration-300" onClick={onClick}>
        {children}
      </button>
    )}
  </>;
};
export default TextLink;
