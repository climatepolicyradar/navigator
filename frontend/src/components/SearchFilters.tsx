import '../pages/i18n';
import { useTranslation } from 'react-i18next';
import ByTextInput from './filters/ByTextInput';
import BySelect from './filters/BySelect';
import Tooltip from './tooltip';
import MultiList from './filters/MultiList';
import ByRange from './filters/ByRange';
import { minYear } from '../constants/timedate';
import useLookups from '../hooks/useLookups';
import useNestedLookups from '../hooks/useNestedLookups';
import Loader from './Loader';

const SearchFilters = ({
  handleFilterChange,
  handleYearChange,
  searchCriteria,
}) => {
  const { t, i18n, ready } = useTranslation('searchResults');
  const {
    nestedLookupsQuery: geosQuery,
    level1: regions,
    level2: countries,
  } = useNestedLookups('geographies', '', 2);
  const { nestedLookupsQuery: sectorsQuery, level1: sectors } =
    useNestedLookups('sectors', 'name');
  const { lookupsQuery: documentTypesQuery, list: documentTypes } =
    useLookups('document_types');
  const { nestedLookupsQuery: instrumentsQuery, level1: instruments } =
    useNestedLookups('instruments', 'name');

  const {
    keyword_filters: { countries: countryFilters = [] },
  } = searchCriteria;

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
      {geosQuery.isFetching ||
      sectorsQuery.isFetching ||
      documentTypesQuery.isFetching ||
      instrumentsQuery.isFetching ? (
        <div className="flex w-full justify-center">
          <Loader />
        </div>
      ) : (
        <>
          <div className="text-indigo-400 font-medium">{t('Filter by')}</div>
          <div className="my-4 text-sm text-indigo-500">
            <div className="relative">
              <div className="absolute top-0 right-0 z-20">
                <Tooltip id="region" tooltip={regionTooltip} />
              </div>

              <BySelect
                list={regions}
                defaultValue={
                  searchCriteria.keyword_filters?.regions
                    ? searchCriteria.keyword_filters.regions[0]
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
                list={countries}
                selectedList={countryFilters}
                keyField="display_value"
                filterType="countries"
                handleFilterChange={handleFilterChange}
              />
              <MultiList
                list={countryFilters}
                removeFilter={handleFilterChange}
                type="countries"
              />
            </div>
            <div className="relative mt-6">
              <div className="absolute top-0 right-0 z-20">
                <Tooltip id="sector" tooltip={sectorTooltip} />
              </div>
              <BySelect
                list={sectors}
                onChange={handleFilterChange}
                defaultValue={
                  searchCriteria.keyword_filters?.sectors
                    ? searchCriteria.keyword_filters.sectors[0]
                    : ''
                }
                title={t('By sector')}
                keyField="name"
                filterType="sectors"
              />
            </div>
            <div className="relative mt-6">
              <div className="absolute top-0 right-0 z-20">
                <Tooltip id="doctype" tooltip={doctypeTooltip} />
              </div>
              <BySelect
                list={documentTypes}
                onChange={handleFilterChange}
                defaultValue={
                  searchCriteria.keyword_filters?.types
                    ? searchCriteria.keyword_filters.types[0]
                    : ''
                }
                title={t('By document type')}
                keyField="name"
                filterType="types"
              />
            </div>
            <div className="relative mt-6">
              <div className="absolute top-0 right-0 z-20">
                <Tooltip id="instrument" tooltip={instrumentTooltip} />
              </div>
              <BySelect
                list={instruments}
                onChange={handleFilterChange}
                defaultValue={
                  searchCriteria.keyword_filters?.instruments
                    ? searchCriteria.keyword_filters.instruments[0]
                    : ''
                }
                title={t('By instrument')}
                keyField="name"
                filterType="instruments"
              />
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
      )}
    </>
  );
};
export default SearchFilters;
