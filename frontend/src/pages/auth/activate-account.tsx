import '../i18n';
import { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../../components/LoaderOverlay';
import Layout from '../../components/layouts/Auth';
import AuthWrapper from '../../components/auth/AuthWrapper';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import TextInput from '../../components/form-inputs/TextInput';
import Button from '../../components/buttons/Button';
import { useAuth } from '../../api/auth';

const ActivateAccount = () => {
  const [status, setStatus] = useState(null);
  const router = useRouter();
  const { t, i18n, ready } = useTranslation('auth');
  const { user, register: activate } = useAuth();
  const schema = Yup.object({
    /* TODO: decide on password requirements */
    password: Yup.string()
      .required(t('Password is required'))
      .min(8, t('Minimum 8 chars')),
    confirm_password: Yup.string().oneOf(
      [Yup.ref('password'), null],
      t('Passwords must match')
    ),
  });
  const {
    register,
    handleSubmit,
    getValues,
    setValue,
    formState: { isSubmitting, errors, isSubmitSuccessful, isValid },
    reset,
    watch,
  } = useForm({
    resolver: yupResolver(schema),
    // defaultValues: initialValues,
  });
  const submitForm = async (data) => {
    const { password } = data;
    const token = router.query.token;
    const response = await activate({ password, token });
    setStatus(response);
  };
  useEffect(() => {
    if (status?.activated) router.push('/auth/signin?activated=true');
  }, [status]);
  return (
    <>
      {isSubmitting ? (
        <LoaderOverlay />
      ) : (
        <Layout title={`Navigator | ${t('Activate your account')}`}>
          <section className="absolute inset-0 z-10 flex items-center">
            <div className="container py-4">
              <AuthWrapper
                heading={t('Activate your account')}
                description={t('Specify your password')}
              >
                {status?.error && (
                  <p className="text-red-500 font-bold mt-4">{status.error}</p>
                )}
                <form className="w-full" onSubmit={handleSubmit(submitForm)}>
                  <div className="form-row text-white">
                    <TextInput
                      label={t('Password')}
                      name="password"
                      type="password"
                      errors={errors}
                      required
                      register={register}
                    />
                  </div>
                  <div className="form-row text-white">
                    <TextInput
                      label={t('Confirm password')}
                      name="confirm_password"
                      type="password"
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
                      {t('Activate')}
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

export default ActivateAccount;
