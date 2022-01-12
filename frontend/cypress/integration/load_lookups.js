describe('Geographies api testing', () => {
  let token;
  it('authenticates the user', () => {
    cy.visit('http://localhost:3000');
    cy.request({
      method: 'POST',
      url: 'http://localhost:8000/api/token/',
      form: true,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
      body: 'grant_type=&username=user%40navigator.com&password=password&scope=&client_id=test&client_secret=super_secret',
    }).as('authRequest');
    cy.get('@authRequest').then((response) => {
      expect(response.status).to.eq(200);
      token = response;
    });
  });
  it('fetches geographies items - GET', () => {
    cy.request('http://localhost:8000/api/v1/geographies/', {
      headers: {
        Authorization: `Bearer ${token}`,
        'Content-Type': 'application/json',
      },
    }).as('geographyRequest');
    cy.get('@geographyRequest').then((response) => {
      expect(response.status).to.eq(200);
      assert.isArray(response.body, 'Geographies Response is an array');
    });
  });
});
