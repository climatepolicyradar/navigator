/// <reference types="cypress" />

describe('Search Input', () => {
  beforeEach(() => {
    cy.login();
    cy.wait(100);
    cy.visit('http://localhost:3000');
  });
  it('Search input placeholder text should be set', () => {
    // wait for animation
    cy.wait(2000);
    cy.get('[data-cy="search-input"]').should(
      'have.attr',
      'placeholder',
      'Search full text of 1032 laws and policies'
    );
  });
  it('Clear search button should not be visible until typing a search term', () => {
    cy.get('[data-cy="search-clear-button"]').should('not.exist');
    cy.get('[data-cy="search-input"]').type('carbon taxes');
    cy.get('[data-cy="search-clear-button"]').should('exist');
  });
  it('Clicking the clear search button should clear the search terms in the input box and hide the button', () => {
    cy.get('[data-cy="search-input"]').type('carbon taxes');
    cy.get('[data-cy="search-input"]').should(
      'have.attr',
      'value',
      'carbon taxes'
    );
    cy.get('[data-cy="search-clear-button"]').click();
    cy.get('[data-cy="search-input"]').should('have.attr', 'value', '');
    cy.get('[data-cy="search-clear-button"]').should('not.exist');
  });
});
