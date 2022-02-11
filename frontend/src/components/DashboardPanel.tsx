import { DocumentsIcon } from './Icons';

interface DashboardPanelProps {
  icon: React.Component;
  number: number;
  text: string;
}

const DashboardPanel = ({ icon, number, text }) => {
  const DashIcon = icon;
  return (
    <div className="mr-8 text-white flex flex-col shrink-0 items-start justify-center p-8 bg-blue-500/25 rounded-3xl text-yellow-500 w-8/12 sm:w-1/2 md:w-full md:mr-0 xl:p-12">
      <DashIcon height="43" width="35" />
      <span className="text-7xl font-medium text-white xl:text-8xl mt-2">
        {number}
      </span>
      <span className="font-medium">{text}</span>
    </div>
  );
};
export default DashboardPanel;
