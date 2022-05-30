import '../../pages/i18n';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import ByTextInput from '../filters/ByTextInput';
import BySelect from '../filters/BySelect';
import Tooltip from '../tooltip';
import MultiList from '../filters/MultiList';
import ByRange from '../filters/ByRange';
import { minYear } from '../../constants/timedate';
import BySelectGroup from '../filters/BySelectGroup';

const SearchFilters = ({
  handleFilterChange,
  handleYearChange,
  searchCriteria,
  handleRegionChange,
  handleClearSearch,
  regions,
  filteredCountries,
  sectors,
  documentTypes,
  instruments,
}) => {
  const [showClear, setShowClear] = useState(false);
  const { t, i18n, ready } = useTranslation('searchResults');

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

  useEffect(() => {
    if (
      searchCriteria.year_range[0] !== minYear &&
      searchCriteria.year_range[1] !== currentYear
    ) {
      setShowClear(true);
    } else if (Object.keys(searchCriteria.keyword_filters).length > 0) {
      setShowClear(true);
    } else {
      setShowClear(false);
    }
  }, [searchCriteria]);

  return (
    <>
      <div className="flex md:justify-between items-center mt-2 md:mt-0">
        <div className="text-indigo-400 font-medium mr-2 md:mr-0">
          {t('Filter by')}
        </div>
        {showClear && (
          <button
            className="underline text-sm text-blue-500 hover:text-indigo-600 transition duration-300"
            onClick={handleClearSearch}
          >
            Clear all filters
          </button>
        )}
      </div>

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
            onChange={handleRegionChange}
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
            list={filteredCountries}
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
          <BySelectGroup
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

        <div className="relative mt-8 mb-12">
          <div className="mx-2">
            <div className="absolute top-0 right-0">
              {/* TODO: translate below text */}
              <Tooltip
                id="year-range"
                tooltip="The years in which documents were first published"
              />
            </div>
            <ByRange
              title={t('By date range')}
              type="year_range"
              handleChange={handleYearChange}
              defaultValues={searchCriteria.year_range}
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
