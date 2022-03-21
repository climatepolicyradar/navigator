import './i18n';
import { useTranslation } from 'react-i18next';
import LoaderOverlay from '../components/LoaderOverlay';
import Layout from '../components/layouts/Auth';
import Logo from '../components/Logo';
import AuthWrapper from '../components/auth/AuthWrapper';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import TextInput from '../components/form-inputs/TextInput';
import Button from '../components/buttons/Button';

const ActivateAccount = () => {
  const { t, i18n, ready } = useTranslation('auth');
  const schema = Yup.object({
    /* TODO: decide on password requirements */
    password: Yup.string().required(t('Password is required')).min(6),
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
  const submitForm = (data) => {
    console.log(data);
  };
  return (
    <>
      {!ready ? (
        <LoaderOverlay />
      ) : (
        <Layout
          title={`Navigator | ${t('Activate your account')}`}
          heading={t('Activate your account')}
        >
          <section>
            <div className="container py-4">
              <AuthWrapper
                heading="Activate your account"
                description="Specify your password"
              >
                <form onSubmit={handleSubmit(submitForm)}>
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
                  <div className="my-4 flex mt-8">
                    <Button
                      data-cy="submit-add-action-form"
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
