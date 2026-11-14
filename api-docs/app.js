/* Static archived API reference: no requests to backend endpoints are allowed. */
(function () {
  "use strict";

  SwaggerUIBundle({
    url: "./openapi.json",
    dom_id: "#swagger-ui",
    deepLinking: true,
    docExpansion: "list",
    filter: true,
    supportedSubmitMethods: [],
    tryItOutEnabled: false,
    validatorUrl: null,
    persistAuthorization: false,
    requestInterceptor: function (request) {
      var url = new URL(request.url, window.location.href);
      var expected = new URL("./openapi.json", window.location.href);

      if (
        url.href !== expected.href ||
        (request.method && request.method.toUpperCase() !== "GET")
      ) {
        throw new Error(
          "Live API requests are disabled in this archived reference",
        );
      }
      return request;
    },
  });
})();
