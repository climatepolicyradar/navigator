/// <reference types="cypress" />

describe('Submit Action form', () => {
  beforeEach(() => {
    cy.login();
  });
  it('should load all lookups', () => {
    cy.get_lookups();

    cy.get('[data-cy="selectSource"] option').should('have.length', 2);
    cy.get('[data-cy="selectGeographies"] option').should('have.length', 11);
    cy.get('[data-cy="selectActionType"] option').should('have.length', 3);
  });

  it('Should show errors when any required fields are not filled out', () => {
    cy.visit('http://localhost:3000/add-action');
    cy.get('[data-cy="submit-add-action-form"]').click();
    cy.get('.error').should('have.length', 6);
  });

  it('Should open the Add Document modal window', () => {
    cy.visit('http://localhost:3000/add-action');
    cy.get('[data-cy="add-doc-modal"]').click();
    cy.get('[data-cy="add-document-form"]').should('have.class', 'is-active');
  });

  it('should fill out form and display success message on submit', () => {
    cy.intercept('POST', 'actions', { fixture: 'action' }).as('postAction');
    cy.get_lookups();
    cy.get('[data-cy="add-action-form"] select[name=action_source_id]').select(
      '1'
    );
    cy.get('[data-cy="add-action-form"] input[name=name]').type(
      'Name of action'
    );
    cy.get('[data-cy="add-action-form"] select[name=year]').select('2020');
    cy.get('[data-cy="add-action-form"] select[name=geography_id]').select('3');
    cy.get('[data-cy="add-action-form"] select[name=action_type_id]').select(
      '1'
    );
    // open add document modal
    cy.get('[data-cy="add-doc-modal"]').click();
    cy.submit_pdf_file();

    cy.get('[data-cy="submit-add-action-form"]').click();
    cy.wait('@postAction');
    // should scroll to top and success message is visible
    cy.get('[data-cy="message"]').should('be.visible');
    cy.window().its('scrollY').should('equal', 0);
  });
});
