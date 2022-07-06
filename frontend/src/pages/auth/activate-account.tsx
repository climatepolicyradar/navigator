import { useEffect, useState } from "react";
import Link from "next/link";
import { useRouter } from "next/router";
import { useTranslation } from "react-i18next";
import { useForm } from "react-hook-form";
import * as Yup from "yup";
import { yupResolver } from "@hookform/resolvers/yup";
import { useAuth } from "@api/auth";
import LoaderOverlay from "@components/LoaderOverlay";
import Layout from "@components/layouts/Auth";
import AuthWrapper from "@components/auth/AuthWrapper";
import PasswordInput from "@components/form-inputs/PasswordInput";
import Button from "@components/buttons/Button";

type TFormInputs = {
  password: string;
  confirm_password: string;
};

const ActivateAccount = () => {
  const [status, setStatus] = useState(null);
  const router = useRouter();
  const { t } = useTranslation("auth");
  const { user, register: activate } = useAuth();

  useEffect(() => {
    if (status?.activated) router.push("/auth/sign-in?activated=true");
  }, [status]);

  useEffect(() => {
    // redirect if already signed in
    if (user?.email) router.push("/");
  }, [user]);

  const schema = Yup.object({
    /* TODO: decide on password requirements */
    password: Yup.string().required(t("Password is required")).min(8, t("Minimum 8 chars")),
    confirm_password: Yup.string().oneOf([Yup.ref("password"), null], t("Passwords must match")),
  });

  const {
    register,
    handleSubmit,
    formState: { isSubmitting, errors },
  } = useForm<TFormInputs>({
    resolver: yupResolver(schema),
    // defaultValues: initialValues,
  });

  const submitForm = async (data: TFormInputs) => {
    const { password } = data;
    const token = router.query.token ? router.query.token : "none";
    const response = await activate({ password, token });
    setStatus(response);
  };

  return (
    <>
      {isSubmitting ? (
        <LoaderOverlay />
      ) : (
        <Layout title={t("Activate your account")}>
          <section className="absolute inset-0 z-10 flex items-center">
            <div className="container py-4">
              <AuthWrapper heading={t("Activate your account")} description={t("Specify your password")}>
                {status?.error && <p className="text-red-500 font-bold mt-4">{status.error}</p>}
                <form className="w-full" onSubmit={handleSubmit(submitForm)}>
                  <div className="form-row text-white" data-cy="password">
                    <PasswordInput label={t("Password")} name="password" errors={errors} required register={register} />
                  </div>
                  <div className="form-row text-white" data-cy="confirm-password">
                    <PasswordInput label={t("Confirm password")} name="confirm_password" errors={errors} required register={register} />
                  </div>
                  <div className="mt-8">
                    <Button type="submit" color="light" disabled={isSubmitting} extraClasses="w-full" fullWidth>
                      {t("Activate")}
                    </Button>
                  </div>
                  <p className="mt-8 text-white text-center">
                    {t("Already have an account?")} &nbsp;
                    <Link href="/auth/sign-in">
                      <a className="text-blue-500 hover:text-white mt-4 transition duration-300">{t("Click here to sign in")}</a>
                    </Link>
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

export default ActivateAccount;
