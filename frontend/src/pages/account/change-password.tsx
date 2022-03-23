import { useAuth } from '../../api/auth';
import '../i18n';
import { useTranslation } from 'react-i18next';
import Layout from '../../components/layouts/Admin';
import TextInput from '../../components/form-inputs/TextInput';
import { useForm } from 'react-hook-form';
import * as Yup from 'yup';
import { yupResolver } from '@hookform/resolvers/yup';
import AccountNav from '../../components/nav/AccountNav';


const Account = () => {
    const { t, i18n, ready } = useTranslation('account');

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
			formState: { isSubmitting, errors, isSubmitSuccessful, isValid },
		} = useForm({
			resolver: yupResolver(schema),
		});
		const submitForm = (data) => {
			console.log(data);
		};
    /* TODO: authentication for this page, static for now 
        Try Next-Auth + React-query: https://github.com/nextauthjs/react-query
        also refer to https://next-auth.js.org/
    */
    const user = {
        email: 'myemail@email.com',
        is_active: true,
        is_superuser: false,
        first_name: 'Paula',
        last_name: 'Hightower',
        id: 1
    }
    
    return (
			<Layout
				title={`Navigator | ${t('My account')}`}
				heading={t('My account')}
			>
				<section>
					<div className="container py-4">
						
							<AccountNav />
							<div className="border-b border-b-indigo-200 py-4">
								<h3>Change password</h3>
								<p>Please enter your current password to change your password.</p>
							</div>
							<div className="border-b-indigo-200 form-row">
								<label>Password</label>
								<TextInput
										name="confirm_password"
										type="password"
										errors={errors}
										required
										register={register}
									/>
							</div>
							
							
					</div>
				</section>
			</Layout>
    )

}
export default Account;