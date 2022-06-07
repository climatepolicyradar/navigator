/// <reference types="cypress" />

import { navigateTo } from '../../support/page_objects/navigationPage';

describe('Test with Page Objects', () => {
  beforeEach('open application', () => {
    cy.login();
    cy.visit('/');
    cy.get('[data-cy="menu-icon"]').click();
  });
  it('click the menu icon', () => {
    navigateTo.aboutUsPage();
    navigateTo.methodologyPage();
    navigateTo.accountPage();
    navigateTo.signOutPage();
  });
});
