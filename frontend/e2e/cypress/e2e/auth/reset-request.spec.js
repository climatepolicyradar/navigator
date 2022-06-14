import { signInPage } from '../../support/page_objects/signinPage';

describe('Validate reset request page fields', () => {
  beforeEach('visit page', () => {
    cy.visit('/auth/reset-request');
  });
  it('Logo should link to the CPR website', () => {
    cy.checkAuthPagesLogo();
  });
  it('Title should be Reset your password', () => {
    cy.getAuthPageTitle('Reset your password');
  });
  it('should not allow empty email', () => {
    signInPage.submitForm();
    signInPage.getEmailError().should('have.text', 'Email is required');
  });
  it('should not allow invalid email', () => {
    signInPage.enterEmail('someemail').submitForm();
    signInPage.getEmailError().should('have.text', 'Invalid email format');
  });
});
