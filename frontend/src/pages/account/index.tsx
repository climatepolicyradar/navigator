import { useState } from 'react';
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

const Account = () => {
  const { t, i18n, ready } = useTranslation(['account', 'common']);

  /* TODO: authentication for this page, static for now 
			Try Next-Auth + React-query: https://github.com/nextauthjs/react-query
			also refer to https://next-auth.js.org/

			TODO: also make sure state is managed with react-query (assuming the above
				handles this automatically anyway) instead of useState
	*/
  const initialValues = {
    id: 1,
    full_name: 'Paula Hightower',
    email: 'myemail@email.com',
    is_active: true,
    is_superuser: false,
    affiliation: 'My Affil',
    affiliation_type: 'NGO',
    job_role: 'Researcher',
    location: 'UK',
    geographies: ['Global'],
  };
  const [user, setUser] = useState(initialValues);

  const schema = Yup.object({
    full_name: Yup.string().required(),
    email: Yup.string().required(),
  });
  const {
    register,
    handleSubmit,
    reset,
    getValues,
    formState: { isSubmitting, errors, isSubmitSuccessful, isValid, isDirty },
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: initialValues,
  });
  const checkBoxChange = (e) => {
    let arr = [];
    const val = e.currentTarget.value;
    if (e.currentTarget.checked) {
      arr = [...user.geographies, val];
    } else {
      arr = user.geographies.filter((geo) => geo != val);
    }
    setUser({ ...user, geographies: arr });
  };
  const submitForm = (data) => {
    console.log(data);
  };

  const cancelUpdate = (e) => {
    e.preventDefault();
    setUser(initialValues);
    reset();
  };

  return (
    <Layout title={`Navigator | ${t('My account')}`} heading={t('My account')}>
      <section>
        <div className="container py-4">
          <AccountNav />
          <AdminSubhead heading={t('My details')} />
          <form className="w-full" onSubmit={handleSubmit(submitForm)}>
            <div className="form-row__border md:flex">
              <label className="flex-shrink-0 md:w-1/4">
                {t('Full name')} <strong className="text-red-500"> *</strong>
              </label>
              <div className="flex-grow">
                <TextInput
                  name="full_name"
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
              <div className="flex-grow">{user.email}</div>
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
                  name="affiliation"
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
              <label className="flex-shrink-0 md:w-1/4">{t('Job role')}</label>
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
              <label className="flex-shrink-0 md:w-1/4">{t('Location')}</label>
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
                      name="geographies[]"
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
        </div>
      </section>
    </Layout>
  );
};
export default Account;
