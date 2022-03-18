import { useState, useEffect } from 'react';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useForm } from 'react-hook-form';
import Button from '../buttons/Button';
import TextInput from '../form-inputs/TextInput';
import TextArea from '../form-inputs/TextArea';
import { months, yearRange, daysInMonth } from '../../constants/timedate';
import Select from '../form-inputs/Select';
import Overlay from '../Overlay';
import Popup from '../modals/Popup';
import AddDocument from './AddDocument';
import {
  Document,
  Action,
  Geography,
  Language,
  ActionType,
  Source,
} from '../../interfaces';
import LoaderOverlay from '../LoaderOverlay';
import '../../pages/i18n';
import { useTranslation } from 'react-i18next';
import useCreateAction from '../../hooks/useCreateAction';
import DocumentList from './DocumentList';

interface AddActionProps {
  geographies: Geography[];
  languages: Language[];
  actionTypes: ActionType[];
  sources: Source[];
}

const AddAction = ({
  geographies,
  languages,
  actionTypes,
  sources,
}: AddActionProps) => {
  const [days, setDays] = useState([]);
  const [popupActive, setPopupActive] = useState(false);
  const initialValues = {
    action_source_id: '',
    name: '',
    description: '',
    year: '',
    month: '',
    day: '',
    geography_id: '',
    action_type_id: '',
    documents: [],
  };
  const createAction = useCreateAction();

  const yearSelections = yearRange();
  const { t, i18n, ready } = useTranslation([
    'addAction',
    'formErrors',
    'common',
  ]);

  const schema = Yup.object({
    action_source_id: Yup.string().required(
      t('addAction.Please select a source.', { ns: 'formErrors' })
    ),
    name: Yup.string().required(t('Required', { ns: 'formErrors' })),
    year: Yup.string().required(t('Year', { ns: 'formErrors' })),
    geography_id: Yup.string().required(
      t('addAction.Please select a geography.', { ns: 'formErrors' })
    ),
    action_type_id: Yup.string().required(
      t('addAction.Please select an action type.', {
        ns: 'formErrors',
      })
    ),
    documents: Yup.array().min(
      1,
      t('addAction.You must add at least one document.', {
        ns: 'formErrors',
      })
    ),
  });

  const {
    register,
    handleSubmit,
    getValues,
    formState: { isSubmitting },
    formState: { errors },
    formState: { isSubmitSuccessful },
    reset,
    watch,
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: initialValues,
  });
  const values = watch();
  const documents = watch('documents');

  const handleDateChange = (e) => {
    const values = getValues();
    const today = new Date();
    const thisYear = today.getFullYear();
    let year = values.year ? values.year : thisYear;
    let month = values.month ? values.month : 1;

    if (e.target.name === 'year') {
      year = e.target.value;
    }
    if (e.target.name === 'month') {
      month = e.target.value;
    }
    // change available days in month
    const totalDays = daysInMonth(month, year);
    setDays(Array.from(Array(totalDays).keys()));
  };

  const processValues = (values) => {
    // React complains when using null values in form fields, so must do all of the below
    // to convert empty values to 1 or null before sending to api

    // unable to send null values for month and day, generates backend error
    if (values.month.length === 0) {
      values.month = 1;
    }
    if (values.day.length === 0) {
      values.day = 1;
    }
    values.documents.forEach((document) => {
      if (document.month.length === 0) {
        document.month = 1;
      }
      if (document.day.length === 0) {
        document.day = 1;
      }
      // need to send null values instead of empty strings otherwise generates backend error
      if (document.source_url.length === 0) {
        document.source_url = null;
      }
      if (document.s3_url?.length === 0) {
        document.s3_url = null;
      }
    });
  };

  const submitForm = (values, resetForm) => {
    processValues(values);
    createAction.mutate(values);
  };

  useEffect(() => {
    setDays(Array.from(Array(31).keys()));
  }, []);

  useEffect(() => {
    reset();
  }, [isSubmitSuccessful]);

  return (
    <>
      {console.log(values)}
      {createAction.isLoading || !ready ? (
        <>
          <LoaderOverlay />
        </>
      ) : null}
      <Overlay
        active={popupActive}
        onClick={() => {
          setPopupActive(false);
        }}
      />
      {ready && (
        <div className="text-lg">
          {createAction.isError ? (
            <p
              data-cy="message"
              className="mt-4 font-bold text-xl text-red-500"
            >
              {t('form.There was an error, please try again later.')}
            </p>
          ) : createAction.isSuccess ? (
            <p
              data-cy="message"
              className="mt-4 font-bold text-xl text-green-500"
            >
              {t('form.Action successfully added!')}
            </p>
          ) : (
            <p className="text-indigo-600 text-xl">
              {t(
                'Add a new action using the form below. Multiple documents can be added to an action.'
              )}
            </p>
          )}
          <Popup
            active={popupActive}
            onClick={() => {
              setPopupActive(false);
            }}
          >
            {popupActive && (
              <AddDocument
                setPopupActive={setPopupActive}
                days={days}
                handleDateChange={handleDateChange}
                yearSelections={yearSelections}
                // year={values.year}
                // month={values.month}
                // day={values.day}
                languages={languages}
                active={popupActive}
                getValues={getValues}
              />
            )}
            {/* <AddDocument
                setPopupActive={setPopupActive}
                days={days}
                handleDateChange={handleDateChange}
                yearSelections={yearSelections}
                year={values.year}
                month={values.month}
                day={values.day}
                languages={languages}
                active={popupActive}
              /> */}
          </Popup>
          <form
            data-cy="add-action-form"
            className="lg:w-2/3 pointer-events-auto"
            onSubmit={handleSubmit(submitForm)}
          >
            <input type="hidden" defaultValue="[]" {...register('documents')} />
            <div className="form-row">
              <Select
                data-cy="selectSource"
                label={t('form.Source')}
                name="action_source_id"
                errors={errors}
                register={register}
                required
              >
                <option value="">{t('form.Choose a source')}</option>
                {sources.map((source, index) => (
                  <option key={`source${index}`} value={source.source_id}>
                    {source.name}
                  </option>
                ))}
              </Select>
            </div>
            <div className="form-row">
              <TextInput
                label={t('form.Action name')}
                name="name"
                type="text"
                errors={errors}
                register={register}
                required
              />
            </div>
            <div className="form-row">
              <TextArea
                label={t('form.Description')}
                name="description"
                type="text"
                errors={errors}
                register={register}
              />
            </div>
            <div className="form-row md:flex items-start">
              <Select
                label={t('Year', { ns: 'common' })}
                name="year"
                classes="md:w-1/3 md:mr-4"
                errors={errors}
                register={register}
                onChange={handleDateChange}
                required
              >
                <option value="">{t('Choose', { ns: 'common' })}</option>
                {yearSelections.map((year, index) => (
                  <option key={index} value={year}>
                    {year}
                  </option>
                ))}
              </Select>
              <Select
                label={t('Month', { ns: 'common' })}
                name="month"
                classes="md:w-1/3 md:mr-4 mt-2 md:mt-0"
                errors={errors}
                register={register}
                onChange={handleDateChange}
              >
                <option value="">{t('Choose', { ns: 'common' })}</option>
                {months.map((month, index) => (
                  <option key={index} value={index + 1}>
                    {month}
                  </option>
                ))}
              </Select>
              <Select
                label={t('Day', { ns: 'common' })}
                name="day"
                classes="md:w-1/3 mt-2 md:mt-0"
                errors={errors}
                register={register}
              >
                <option value="">{t('Choose', { ns: 'common' })}</option>
                {days.map((day, index) => (
                  <option key={index} value={day + 1}>
                    {day + 1}
                  </option>
                ))}
              </Select>
            </div>
            <div className="form-row">
              <Select
                data-cy="selectGeographies"
                label={t('form.Geography/Country')}
                name="geography_id"
                errors={errors}
                register={register}
                required
              >
                <option value="">{t('form.Choose a geography')}</option>
                {/* TODO - implement input box with suggestions as in prototype */}
                {geographies.map((geo: Geography) => (
                  <option
                    key={`geo${geo.geography_id}`}
                    value={geo.geography_id}
                  >
                    {geo.english_shortname}
                  </option>
                ))}
              </Select>
            </div>
            <div className="form-row">
              <Select
                data-cy="selectActionType"
                label={t('form.Action type')}
                name="action_type_id"
                errors={errors}
                register={register}
                required
              >
                <option value="">{t('form.Choose an action type')}</option>
                {actionTypes.map((type: ActionType) => (
                  <option
                    key={`type${type.action_type_id}`}
                    value={type.action_type_id}
                  >
                    {type.type_name}
                  </option>
                ))}
              </Select>
            </div>
            <div className="form-row">
              <h3>{t('form.Documents')}</h3>
              <div className="mt-4">
                {errors.documents ? (
                  <p className="error text-red-500 mb-4">
                    {errors.documents?.message}
                  </p>
                ) : null}

                <DocumentList documents={documents} />
              </div>
              <Button
                data-cy="add-doc-modal"
                type="submit"
                onClick={(e) => {
                  e.preventDefault();
                  window.scrollTo(0, 0);
                  setPopupActive(true);
                }}
              >
                {t('form.Add Document')}
              </Button>
            </div>
            <div className="my-4 flex border-t pt-8 mt-10 border-gray-300">
              <Button
                data-cy="submit-add-action-form"
                type="submit"
                color="dark"
                disabled={isSubmitting}
              >
                {t('form.Submit Action')}
              </Button>
            </div>
          </form>
        </div>
      )}
    </>
  );
};

export default AddAction;
