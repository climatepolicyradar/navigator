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
import Link from 'next/link';

const Login = () => {
  const { t, i18n, ready } = useTranslation('auth');
  const schema = Yup.object({
    email: Yup.string()
      .email(t('Invalid email format'))
      .required('Email is required'),
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
    console.log(data);
  };
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
                <form className="w-full" onSubmit={handleSubmit(submitForm)}>
                  <div className="form-row text-white">
                    <TextInput
                      label={t('Email')}
                      name="email"
                      type="email"
                      errors={errors}
                      required
                      register={register}
                    />
                  </div>
                  <div className="form-row text-white">
                    <TextInput
                      label={t('Password')}
                      name="password"
                      type="password"
                      errors={errors}
                      required
                      register={register}
                    />
                    <div className="mt-6">
                      <Link href="/reset-password">
                        <a className="text-blue-500 hover:text-white transition duration-300">
                          {t('Forgot password?')}
                        </a>
                      </Link>
                    </div>
                  </div>
                  <div className="form-row">
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
