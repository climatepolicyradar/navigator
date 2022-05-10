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
    cy.get('[data-cy="header-logo"]').should('be.visible');
  });
  it('Logo should link to company website', () => {
    cy.get('[data-cy="header-logo"]')
      .closest('a')
      .should('have.attr', 'href', 'https://climatepolicyradar.org');
  });
  it('Product name should be visible', () => {
    cy.get('[data-cy="product-name"]').should('be.visible');
    cy.get('[data-cy="alpha"]').should('be.visible');
  });
  it('Product name should link to home page', () => {
    cy.get('[data-cy="product-name"] > a').should('have.attr', 'href', '/');
  });
  it('Account menu icon/button should be visible', () => {
    cy.get('[data-cy="menu-icon"]').should('be.visible');
  });
  it('Account menu icon should be visible on menu icon click', () => {
    cy.get('[data-cy="menu-icon"]').click();
    cy.get('[data-cy="dropdown-menu"]').should('be.visible');
  });
  // it('Header should become fixed to top on scroll', () => {
  //   cy.wait(2000);
  //   cy.scrollTo(0, 100);
  //   cy.get('[data-cy="header"]').should('have.class', 'fixed');
  // });
});
