import { useAuth, resetRequest } from '../../api/auth';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import TextInput from '@components/form-inputs/TextInput';
import Layout from '@components/layouts/Main';
import AccountNav from '@components/nav/AccountNav';
import AdminSubhead from '@components/headers/AdminSubhead';
import Button from '@components/buttons/Button';
import LoaderOverlay from '@components/LoaderOverlay';

function Account() {
  const [status, setStatus] = useState(null);
  const { t } = useTranslation(['account', 'auth']);
  const { user, register: request } = useAuth();

  const schema = Yup.object({
    email: Yup.string()
      .email(t('Invalid email format'))
      .required(t('Email is required')),
  });
  const {
    register,
    handleSubmit,
    reset,
    formState: {
 isSubmitting, errors, isSubmitSuccessful, isValid, isDirty 
},
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      email: '',
    },
  });
  const cancelUpdate = () => {
    reset();
  };
  const submitForm = async (data) => {
    // console.log(data);
    const email = data.email.toLowerCase();
    const status = await resetRequest(encodeURIComponent(email));
    setStatus(status);
  };

  return (
    <Layout
      title={`Climate Policy Radar | ${t('My account')}`}
      heading={t('My account')}
    >
      <section>
        <div className="container py-4 relative">
          <AccountNav />
          {isSubmitting ? (
            <div className="absolute z-20 w-full h-96">
              <LoaderOverlay />
            </div>
          ) : status?.data === true ? (
            <AdminSubhead
              heading={t('Password change requested')}
              description={t(
                'Please check your email for the link to change your password.',
              )}
            />
          ) : (
            <>
              <AdminSubhead
                heading={t('Request password change')}
                description={t(
                  'You will receive an email to confirm this change. Your password will not be updated until you click the confirm link in the email.',
                )}
              />
              <form className="w-full" onSubmit={handleSubmit(submitForm)}>
                <div className="form-row__border md:flex">
                  <label className="flex-shrink-0 md:w-1/4">
                    {t('Your email address:')}
:
<strong className="text-red-500"> *</strong>
                  </label>
                  <div className="flex-grow">
                    <TextInput
                      name="email"
                      type="email"
                      errors={errors}
                      required
                      register={register}
                    />
                  </div>
                </div>

                <div className="form-row md:flex md:justify-end">
                  <Button
                    color="clear"
                    type="button"
                    onClick={cancelUpdate}
                    disabled={!isDirty}
                  >
                    {t('common:Cancel')}
                  </Button>
{' '}
                  &nbsp; &nbsp;
                  <Button color="light-hover-dark" type="submit">
                    {t('Request password change')}
                  </Button>
                </div>
              </form>
            </>
          )}
        </div>
      </section>
    </Layout>
  );
}
export default Account;
