import { signInPage } from '../../support/page_objects/signinPage';

describe('Validate user sign in fields', () => {
  before('visit page', () => {
    cy.visit('/auth/sign-in');
  });
  beforeEach('visit page', () => {
    signInPage.clearForm();
  });
  it('Logo should link to the CPR website', () => {
    cy.checkAuthPagesLogo();
  });
  it('should not allow empty email', () => {
    signInPage.enterPassword('1234').submitForm();
    signInPage.getEmailError().should('have.text', 'Email is required');
  });
  it('should not allow invalid email', () => {
    signInPage.signIn('someemail@', '1234').submitForm();
    signInPage.getEmailError().should('have.text', 'Invalid email format');
  });
  it('should not allow empty password', () => {
    signInPage.enterEmail('someemail@website.com').submitForm();
    signInPage.getPasswordError().should('have.text', 'Password is required');
  });
  it('should redirect to the password reset page', () => {
    cy.clickTextLink('Forgot password?');
    cy.location('pathname', { timeout: 1000 }).should('eq', '/auth/reset-request');
  });
});

describe('Validate request access link', () => {
  before('visit page', () => {
    cy.visit('/auth/sign-in');
  });
  it('should link to the request form on the website', () => {
    cy.visit('/auth/sign-in');
    cy.contains('a', 'Request early access')
      .invoke('attr', 'href')
      .then((href) => {
        expect(href).to.equal('https://climatepolicyradar.org/request-access');
      });
  });
})
