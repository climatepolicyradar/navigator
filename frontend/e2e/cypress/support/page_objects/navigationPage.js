export class NavigationPage {
  aboutUsPage() {
    cy.contains('[data-cy="dropdown-menu"] a', 'About us').click();
  }
  methodologyPage() {
    cy.contains('[data-cy="dropdown-menu"] a', 'Methodology').click();
  }
  accountPage() {
    cy.contains('[data-cy="dropdown-menu"] a', 'My account').click();
  }
  signOutPage() {
    cy.contains('[data-cy="dropdown-menu"] button', 'Sign out').click();
  }
}
export const navigateTo = new NavigationPage();
