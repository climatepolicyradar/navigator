import './i18n';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../components/LoaderOverlay';
import Layout from '../components/layouts/Auth';
import AuthWrapper from '../components/auth/AuthWrapper';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import TextInput from '../components/form-inputs/TextInput';
import Button from '../components/buttons/Button';

const ResetRequest = () => {
  const { t, i18n, ready } = useTranslation('auth');
  const schema = Yup.object({
    email: Yup.string()
      .email(t('Invalid email format'))
      .required('Email is required'),
  });
  const {
    register,
    handleSubmit,
    formState: { isSubmitting, errors, isSubmitSuccessful, isValid },
  } = useForm({
    resolver: yupResolver(schema),
  });
  const submitForm = (data) => {
    console.log(data);
  };
  return (
    <>
      {!ready ? (
        <LoaderOverlay />
      ) : (
        <Layout title={`Navigator | ${t('Reset your password')}`}>
          <section className="absolute inset-0 z-10 flex items-center">
            <div className="container py-4">
              <AuthWrapper
                heading={t('Reset your password')}
                description={t(
                  'Enter your email you signed up with.<br>We will send you a link.'
                )}
              >
                <form className="w-full" onSubmit={handleSubmit(submitForm)}>
                  <div className="form-row text-white">
                    <TextInput
                      label={t('Email')}
                      name="email"
                      type="email"
                      errors={errors}
                      required
                      register={register}
                      placeholder="Enter your email"
                    />
                  </div>
                  <div className="mt-8">
                    <Button
                      type="submit"
                      color="light"
                      disabled={isSubmitting}
                      extraClasses="w-full"
                      fullWidth
                    >
                      {t('Reset password')}
                    </Button>
                  </div>
                </form>
              </AuthWrapper>
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};

export default ResetRequest;
