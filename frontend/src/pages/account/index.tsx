import { useAuth } from '../../api/auth';
import '../i18n';
import { useTranslation } from 'react-i18next';
import Layout from '../../components/layouts/Admin';
import Link from 'next/link';
import AccountNav from '../../components/nav/AccountNav';



const Account = () => {
	const { t, i18n, ready } = useTranslation('account');

	
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
						<h3>My details</h3>
					</div>
					
					<div className="py-4">
						<div className="font-medium">{user.first_name} {user.last_name}</div>
						<div className="mt-4">{user.email}</div>
					</div>
				</div>
			</section>
		</Layout>
	)

}
export default Account;