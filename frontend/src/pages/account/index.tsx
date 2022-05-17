import { useState, useEffect } from 'react';
import '../i18n';
import { useTranslation } from 'react-i18next';
import Layout from '../../components/layouts/Admin';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import AccountNav from '../../components/nav/AccountNav';
import AdminSubhead from '../../components/headers/AdminSubhead';
import TextInput from '../../components/form-inputs/TextInput';
import Select from '../../components/form-inputs/Select';
import Checkbox from '../../components/form-inputs/Checkbox';
import Button from '../../components/buttons/Button';
import { geo_scope, affiliation_types } from '../../constants/formOptions';
import { EditIcon } from '../../components/Icons';
import Link from 'next/link';
import { useAuth } from '../../api/auth';
import useUpdateAccount from '../../hooks/useUpdateAccount';
import Loader from '../../components/Loader';

const Account = () => {
  const { t, i18n, ready } = useTranslation(['account', 'common']);
  const { user } = useAuth();
  const updateAccount = useUpdateAccount();

  const initialValues = {
    id: null,
    names: '',
    email: '',
    is_active: false,
    is_superuser: false,
    affiliation_organisation: '',
    affiliation_type: [],
    job_role: '',
    location: '',
    geographies_of_interest: [],
  };

  const [geos, setGeos] = useState(initialValues.geographies_of_interest);

  const schema = Yup.object({
    names: Yup.string().required(),
    //  email: Yup.string().email(t('Invalid email format')).required(t('Email is required')),
  });
  const {
    register,
    handleSubmit,
    reset,
    getValues,
    setValue,
    formState: { isSubmitting, errors, isSubmitSuccessful, isValid, isDirty },
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: initialValues,
  });
  const checkBoxChange = (e) => {
    let arr = [];
    const val = e.currentTarget.value;
    if (e.currentTarget.checked) {
      arr = [...geos, val];
    } else {
      arr = geos.filter((geo) => geo != val);
    }
    setGeos(arr);
    // setAccount({ ...account, geographies: arr });
    // updateAccount.mutate({ ...account, geographies: arr });
  };
  const submitForm = (data) => {
    console.log(data);
    updateAccount.mutate(data);
  };

  const cancelUpdate = (e) => {
    e.preventDefault();
    resetAccount();
  };

  const resetAccount = () => {
    console.log(user.geographies_of_interest);
    const geos = user.geographies_of_interest
      ? user.geographies_of_interest
      : [];
    reset({
      id: user.id,
      names: user.names,
      email: user.email,
      is_active: user.is_active,
      is_superuser: user.is_superuser,
      affiliation_organisation: user.affiliation_organisation,
      affiliation_type: user.affiliation_type,
      job_role: user.job_role,
      location: user.location,
      geographies_of_interest: geos,
    });
    setGeos(geos);
  };

  useEffect(() => {
    if (user) {
      resetAccount();
    }
  }, [user]);

  return (
    <Layout title={`Navigator | ${t('My account')}`} heading={t('My account')}>
      {console.log(geos)}
      <section>
        <div className="container py-4">
          {isSubmitting ? (
            <Loader />
          ) : (
            <>
              <AccountNav />
              <AdminSubhead heading={t('My details')} />
              <form className="w-full" onSubmit={handleSubmit(submitForm)}>
                <div className="form-row__border md:flex">
                  <label className="flex-shrink-0 md:w-1/4">
                    {t('Full name')}{' '}
                    <strong className="text-red-500"> *</strong>
                  </label>
                  <div className="flex-grow">
                    <TextInput
                      name="names"
                      type="text"
                      errors={errors}
                      required
                      register={register}
                    />
                  </div>
                </div>
                <div className="form-row__border md:flex">
                  <label className="flex-shrink-0 md:w-1/4">
                    {t('common:Email')}
                  </label>
                  <div className="flex-grow">{user?.email}</div>
                  <Link href="/account/change-email">
                    <a>
                      <EditIcon />
                    </a>
                  </Link>
                </div>
                <div className="form-row__border md:flex">
                  <label className="flex-shrink-0 md:w-1/4">
                    {t('Organisation/affiliation')}
                  </label>
                  <div className="flex-grow">
                    <TextInput
                      name="affiliation_organisation"
                      type="text"
                      errors={errors}
                      required
                      register={register}
                    />
                  </div>
                </div>
                <div className="form-row__border md:flex">
                  <label className="flex-shrink-0 md:w-1/4">
                    {t('Affiliation type')}
                  </label>
                  <div className="flex-grow">
                    <Select
                      name="affiliation_type"
                      errors={errors}
                      required
                      register={register}
                    >
                      <option value="">{t('Choose a type')}</option>
                      {affiliation_types.map((type, index) => (
                        <option key={`afftype${index}`} value={type.value}>
                          {type.label}
                        </option>
                      ))}
                    </Select>
                  </div>
                </div>
                <div className="form-row__border md:flex">
                  <label className="flex-shrink-0 md:w-1/4">
                    {t('Job role')}
                  </label>
                  <div className="flex-grow">
                    <TextInput
                      name="job_role"
                      type="text"
                      errors={errors}
                      required
                      register={register}
                    />
                  </div>
                </div>
                <div className="form-row__border md:flex">
                  <label className="flex-shrink-0 md:w-1/4">
                    {t('Location')}
                  </label>
                  <div className="flex-grow">
                    <TextInput
                      name="location"
                      type="text"
                      errors={errors}
                      required
                      register={register}
                    />
                  </div>
                </div>
                <div className="form-row__border md:flex">
                  <label className="flex-shrink-0 md:w-1/4">
                    {t('Geographies of interest')}
                  </label>
                  <div className="flex-grow">
                    <fieldset className="grid grid-cols-2">
                      {geo_scope.map((item, index) => (
                        <Checkbox
                          key={`geo${index}`}
                          id={item.id}
                          register={register}
                          errors={errors}
                          name="geographies_of_interest[]"
                          label={item.label}
                          value={item.value}
                          onClick={checkBoxChange}
                        />
                      ))}
                    </fieldset>
                  </div>
                </div>
                <div className="form-row md:flex md:justify-end">
                  <Button
                    color="clear"
                    type="button"
                    onClick={cancelUpdate}
                    disabled={isDirty ? false : true}
                  >
                    {t('common:Cancel')}
                  </Button>{' '}
                  &nbsp; &nbsp;
                  <Button color="light-hover-dark" type="submit">
                    {t('Update account')}
                  </Button>
                </div>
              </form>
            </>
          )}
        </div>
      </section>
    </Layout>
  );
};
export default Account;
