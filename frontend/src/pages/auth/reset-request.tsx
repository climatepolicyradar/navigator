import { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { useRouter } from 'next/router';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useAuth, resetRequest } from '@api/auth';
import LoaderOverlay from '@components/LoaderOverlay';
import Layout from '@components/layouts/Auth';
import AuthWrapper from '@components/auth/AuthWrapper';
import TextInput from '@components/form-inputs/TextInput';
import Button from '@components/buttons/Button';

type TFormInputs = {
  email: string;
};

function ResetRequest() {
  const [status, setStatus] = useState(null);
  const { t } = useTranslation('auth');
  const router = useRouter();
  const { user } = useAuth();

  useEffect(() => {
    // redirect if already signed in
    if (user?.email) router.push('/');
  }, [user]);

  const schema = Yup.object({
    email: Yup.string()
      .email(t('Invalid email format'))
      .required('Email is required'),
  });

  const {
    register,
    handleSubmit,
    formState: { isSubmitting, errors },
  } = useForm<TFormInputs>({
    resolver: yupResolver(schema),
  });

  const submitForm = async (data: TFormInputs) => {
    const email = data.email.toLowerCase();
    const status = await resetRequest(encodeURIComponent(email));
    setStatus(status);
  };

  return (
    <>
      {isSubmitting ? (
        <LoaderOverlay />
      ) : (
        <Layout title={t('Reset your password')} height={600}>
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
                  <p className="text-red-500 font-bold mt-4">{status.error}</p>
                )}
                <form
                  className="w-full"
                  onSubmit={handleSubmit(submitForm)}
                  noValidate
                >
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
        </Layout>
      )}
    </>
  );
}

export default ResetRequest;
