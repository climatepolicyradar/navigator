import '../i18n';
import { useTranslation } from 'react-i18next';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useAuth, resetRequest } from '../../api/auth';
import Layout from '../../components/layouts/Main';
import PasswordInput from '../../components/form-inputs/PasswordInput';
import AccountNav from '../../components/nav/AccountNav';
import AdminSubhead from '../../components/headers/AdminSubhead';
import Button from '../../components/buttons/Button';

const Account = () => {
  const { t, i18n, ready } = useTranslation(['account', 'auth']);
  const { user, register: changePassword } = useAuth();

  const schema = Yup.object({
    // password: Yup.string().required(t('auth:Password is required')),
    password: Yup.string()
      .required(t('auth:Password is required'))
      .min(8, t('auth:Minimum 8 chars')),
    confirm_new_password: Yup.string().oneOf(
      [Yup.ref('new_password'), null],
      t('auth:Passwords must match')
    ),
  });
  const {
    register,
    handleSubmit,
    reset,
    formState: { isSubmitting, errors, isSubmitSuccessful, isValid, isDirty },
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      password: '',
      new_password: '',
      confirm_new_password: '',
    },
  });
  const cancelUpdate = () => {
    reset();
  };
  const submitForm = (data) => {
    console.log(data);
  };

  return (
    <Layout
      title={`Climate Policy Radar | ${t('My account')}`}
      heading={t('My account')}
    >
      <section>
        <div className="container py-4">
          <AccountNav />
          <AdminSubhead
            heading={t('Change password')}
            description={t(
              'Please enter your current password to change your password.'
            )}
          />
          <form className="w-full" onSubmit={handleSubmit(submitForm)}>
            {/* <div className="form-row__border md:flex">
              <label className="flex-shrink-0 md:w-1/4">
                {t('Current password')}{' '}
                <strong className="text-red-500"> *</strong>
              </label>
              <div className="flex-grow">
                <TextInput
                  name="password"
                  type="password"
                  errors={errors}
                  required
                  register={register}
                />
              </div>
            </div> */}
            <div className="form-row__border md:flex">
              <label className="flex-shrink-0 md:w-1/4">
                {t('New password')} <strong className="text-red-500"> *</strong>
              </label>
              <div className="flex-grow">
                <PasswordInput
                  name="password"
                  errors={errors}
                  required
                  register={register}
                />
                <p className="text-indigo-400 mt-1">
                  {t('Your password must be at least 8 characters.')}
                </p>
              </div>
            </div>
            <div className="form-row__border md:flex">
              <label className="flex-shrink-0 md:w-1/4">
                {t('Confirm new password')}{' '}
                <strong className="text-red-500"> *</strong>
              </label>
              <div className="flex-grow">
                <PasswordInput
                  name="confirm_password"
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
                disabled={isDirty ? false : true}
              >
                {t('common:Cancel')}
              </Button>{' '}
              &nbsp; &nbsp;
              <Button color="light-hover-dark" type="submit">
                {t('Update password')}
              </Button>
            </div>
          </form>
        </div>
      </section>
    </Layout>
  );
};
export default Account;
