import DashboardPanel from './DashboardPanel';
import { DocumentsIcon, JurisdictionsIcon, AddIcon } from '../Icons';

interface DashboardProps {
  terms: string[];
}

const Dashboard = ({ terms }: DashboardProps) => {
  return (
    <div
      data-cy="dashboard"
      className="-mx-8 md:mx-0 pl-8 md:pl-0 w-auto overflow-x-auto no-scrollbar flex no-wrap md:grid md:grid-cols-3 md:gap-8 lg:gap-10 xl:gap-28"
    >
      <DashboardPanel icon={DocumentsIcon} number={1023} text={terms[0]} />
      <DashboardPanel icon={JurisdictionsIcon} number={634} text={terms[1]} />
      <DashboardPanel icon={AddIcon} number={10} text={terms[2]} />
    </div>
  );
};
export default Dashboard;
