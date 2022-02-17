import DashboardPanel from './DashboardPanel';
import { DocumentsIcon, JurisdictionsIcon, AddIcon } from './Icons';

const Dashboard = () => {
  return (
    <div className="-mx-8 md:mx-0 pl-8 md:pl-0 w-auto overflow-x-auto no-scrollbar flex no-wrap md:grid md:grid-cols-3 md:gap-8 lg:gap-10 xl:gap-28">
      <DashboardPanel icon={DocumentsIcon} number={1023} text="Documents" />
      <DashboardPanel
        icon={JurisdictionsIcon}
        number={634}
        text="Jurisdictions"
      />
      <DashboardPanel icon={AddIcon} number={10} text="New documents" />
    </div>
  );
};
export default Dashboard;
