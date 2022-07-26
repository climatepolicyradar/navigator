import ReactTooltip from "react-tooltip";
interface TooltipProps {
  id: string;
  tooltip: string;
  icon?: "?" | "!" | "i";
}

const Tooltip = ({ id, tooltip, icon = "?" }: TooltipProps) => {
  return (
    <div>
      <button data-tip="React-tooltip" data-for={id} className="circle-sm rounded-full bg-blue-600 text-white flex justify-center items-center text-sm font-light">
        {icon}
      </button>
      <ReactTooltip className="customTooltip" getContent={(dataTip) => tooltip} id={id} />
    </div>
  );
};
export default Tooltip;
