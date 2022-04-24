import '../pages/i18n';
import { useTranslation } from 'react-i18next';
import ByTextInput from './filters/ByTextInput';
import useLookups from '../hooks/useLookups';
import BySelect from './filters/BySelect';
import Tooltip from './tooltip';

const SearchFilters = ({ handleFilterChange }) => {
  const { t, i18n, ready } = useTranslation('searchResults');
  const geosQuery = useLookups('geographies');
  const { data: { geographies } = [] } = geosQuery;
  // the 3 lists below may come dynamically from db at some point?
  const regionsList = [
    'All',
    'Africa',
    'East Asia & Pacific',
    'Europe & Central Asia',
    'Latin America & the Caribbean',
    'Middle East & North Africa',
    'South Asia',
  ];
  const sectorList = [
    'All',
    'Adaptation',
    'Buildings',
    'Cross-cutting areas',
    'Economy-wide',
  ];
  const documentTypeList = ['Act', 'Decree', 'Strategy', 'Law', 'Plan'];

  // tooltip descriptions
  const regionTooltip = t('Tooltips.Region');
  const countryTooltip = t('Tooltips.Country');
  const sectorTooltip = t('Tooltips.Sector');
  const doctypeTooltip = t('Tooltips.Document type');

  return (
    <>
      <div className="text-indigo-400 mt-8 font-medium">{t('Filter by')}</div>
      <div className="my-4 text-sm text-indigo-500">
        <div className="relative">
          <div className="absolute top-0 right-0 z-20">
            <Tooltip id="region" tooltip={regionTooltip} />
          </div>

          <BySelect
            list={regionsList}
            onChange={handleFilterChange}
            title={t('By region')}
            type="action_region"
          />
        </div>
        <div className="relative mt-6">
          <div className="absolute top-0 right-0 z-10">
            <Tooltip id="country" tooltip={countryTooltip} />
          </div>
          <ByTextInput
            title={t('By country')}
            list={geographies}
            keyField="english_shortname"
            type="action_geography_english_shortname"
            handleFilterChange={handleFilterChange}
          />
        </div>
        <div className="relative mt-6">
          <div className="absolute top-0 right-0 z-10">
            <Tooltip id="sector" tooltip={sectorTooltip} />
          </div>
          <BySelect
            list={sectorList}
            onChange={handleFilterChange}
            title={t('By sector')}
            type="action_sector"
          />
        </div>
        <div className="relative mt-6">
          <div className="absolute top-0 right-0 z-10">
            <Tooltip id="doctype" tooltip={doctypeTooltip} />
          </div>
          <BySelect
            list={documentTypeList}
            onChange={handleFilterChange}
            title={t('By document type')}
            type="action_document_type"
          />
        </div>
      </div>
    </>
  );
};
export default SearchFilters;
