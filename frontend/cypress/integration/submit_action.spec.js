/// <reference types="cypress" />

context('SubmitDocument', () => {
  // beforeEach(() => {
  //   cy.visit('http://localhost:3000');
  // });

  it('Should open the Add Document modal window', () => {
    cy.visit('http://localhost:3000');
    cy.get('#cy-add-doc-modal').click();
    cy.get('#cy-add-document-form').should('have.class', 'is-active');
  });
  it('Should return errors because form fields are all empty', () => {
    cy.get('#cy-submit-add-document-form').click();

    //   cy.get('#cy-add-document-form input[name=name]')
    //     .next('.error')
    //     .should('contain', 'Required');
    cy.get('.error').should('have.length', 4);
  });

  it('Should close the Add Document modal window', () => {
    cy.get('#cy-close-add-document-form').click();
    cy.get('#cy-add-document-form').should('not.have.class', 'is-active');
  });
});
