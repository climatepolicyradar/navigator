/// <reference types="cypress" />

describe('Header', () => {
  beforeEach(() => {
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
  it('User icon/button should be visible', () => {
    cy.get('[data-cy="user-icon"]').should('be.visible');
  });
  // it('Header should become fixed to top on scroll', () => {
  //   cy.wait(2000);
  //   cy.scrollTo(0, 100);
  //   cy.get('[data-cy="header"]').should('have.class', 'fixed');
  // });
});
