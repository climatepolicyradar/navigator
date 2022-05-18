import '../pages/i18n';
import { useTranslation } from 'react-i18next';
import ByTextInput from './filters/ByTextInput';
import useLookups from '../hooks/useLookups';
import BySelect from './filters/BySelect';
import Tooltip from './tooltip';
import MultiList from './filters/MultiList';
import ByRange from './filters/ByRange';
import { minYear } from '../constants/timedate';
import useGeographies from '../hooks/useGeographies';
import useRegions from '../hooks/useRegions';

const SearchFilters = ({
  handleFilterChange,
  handleYearChange,
  searchCriteria,
}) => {
  const { t, i18n, ready } = useTranslation('searchResults');
  const { geosQuery, geographies } = useGeographies();
  const { regionsQuery, regions } = useRegions();
  const sectorsQuery = useLookups('sectors');
  const {
    keyword_filters: { countries: geoFilters = [] },
  } = searchCriteria;
  // the 3 lists below may come dynamically from db at some point?

  const sectorList = [
    'All',
    'Adaptation',
    'Buildings',
    'Cross-cutting areas',
    'Economy-wide',
  ];
  const documentTypeList = ['All', 'Act', 'Decree', 'Strategy', 'Law', 'Plan'];
  const instrumentList = ['All', 'Tax incentive', 'Something else'];

  const now = new Date();
  const currentYear = now.getFullYear();

  // tooltip descriptions
  const regionTooltip = t('Tooltips.Region');
  const countryTooltip = t('Tooltips.Country');
  const sectorTooltip = t('Tooltips.Sector');
  const doctypeTooltip = t('Tooltips.Document type');
  const instrumentTooltip = t('Tooltips.Instrument');

  return (
    <>
      {console.log(sectorsQuery.data)}
      <div className="text-indigo-400 font-medium">{t('Filter by')}</div>
      <div className="my-4 text-sm text-indigo-500">
        <div className="relative">
          <div className="absolute top-0 right-0 z-20">
            <Tooltip id="region" tooltip={regionTooltip} />
          </div>

          <BySelect
            list={regions}
            defaultValue={
              searchCriteria.keyword_filters?.region
                ? searchCriteria.keyword_filters.region[0]
                : ''
            }
            onChange={handleFilterChange}
            title={t('By region')}
            keyField="display_value"
            filterType="regions"
          />
        </div>
        <div className="relative mt-6">
          <div className="absolute top-0 right-0 z-20">
            <Tooltip id="country" tooltip={countryTooltip} />
          </div>
          <ByTextInput
            title={t('By country')}
            list={geographies}
            selectedList={geoFilters}
            keyField="display_value"
            filterType="countries"
            handleFilterChange={handleFilterChange}
          />
          <MultiList
            list={geoFilters}
            removeFilter={handleFilterChange}
            type="countries"
          />
        </div>
        <div className="relative mt-6">
          <div className="absolute top-0 right-0 z-20">
            <Tooltip id="sector" tooltip={sectorTooltip} />
          </div>
          {/* <BySelect
            list={sectorList}
            onChange={handleFilterChange}
            defaultValue={
              searchCriteria.keyword_filters?.action_sector
                ? searchCriteria.keyword_filters.action_sector[0]
                : ''
            }
            title={t('By sector')}
            type="action_sector"
          /> */}
        </div>
        <div className="relative mt-6">
          <div className="absolute top-0 right-0 z-20">
            <Tooltip id="doctype" tooltip={doctypeTooltip} />
          </div>
          {/* <BySelect
            list={documentTypeList}
            onChange={handleFilterChange}
            defaultValue={
              searchCriteria.keyword_filters?.action_document_type
                ? searchCriteria.keyword_filters.action_document_type[0]
                : ''
            }
            title={t('By document type')}
            type="action_document_type"
          /> */}
        </div>
        <div className="relative mt-6">
          <div className="absolute top-0 right-0 z-20">
            <Tooltip id="instrument" tooltip={instrumentTooltip} />
          </div>
          {/* <BySelect
            list={instrumentList}
            onChange={handleFilterChange}
            defaultValue={
              searchCriteria.keyword_filters?.action_instrument
                ? searchCriteria.keyword_filters.action_instrument[0]
                : ''
            }
            title={t('By instrument')}
            type="action_instrument"
          /> */}
        </div>
        <div className="relative mt-6">
          <div className="mx-2">
            <ByRange
              title={t('By date range')}
              type="year_range"
              handleChange={handleYearChange}
              defaultValues={
                searchCriteria.year_range ? searchCriteria.year_range : ''
              }
              min={minYear}
              max={currentYear}
            />
          </div>
        </div>
      </div>
    </>
  );
};
export default SearchFilters;
