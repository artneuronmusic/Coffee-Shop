/* @TODO replace with your variables
 * ensure all variables on this page match your project, http://localhost:8100 
 */

export const environment = {
  production: false,
  apiServerUrl: 'https://127.0.0.1:8000/login', // the running FLASK api server url
  auth0: {
    url: 'fsnd-coffeeshop-udacity.us.auth0.com', // the auth0 domain prefix
    audience: 'coffee_shop', // the audience set for the auth0 app
    clientId: '5KFAASKQvgBNfETwse5YTV9QWpBobQaL', // the client id generated for the auth0 app
    callbackURL: 'http://127.0.0.1:8000/login_result', // the base url of the running ionic application. 
  }
};
