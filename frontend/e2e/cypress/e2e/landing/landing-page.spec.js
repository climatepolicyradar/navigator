/// <reference types="cypress" />

describe("Landing page", () => {
  before(() => {
    cy.visit("/");
  });

  it("should see placeholder text", () => {
    cy.get('[data-cy="search-input"]')
      .invoke("attr", "placeholder")
      .then((text) => {
        expect(text).to.equal("Search full text of 3000+ laws and policies");
      });
  });

  it("should display a placeholder animated element", () => {
    cy.get(".search-animated-placeholder").should("be.visible");
  });

  it("should hide the animated placeholder when the input is interacted with", () => {
    cy.get('[data-cy="search-input"]').click();
    cy.get(".search-animated-placeholder").should("not.exist");
  });

  it("should display the value that is typed in", () => {
    cy.get('[data-cy="search-input"]')
      .clear()
      .type("This is a test input")
      .invoke("val")
      .then((val) => {
        const myVal = val;
        expect(myVal).to.equal("This is a test input");
      });
  });
});
