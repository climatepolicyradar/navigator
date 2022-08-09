import React, { useEffect, useState } from 'react';
import Link from 'next/link';
import { useTranslation } from 'react-i18next';
import { currentYear, minYear } from '@constants/timedate';
import { TSector } from '@types';
import ByTextInput from '../filters/ByTextInput';
import BySelect from '../filters/BySelect';
import MultiList from '../filters/MultiList';
import ExactMatch from '../filters/ExactMatch';
import ByDateRange from '../filters/ByDateRange';

interface SearchFiltersProps {
  handleFilterChange(type: string, value: string, action?: string): void;
  handleYearChange(values: number[]): void;
  handleRegionChange(type: any, regionName: any): void;
  handleClearSearch(): void;
  handleSearchChange(type: string, value: string): void;
  searchCriteria: any;
  regions: object[];
  filteredCountries: object[];
  sectors: TSector[];
  documentTypes: object[];
  instruments: object[];
}

const SearchFilters: React.FC<SearchFiltersProps> = React.memo(
  ({
    handleFilterChange,
    handleYearChange,
    searchCriteria,
    handleRegionChange,
    handleClearSearch,
    handleSearchChange,
    regions,
    filteredCountries,
    sectors,
  }) => {
    const [showClear, setShowClear] = useState(false);
    const { t } = useTranslation('searchResults');

    const {
      keyword_filters: {
        countries: countryFilters = [],
        sectors: sectorFilters = [],
      },
    } = searchCriteria;

    const thisYear = currentYear();

    useEffect(() => {
      if (
        searchCriteria.year_range[0] !== minYear
        && searchCriteria.year_range[1] !== thisYear
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
          <div>
            <ExactMatch
              checked={searchCriteria.exact_match}
              id="exact-match"
              handleSearchChange={handleSearchChange}
            />
          </div>
          <div className="relative mt-6">
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
            <BySelect
              list={sectors.filter(
                (sector) => !sectorFilters.includes(sector.name)
              )}
              onChange={handleFilterChange}
              title={t('By sector')}
              keyField="name"
              filterType="sectors"
              defaultValue=""
              defaultText={sectorFilters.length ? 'Add more sectors' : 'All'}
            />
            <MultiList
              list={sectorFilters}
              removeFilter={handleFilterChange}
              type="sectors"
            />
          </div>
          <div className="relative mt-8 mb-12">
            <div className="">
              <ByDateRange
                title={t('By date range')}
                type="year_range"
                handleChange={handleYearChange}
                defaultValues={searchCriteria.year_range}
                min={minYear}
                max={thisYear}
                clear={showClear}
              />
            </div>
          </div>
          <div className="my-8 pt-8 border-t border-blue-200">
            <p className="text-center">
              For more info see
              <br />
              <Link href="/methodology">
                <a className="underline text-blue-600">our methodology page</a>
              </Link>
            </p>
          </div>
        </div>
      </>
    );
  }
);
export default SearchFilters;
