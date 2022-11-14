import { NavigationHelper } from '../page-objects';

BASE_URL = "localhost:3000"

fixture`Happy Path`
    .page(BASE_URL)

test('Happy path', async () => {
    const navigationHelper = new NavigationHelper();
    const submissionId = await navigationHelper.enterSearchTerm("carbon");
});