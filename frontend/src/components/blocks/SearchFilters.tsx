import React, { useEffect, useState } from "react";
import Link from "next/link";
import { useTranslation } from "react-i18next";
import ByTextInput from "../filters/ByTextInput";
import BySelect from "../filters/BySelect";
import MultiList from "../filters/MultiList";
import ByRange from "../filters/ByRange";
import BySelectGroup from "../filters/BySelectGroup";
import ExactMatch from "../filters/ExactMatch";
import { minYear, currentYear } from "../../constants/timedate";
import { TSector } from "../../interfaces";

interface SearchFiltersProps {
  handleFilterChange(type: string, value: string, action: string): void;
  handleYearChange(values: any): void;
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

const SearchFilters = ({
  handleFilterChange,
  handleYearChange,
  searchCriteria,
  handleRegionChange,
  handleClearSearch,
  handleSearchChange,
  regions,
  filteredCountries,
  sectors,
}: SearchFiltersProps) => {
  const [showClear, setShowClear] = useState(false);
  const { t } = useTranslation("searchResults");
  const yearNow = currentYear();

  const {
    keyword_filters: { countries: countryFilters = [], sectors: sectorFilters = [] },
  } = searchCriteria;

  useEffect(() => {
    if (searchCriteria.year_range[0] !== minYear && searchCriteria.year_range[1] !== yearNow) {
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
        <div className="text-indigo-400 font-medium mr-2 md:mr-0">{t("Filter by")}</div>
        {showClear && (
          <button className="underline text-sm text-blue-500 hover:text-indigo-600 transition duration-300" onClick={handleClearSearch}>
            Clear all filters
          </button>
        )}
      </div>

      <div className="my-4 text-sm text-indigo-500">
        <div>
          <ExactMatch checked={searchCriteria.exact_match} id="exact-match" handleSearchChange={handleSearchChange} />
        </div>
        <div className="relative mt-6">
          <BySelect
            list={regions}
            defaultValue={searchCriteria.keyword_filters?.regions ? searchCriteria.keyword_filters.regions[0] : ""}
            onChange={handleRegionChange}
            title={t("By region")}
            keyField="display_value"
            filterType="regions"
          />
        </div>
        <div className="relative mt-6">
          <ByTextInput
            title={t("By country")}
            list={filteredCountries}
            selectedList={countryFilters}
            keyField="display_value"
            filterType="countries"
            handleFilterChange={handleFilterChange}
          />
          <MultiList list={countryFilters} removeFilter={handleFilterChange} type="countries" />
        </div>
        <div className="relative mt-6">
          <BySelect
            list={sectors.filter((s) => !sectorFilters.includes(s.name))}
            onChange={handleFilterChange}
            title={t("By sector")}
            keyField="name"
            filterType="sectors"
            defaultText="Add sectors"
          />
          <MultiList list={sectorFilters} removeFilter={handleFilterChange} type="sectors" />
          {/* <input list="ice-cream-flavors" id="ice-cream-choice" name="ice-cream-choice" placeholder="Select an ice cream" />
          <datalist id="ice-cream-flavors">
              <option value="Chocolate" />
              <option value="Coconut" />
              <option value="Mint" />
              <option value="Strawberry" />
              <option value="Vanilla" />
          </datalist> */}
        </div>
        <div className="relative mt-8 mb-12">
          <div className="mx-2">
            <ByRange title={t("By date range")} type="year_range" handleChange={handleYearChange} defaultValues={searchCriteria.year_range} min={minYear} max={yearNow} />
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
};
export default SearchFilters;
