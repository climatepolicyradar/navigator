import { useAuth } from '../../api/auth';
import '../i18n';
import { useTranslation } from 'react-i18next';
import Layout from '../../components/layouts/Admin';
import TextInput from '../../components/form-inputs/TextInput';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import AccountNav from '../../components/nav/AccountNav';
import AdminSubhead from '../../components/headers/AdminSubhead';
import Button from '../../components/buttons/Button';
import ResetRequest from '../auth/reset-request';

const Account = () => {
  const { t, i18n, ready } = useTranslation(['account', 'auth']);

  const schema = Yup.object({
    email: Yup.string()
      .email(t('Invalid email format'))
      .required(t('Email is required')),
  });
  const {
    register,
    handleSubmit,
    reset,
    formState: { isSubmitting, errors, isSubmitSuccessful, isValid, isDirty },
  } = useForm({
    resolver: yupResolver(schema),
    defaultValues: {
      email: '',
    },
  });
  const cancelUpdate = () => {
    reset();
  };
  const submitForm = (data) => {
    console.log(data);
  };

  return (
    <Layout title={`Navigator | ${t('My account')}`} heading={t('My account')}>
      <section>
        <div className="container py-4">
          <AccountNav />
          <AdminSubhead
            heading={t('Change email')}
            description={t(
              'You will receive an email to confirm this change. Your email will not be updated until you click the confirm link in the email.'
            )}
          />
          <form className="w-full" onSubmit={handleSubmit(submitForm)}>
            <div className="form-row__border md:flex">
              <label className="flex-shrink-0 md:w-1/4">
                {t('New email')} <strong className="text-red-500"> *</strong>
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
                disabled={isDirty ? false : true}
              >
                {t('common:Cancel')}
              </Button>{' '}
              &nbsp; &nbsp;
              <Button color="light-hover-dark" type="submit">
                {t('Update email')}
              </Button>
            </div>
          </form>
        </div>
      </section>
    </Layout>
  );
};
export default Account;
