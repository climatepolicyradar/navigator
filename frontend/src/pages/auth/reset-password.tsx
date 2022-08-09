import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useForm } from 'react-hook-form';
import { useRouter } from 'next/router';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import { useAuth } from '@api/auth';
import LoaderOverlay from '@components/LoaderOverlay';
import Layout from '@components/layouts/Auth';
import AuthWrapper from '@components/auth/AuthWrapper';
import PasswordInput from '@components/form-inputs/PasswordInput';
import Button from '@components/buttons/Button';

type TFormInputs = {
  password: string;
  confirm_password: string;
};

function ResetPassword() {
  const [status, setStatus] = useState(null);
  const { t } = useTranslation('auth');
  const { register: reset } = useAuth();
  const router = useRouter();

  const schema = Yup.object({
    password: Yup.string()
      .required(t('Password is required'))
      .min(8, t('Minimum 8 chars')),
    confirm_password: Yup.string().oneOf(
      [Yup.ref('password'), null],
      t('Passwords must match')
    ),
  });

  useEffect(() => {
    if (status?.activated) router.push('/auth/sign-in?reset=true');
  }, [status]);

  const {
    register,
    handleSubmit,
    formState: { isSubmitting, errors },
  } = useForm<TFormInputs>({
    resolver: yupResolver(schema),
  });

  const submitForm = async (data: TFormInputs) => {
    const { password } = data;
    const token = router.query.token ? router.query.token : 'none';
    const response = await reset({ password, token });
    setStatus(response);
  };

  return (
    <>
      {isSubmitting ? (
        <LoaderOverlay />
      ) : (
        <Layout title={t('Reset your password')}>
          <section className="absolute inset-0 z-10 flex items-center">
            <div className="container py-4">
              <AuthWrapper
                heading={t('Reset your password')}
                description={t('Specify your new password')}
              >
                {status?.error && (
                  <p className="text-red-500 font-bold mt-4">{status.error}</p>
                )}
                <form className="w-full" onSubmit={handleSubmit(submitForm)}>
                  <div className="form-row text-white" data-cy="password">
                    <PasswordInput
                      label={t('Password')}
                      name="password"
                      errors={errors}
                      required
                      register={register}
                    />
                  </div>
                  <div
                    className="form-row text-white"
                    data-cy="confirm-password"
                  >
                    <PasswordInput
                      label={t('Confirm password')}
                      name="confirm_password"
                      errors={errors}
                      required
                      register={register}
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
                      {t('Save password')}
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
}

export default ResetPassword;
