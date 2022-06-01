import '../i18n';
import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../../components/LoaderOverlay';
import Layout from '../../components/layouts/Auth';
import AuthWrapper from '../../components/auth/AuthWrapper';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import TextInput from '../../components/form-inputs/TextInput';
import Button from '../../components/buttons/Button';
import { useAuth, resetRequest } from '../../api/auth';
import { useRouter } from 'next/router';

const ResetRequest = () => {
  const [status, setStatus] = useState(null);
  const { t, i18n, ready } = useTranslation('auth');
  const router = useRouter();
  const { user, register: reset } = useAuth();
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
  const submitForm = async (data) => {
    const email = data.email.toLowerCase();
    const status = await resetRequest(encodeURIComponent(email));
    setStatus(status);
  };
  useEffect(() => {
    // redirect if already signed in
    if (user?.email) router.push('/');
  }, [user]);
  return (
    <>
      {isSubmitting ? (
        <LoaderOverlay />
      ) : (
        <Layout title={`Climate Policy Radar | ${t('Reset your password')}`}>
          <section className="absolute inset-0 z-10 flex items-center">
            <div className="container py-4">
              {status?.data === true ? (
                <AuthWrapper
                  heading={t('Reset request sent')}
                  description={t(
                    'Please check your email and click the enclosed link to reset your password.'
                  )}
                />
              ) : (
                <AuthWrapper
                  heading={t('Reset your password')}
                  description={t(
                    'Enter your email you signed up with.<br>We will send you a link.'
                  )}
                >
                  {status?.error && (
                    <p className="text-red-500 font-bold mt-4">
                      {status.error}
                    </p>
                  )}
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
              )}
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};

export default ResetRequest;
