/// <reference types="cypress" />

describe('Header', () => {
  beforeEach(() => {
    cy.login();
    cy.wait(100);
  });
  it('should go to home page', () => {
    cy.visit('http://localhost:3000');
  });

  it('Logo should be visible', () => {
    cy.get('[data-cy="cpr-logo"]').should('be.visible');
  });

  it('Logo should link to home page', () => {
    cy.get('[data-cy="cpr-logo"] > a').should('have.attr', 'href', '/');
  });
  it('Account menu icon/button should be visible', () => {
    cy.get('[data-cy="menu-icon"]').should('be.visible');
  });
  it('Account menu icon should be visible on menu icon click', () => {
    cy.get('[data-cy="menu-icon"]').click();
    cy.get('[data-cy="dropdown-menu"]').should('be.visible');
  });
});
