/// <reference types="cypress" />

describe('Submit Action form', () => {
  it('should load all lookups', () => {
    cy.intercept('GET', 'sources', { fixture: 'sources' }).as('getSources');
    cy.intercept('GET', 'geographies', { fixture: 'geographies' }).as(
      'getGeographies'
    );
    cy.intercept('GET', 'action_types', { fixture: 'action-types' }).as(
      'getActionTypes'
    );
    cy.intercept('GET', 'languages', { fixture: 'languages' }).as(
      'getLanguages'
    );
    cy.visit('http://localhost:3000/');
    cy.wait('@getSources');
    cy.wait('@getGeographies');
    cy.wait('@getActionTypes');
    cy.wait('@getLanguages');

    cy.get('[data-cy="selectSource"] option').should('have.length', 2);
    cy.get('[data-cy="selectGeographies"] option').should('have.length', 11);
    cy.get('[data-cy="selectActionType"] option').should('have.length', 3);
    cy.get('[data-cy="selectLanguages"] option').should('have.length', 11);
  });

  it('Should open the Add Document modal window', () => {
    cy.visit('http://localhost:3000');
    cy.get('[data-cy="add-doc-modal"]').click();
    cy.get('[data-cy="add-document-form"]').should('have.class', 'is-active');
  });
});
