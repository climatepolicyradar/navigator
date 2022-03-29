/// <reference types="cypress" />

describe('Dashboard', () => {
  beforeEach(() => {
    cy.login();
    cy.wait(100);
    cy.visit('http://localhost:3000');
  });
  it('Dashboard should show three panels', () => {
    cy.get('[data-cy="dashboard"]').find('div').should('have.length', 3);
  });

  it('Dashboard should scroll horizontally on mobile screens', () => {
    cy.viewport(335, 600);
    // if element is not scrollable, this will fail
    cy.get('[data-cy="dashboard"]').scrollTo('right');
  });
});

describe('Search Input', () => {
  beforeEach(() => {
    cy.login();
    cy.wait(100);
    cy.visit('http://localhost:3000');
  });
  it('Search input placeholder text should be set', () => {
    cy.get('[data-cy="search-input"]').should(
      'have.attr',
      'placeholder',
      "Search for something, e.g. 'carbon taxes'"
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
