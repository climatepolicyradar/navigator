describe('SubmitDocument', () => {
  beforeEach(() => {
    cy.visit('http://localhost:3000');
    cy.get('[data-cy="add-doc-modal"]').click();
  });

  //before
  //after
  //afterEach

  it('Should return errors when clicking Add because required form fields are empty', () => {
    cy.get('[data-cy="submit-add-document-form"]').click();
    cy.get('.error').should('have.length', 4);
  });

  it('Should close popup and add to documents list when all required fields are completed and Add button is clicked', () => {
    cy.intercept('POST', 'document', { fixture: 'document' }).as(
      'postDocument'
    );
    cy.get('[data-cy="add-document-form"] input[name=name]').type(
      'Name of document'
    );
    cy.get('[data-cy="add-document-form"] select[name=language_id]').select(
      '193'
    );
    cy.get('[data-cy="add-document-form"]  input[type="file"]').attachFile(
      'somefile.pdf'
    );
    cy.get('[data-cy="add-document-form"] select[name=year]').select('2020');
    cy.get('[data-cy="submit-add-document-form"]').click();
    cy.get('[data-cy="add-document-form"]').should(
      'not.have.class',
      'is-active'
    );
    cy.get('[data-cy="document-list"] li').should('have.length', 1);
  });

  it('Should close the Add Document modal window', () => {
    cy.get('[data-cy="close-add-document-form"]').click();
    cy.get('[data-cy="add-document-form"]').should(
      'not.have.class',
      'is-active'
    );
  });
});
