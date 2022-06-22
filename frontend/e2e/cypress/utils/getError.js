// Current uniform DOM for the location of errors
// TODO: consider and alternative of dynamically applying data-cy attributes to inputs and errors
/**
 * 
 * @param {inputSelector} inputSelector the DOM location of the input
 * @returns The error DOM object
 */
export const getError = (inputSelector) => {
  return cy.get(inputSelector).parent().next('.error');
};
