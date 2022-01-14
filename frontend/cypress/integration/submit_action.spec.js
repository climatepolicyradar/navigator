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

  it('Should show errors when any required fields are not filled out', () => {
    cy.visit('http://localhost:3000');
    cy.get('[data-cy="submit-add-action-form"]').click();
    cy.get('.error').should('have.length', 6);
  });

  it('Should open the Add Document modal window', () => {
    cy.visit('http://localhost:3000');
    cy.get('[data-cy="add-doc-modal"]').click();
    cy.get('[data-cy="add-document-form"]').should('have.class', 'is-active');
  });

  it('should fill out form and display success message on submit', () => {
    cy.visit('http://localhost:3000');
    cy.get('[data-cy="add-action-form"] select[name=source_id]').select('1');
    cy.get('[data-cy="add-action-form"] input[name=name]').type(
      'Name of action'
    );
    cy.get('[data-cy="add-action-form"] select[name=year]').select('2020');
    cy.get('[data-cy="add-action-form"] select[name=geography_id]').select('3');
    cy.get('[data-cy="add-action-form"] select[name=type_id]').select('1');
    // open add document modal
    cy.get('[data-cy="add-doc-modal"]').click();
    cy.submit_pdf_file();

    cy.get('[data-cy="submit-add-action-form"]').click();

    cy.get('[data-cy="message"]').should('contain', 'Success!');
  });
});
