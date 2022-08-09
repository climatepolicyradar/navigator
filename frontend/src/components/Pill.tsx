interface PillProps {
  text: string;
}

function Pill({ text }: PillProps) {
  return (
    <span className="bg-blue-500 uppercase text-xs font-medium py-2 px-4 text-white rounded-2xl tracking-wider md:tracking-widest">
      {text}
    </span>
  );
}
export default Pill;
