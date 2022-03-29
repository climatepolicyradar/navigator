import { useEffect } from 'react';
import { useRouter } from 'next/router';
import '../i18n';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../../components/LoaderOverlay';
import Layout from '../../components/layouts/Auth';
import AuthWrapper from '../../components/auth/AuthWrapper';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import TextInput from '../../components/form-inputs/TextInput';
import Button from '../../components/buttons/Button';
import Link from 'next/link';
import { useAuth } from '../../api/auth';

const Login = () => {
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
  const submitForm = (data) => {
    // console.log(data);
    login(data);
  };
  useEffect(() => {
    if (user?.first_name) router.push('/account');
  }, [user]);
  return (
    <>
      {!ready ? (
        <LoaderOverlay />
      ) : (
        <Layout title={`Navigator | ${t('Sign in to your account')}`}>
          <section className="absolute inset-0 z-10 flex items-center">
            <div className="container py-4">
              <AuthWrapper
                heading={t('Sign in to your account')}
                description={t('Welcome back! Please enter your details.')}
              >
                {user?.error && (
                  <p className="text-red-500 font-bold mt-4">{user.error}</p>
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
                    <TextInput
                      label={t('Password')}
                      name="password"
                      type="password"
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
