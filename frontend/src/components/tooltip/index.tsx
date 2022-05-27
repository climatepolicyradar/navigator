import ReactTooltip from 'react-tooltip';
interface TooltipProps {
  id: string;
  tooltip: string;
}

const Tooltip = ({ id, tooltip }: TooltipProps) => {
  return (
    <div>
      <button
        data-tip="React-tooltip"
        data-for={id}
        className="circle-sm rounded-full bg-blue-400 text-white flex justify-center items-center text-sm"
      >
        ?
      </button>
      <ReactTooltip
        className="customTooltip"
        getContent={(dataTip) => tooltip}
        id={id}
      />
    </div>
  );
};
export default Tooltip;
