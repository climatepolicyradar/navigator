import ReactTooltip from "react-tooltip";

interface TooltipProps {
  id: string;
  tooltip: string | React.ReactNode;
  icon?: "?" | "!" | "i";
  place?: "top" | "right" | "bottom" | "left";
}

const Tooltip = ({ id, tooltip, icon = "?", place }: TooltipProps) => {
  return (
    <div>
      <button data-tip="React-tooltip" data-for={id} className="circle-sm rounded-full bg-blue-600 text-white flex justify-center items-center text-sm font-light">
        {icon}
      </button>
      <ReactTooltip className="customTooltip" id={id} type="light" place={place}>
        {tooltip}
      </ReactTooltip>
    </div>
  );
};
export default Tooltip;
