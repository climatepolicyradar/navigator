import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import '../i18n';
import { useTranslation } from 'react-i18next';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import Link from 'next/link';
import { yupResolver } from '@hookform/resolvers/yup';
import LoaderOverlay from '../../components/LoaderOverlay';
import Layout from '../../components/layouts/Auth';
import AuthWrapper from '../../components/auth/AuthWrapper';
import TextInput from '../../components/form-inputs/TextInput';
import PasswordInput from '../../components/form-inputs/PasswordInput';
import Button from '../../components/buttons/Button';
import { useAuth } from '../../api/auth';

const Login = () => {
  const [status, setStatus] = useState(null);
  const { t, i18n, ready } = useTranslation('auth');
  const { user, login } = useAuth();
  const router = useRouter();

  const schema = Yup.object({
    email: Yup.string()
      .email(t('Invalid email format'))
      .required(t('Email is required')),
    password: Yup.string().required(t('Password is required')),
  });
  const {
    register,
    handleSubmit,
    formState: { isSubmitting, errors, isSubmitSuccessful, isValid },
  } = useForm({
    resolver: yupResolver(schema),
  });

  const welcomeMessage = () => {
    // set message based on how the user arrived to the page
    let message = t('Welcome back! Please enter your details.');
    if (router?.query?.activated) {
      message = t('Your account has been activated! please sign in below.');
    } else if (router?.query?.reset) {
      message = t(
        'Your password has been reset successfully. Please sign in below.'
      );
    }
    return message;
  };
  const submitForm = async (data) => {
    const email = data.email.toLowerCase();
    const newData = { ...data, email: encodeURIComponent(email) };
    const status = await login(newData);
    setStatus(status);
  };

  useEffect(() => {
    // checks if a user account is returned rather than an error
    if (status?.email) router.push('/');
  }, [status]);
  useEffect(() => {
    // redirect if already signed in
    if (user?.email) router.push('/');
  }, [user]);
  return (
    <>
      {isSubmitting || (isSubmitSuccessful && status?.email) ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Climate Policy Radar | ${t('Sign in to your account')}`}
        >
          <section className="absolute inset-0 z-10 flex items-center">
            <div className="container py-4">
              <AuthWrapper
                heading={t('Sign in to your account')}
                description={welcomeMessage()}
              >
                {status?.error && (
                  <p className="text-red-500 font-bold mt-4">{status.error}</p>
                )}

                <form
                  className="w-full"
                  onSubmit={handleSubmit(submitForm)}
                  noValidate
                >
                  <div data-cy="signin-email" className="form-row text-white">
                    <TextInput
                      label={t('Email')}
                      name="email"
                      type="email"
                      errors={errors}
                      required
                      register={register}
                    />
                  </div>
                  <div
                    data-cy="signin-password"
                    className="form-row text-white"
                  >
                    <PasswordInput
                      label={t('Password')}
                      name="password"
                      errors={errors}
                      required
                      register={register}
                    />
                    <div className="mt-6">
                      <Link href="/auth/reset-request">
                        <a className="text-blue-500 hover:text-white transition duration-300">
                          {t('Forgot password?')}
                        </a>
                      </Link>
                    </div>
                  </div>
                  <div data-cy="signin-submit" className="form-row">
                    <Button
                      type="submit"
                      color="light"
                      disabled={isSubmitting}
                      extraClasses="w-full"
                      fullWidth
                    >
                      {t('Sign in')}
                    </Button>
                  </div>
                  <p className="mt-8 text-white text-center">
                    {t("Don't have an account?")} &nbsp;
                    <a
                      href="https://climatepolicyradar.org/request-access"
                      className="text-blue-500 hover:text-white mt-4 transition duration-300"
                    >
                      {t('Request early access')}
                    </a>
                  </p>
                </form>
              </AuthWrapper>
            </div>
          </section>
        </Layout>
      )}
    </>
  );
};

export default Login;
