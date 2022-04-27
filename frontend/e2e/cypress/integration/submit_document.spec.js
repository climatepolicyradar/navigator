describe('SubmitDocument', () => {
  beforeEach(() => {
    cy.login();
    cy.wait(100);
    cy.visit('http://localhost:3000/add-action');
    cy.get_lookups();
    cy.get('[data-cy="add-doc-modal"]').click();
  });

  it('Select list should be populated with language choices', () => {
    cy.get('[data-cy="selectLanguages"] option').should('have.length', 11);
  });

  it('Should return errors when clicking Add because required form fields are empty', () => {
    cy.get('[data-cy="submit-add-document-form"]').click();
    cy.get('.error').should('have.length', 4);
  });

  it('Should close popup and add to documents list when all required fields are completed and Add button is clicked', () => {
    cy.submit_pdf_file();
    cy.get('[data-cy="add-document-form"]').should('not.exist');
    cy.get('[data-cy="document-list"] li').should('have.length', 1);
  });

  it('Should close the Add Document modal window', () => {
    cy.get('[data-cy="close-add-document-form"]').click();
    cy.get('[data-cy="add-document-form"]').should('not.exist');
  });
});
